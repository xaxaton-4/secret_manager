sudo apt update && sudo apt install curl
sudo docker compose up --build &
curl -X POST http://localhost:8200/v1/sys/init -d '{
  "secret_shares": 1,
  "secret_threshold": 1
}'
