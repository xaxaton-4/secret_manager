#!/bin/sh
set -e

# -------------------------------
# Переменные окружения
# -------------------------------
OPENBAO_URL=${OPENBAO_URL:-http://openbao:8200}
BAO_FILE=${BAO_FILE:-/openbao/file/.bao_token}
TOKENS_FILE="/openbao/file/tokens.env"
POLICIES_DIR="/openbao/policies"
KV_MOUNT_PATH="secret"

# -------------------------------
# Ждем запуска OpenBao
# -------------------------------
echo "Waiting for OpenBao to start..."
until curl -s $OPENBAO_URL/v1/sys/health >/dev/null 2>&1; do
  echo "OpenBao not ready yet..."
  sleep 1
done

echo "OpenBao is up! Waiting 2 sec to ensure full readiness..."
sleep 2

# -------------------------------
# Инициализация OpenBao
# -------------------------------
if [ ! -f "$BAO_FILE" ]; then
  echo "Initializing OpenBao..."
  keys=$(curl -s --request POST --data '{"secret_shares":1,"secret_threshold":1}' $OPENBAO_URL/v1/sys/init)
  unseal_key=$(echo $keys | jq -r '.keys[0]')
  root_token=$(echo $keys | jq -r '.root_token')

  echo "Unsealing OpenBao..."
  curl -s --request PUT --data "{\"key\":\"$unseal_key\"}" $OPENBAO_URL/v1/sys/unseal

  echo "$keys" > $BAO_FILE
  echo "OpenBao initialized and unsealed."
else
  echo "OpenBao already initialized."
  root_token=$(jq -r '.root_token' $BAO_FILE)
fi

# -------------------------------
# Авто-unseal при повторных запусках
# -------------------------------
sealed=$(curl -s $OPENBAO_URL/v1/sys/health | jq -r .sealed)
if [ "$sealed" = "true" ]; then
  echo "OpenBao is sealed. Unsealing..."
  unseal_key=$(jq -r '.keys[0]' $BAO_FILE)
  curl -s --request PUT --data "{\"key\":\"$unseal_key\"}" $OPENBAO_URL/v1/sys/unseal
  echo "OpenBao unsealed."
else
  echo "OpenBao already unsealed."
fi

# -------------------------------
# Монтирование KV v2 движка
# -------------------------------
exists=$(curl -s -H "X-Vault-Token: $root_token" $OPENBAO_URL/v1/sys/mounts | jq -r "has(\"$KV_MOUNT_PATH/\")")
if [ "$exists" != "true" ]; then
  curl -s -X POST -H "X-Vault-Token: $root_token" \
       -H "Content-Type: application/json" \
       --data '{"type": "kv", "options":{"version":"2"}}' \
       $OPENBAO_URL/v1/sys/mounts/$KV_MOUNT_PATH
  echo "KV v2 mounted at $KV_MOUNT_PATH/"
else
  echo "KV v2 already mounted at $KV_MOUNT_PATH/"
fi

# -------------------------------
# Настройка политик
# -------------------------------
apply_policy() {
  local name=$1
  local file=$2
  exists=$(curl -s --header "X-Vault-Token: $root_token" \
           $OPENBAO_URL/v1/sys/policies/acl/$name | jq -r .name 2>/dev/null || echo "")
  if [ "$exists" != "$name" ]; then
    policy_json=$(jq -Rs . < "$file")
    curl -s --header "X-Vault-Token: $root_token" \
         --request PUT \
         --data "{\"policy\": $policy_json}" \
         $OPENBAO_URL/v1/sys/policies/acl/$name
    echo "Policy $name applied."
  else
    echo "Policy $name already exists."
  fi
}

apply_policy "admin" "$POLICIES_DIR/admin-policy.hcl"
apply_policy "user" "$POLICIES_DIR/user-policy.hcl"

# -------------------------------
# Создание токенов
# -------------------------------
if [ ! -f "$TOKENS_FILE" ]; then
  echo "Creating tokens..."

  ADMIN_TOKEN=$(curl -s --header "X-Vault-Token: $root_token" \
    --request POST \
    --data '{"policies":["admin"], "ttl":"24h"}' \
    $OPENBAO_URL/v1/auth/token/create | jq -r '.auth.client_token')

  USER_TOKEN=$(curl -s --header "X-Vault-Token: $root_token" \
    --request POST \
    --data '{"policies":["user"], "ttl":"24h"}' \
    $OPENBAO_URL/v1/auth/token/create | jq -r '.auth.client_token')

  echo "ADMIN_TOKEN=$ADMIN_TOKEN" >> $TOKENS_FILE
  echo "USER_TOKEN=$USER_TOKEN" >> $TOKENS_FILE

  echo "Tokens created and saved to $TOKENS_FILE."
else
  echo "Tokens file already exists. Skipping token creation."
fi

echo "OpenBao setup completed."
