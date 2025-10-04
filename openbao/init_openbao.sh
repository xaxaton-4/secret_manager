#!/bin/sh
set -e

# Получаем переменные из окружения
OPENBAO_URL=${OPENBAO_URL:-http://openbao:8200}
BAO_FILE=${BAO_FILE:-/openbao/file/.bao_token}

POLICIES_DIR="/openbao/policies"

# Проверяем, что OpenBao доступен
echo "Waiting for OpenBao to start..."
until curl -s $OPENBAO_URL/v1/sys/health >/dev/null 2>&1; do
  echo "OpenBao not ready yet..."
  sleep 1
done

echo "OpenBao is up!"
echo "Waiting 2 sec to ensure OpenBao fully ready..."
sleep 2


# Проверяем, что OpenBao не инициализирован
status=$(curl -s $OPENBAO_URL/v1/sys/health | jq -r .initialized)

# Инициализируем OpenBao
if [ "$status" = "false" ]; then
  echo "Initializing OpenBao..."
  keys=$(curl -s --request POST --data '{"secret_shares":1,"secret_threshold":1}' $OPENBAO_URL/v1/sys/init)
  echo "Keys: $keys"
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

# Настройка ACL
admin_policy=$(jq -Rs . < "$POLICIES_DIR/admin-policy.hcl")
user_policy=$(jq -Rs . < "$POLICIES_DIR/user-policy.hcl")

curl -s --header "X-Vault-Token: $root_token" \
  --request PUT \
  --data "{\"policy\": $admin_policy}" \
  $OPENBAO_URL/v1/sys/policies/acl/admin

curl -s --header "X-Vault-Token: $root_token" \
  --request PUT \
  --data "{\"policy\": $user_policy}" \
  $OPENBAO_URL/v1/sys/policies/acl/user

# Создаем токен администратора
ADMIN_TOKEN=$(curl -s --header "X-Vault-Token: $root_token" \
  --request POST \
  --data '{"policies":["admin"], "ttl":"24h"}' \
  $OPENBAO_URL/v1/auth/token/create | jq -r '.auth.client_token')
echo "ADMIN_TOKEN=$ADMIN_TOKEN" >> /openbao/file/tokens.env

# Создаем токен пользователя
USER_TOKEN=$(curl -s --header "X-Vault-Token: $root_token" \
  --request POST \
  --data '{"policies":["user"], "ttl":"24h"}' \
  $OPENBAO_URL/v1/auth/token/create | jq -r '.auth.client_token')
echo "USER_TOKEN=$USER_TOKEN" >> /openbao/file/tokens.env
