
    Place docker-compose.yml and .env in your project root
    Place Dockerfile.backend in your project root (same level as main.py)
    Place frontend/Dockerfile in your frontend directory
    Run:
    bash

    docker-compose up -d

This will:

    Start PostgreSQL on port 5432
    Start FastAPI on port 8000
    Start React on port 3000
    Create volumes for persistent database data

To stop: docker-compose down To view logs: docker-compose logs -f [service_name]

create db tables: 
docker-compose exec backend python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"