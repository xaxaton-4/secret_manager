#!/bin/sh
set -e

OPENBAO_URL=${OPENBAO_URL:-http://openbao:8200}
BAO_FILE=${BAO_FILE:-/openbao/file/.bao_token}

echo "Waiting for OpenBao to start..."
until curl -s $OPENBAO_URL/v1/sys/health >/dev/null 2>&1; do
  echo "OpenBao not ready yet..."
  sleep 1
done

echo "OpenBao is up!"

status=$(curl -s $OPENBAO_URL/v1/sys/health | jq -r .initialized)

if [ "$status" = "false" ]; then
  echo "Initializing OpenBao..."
  keys=$(curl -s --request POST --data '{"secret_shares":1,"secret_threshold":1}' $OPENBAO_URL/v1/sys/init)
  unseal_key=$(echo $keys | jq -r '.keys[0]')
  echo "Unsealing OpenBao..."
  curl -s --request PUT --data "{\"key\":\"$unseal_key\"}" $OPENBAO_URL/v1/sys/unseal
  echo "$keys" > $BAO_FILE
  echo "OpenBao initialized and unsealed."
else
  echo "OpenBao already initialized."
fi
