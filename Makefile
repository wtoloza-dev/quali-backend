dev:
	uv run fastapi dev

db:
	colima start
	docker compose up db -d

migrate:
	uv run alembic upgrade head

migration:
	uv run alembic revision --autogenerate -m "$(m)"

stop:
	-lsof -ti :8000 | xargs kill -9
	docker compose stop db

down:
	-lsof -ti :8000 | xargs kill -9
	docker compose stop db
	colima stop
