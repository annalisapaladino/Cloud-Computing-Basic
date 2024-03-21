# Cloud-Computing-Basic

1. Install Docker and Docker-Compose
2. Start the containers
```bash
docker-compose up -d
```
3. Launch the [`UserCreate.sh`](UserCreate.sh) file to set up the working environment
```bash
sh UserCreate.sh
```
4. Perform tests on Locust going to http://localhost:8080, but first 
```bash
locust -f locustfile.py
```
