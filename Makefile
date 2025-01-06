dev:
	python src/main.py

test:
	pytest -p no:warnings

migrate:
	alembic upgrade head

docker-up:
	docker-compose up -d --build
