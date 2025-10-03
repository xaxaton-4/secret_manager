#!/bin/bash
sudo apt update && sudo apt install -y curl

sudo docker compose up --build -d

# Ждём пока OpenBao запустится
echo "Waiting for OpenBao to start..."
sleep 5  # или проверять curl в цикле

# Проверяем, инициализирован ли Vault
INIT_CHECK=$(curl -s http://localhost:8200/v1/sys/health | grep '"initialized":true')

if [ -z "$INIT_CHECK" ]; then
  echo "Initializing OpenBao..."
  # Сохраняем вывод инициализации в переменную
  INIT_OUTPUT=$(curl -s -X POST http://localhost:8200/v1/sys/init -d '{
    "secret_shares": 1,
    "secret_threshold": 1
  }')

  # Сохраняем root_token в файл
  echo "$INIT_OUTPUT" > .bao_token
  echo "OpenBao initialized! Token saved to .bao_token"
else
  echo "OpenBao already initialized, skipping init."
fi
