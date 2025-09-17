include .env
export $(shell sed 's/=.*//' .env)

run: 
	fastapi dev api/main.py --port ${PORT}

run-db: 
	docker compose up -d 