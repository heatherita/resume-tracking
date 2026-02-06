# --- Database convenience commands -----------------------------------------

DB_CONTAINER = fastapi_postgres
DB_USER      = fastapi_user
DB_NAME      = fastapi_db

psql:
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

db-shell: psql

db-dump:
	docker exec -t $(DB_CONTAINER) pg_dump -U $(DB_USER) $(DB_NAME) > db_dump.sql

db-restore:
	cat db_dump.sql | docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

db-tables:
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "\dt"

db-reset:
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
