.PHONY .SILENT:
run:
	docker pull postgres
	docker run --name my-postgres -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root -e POSTGRES_DB=library_db -d -p 5432:5432 postgres
	pipenv --python 3.13
	pipenv install -r requirements.txt
	pipenv run alembic upgrade head
	pipenv run uvicorn app.main:app --port 8080
