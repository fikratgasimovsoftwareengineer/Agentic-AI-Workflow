## Commando:
```sh
ngrok http 5678
```
```sh
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - TZ=Europe/Rome
      - N8N_RESTRICT_FILE_ACCESS_TO=/home/node/docs;/home/node/.n8n-files
      - WEBHOOK_URL=https://aim-gas-ambush.ngrok-free.dev
    volumes:
      - n8n_data:/home/node/.n8n  
      - ~/n8n_docs_test:/home/node/docs
    extra_hosts:
      - "host.docker.internal:host-gateway"

volumes:
  n8n_data:
```
