.PHONY .SILENT:
run:
	docker compose up --build -d
	docker compose exec library alembic upgrade head
