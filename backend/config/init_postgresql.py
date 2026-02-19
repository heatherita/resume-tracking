from database import Base, engine, get_db



#usage: from host shell run:
#docker exec -it answerbank-backend python /backend/config/init_postgres.py



Base.metadata.create_all(bind=engine)
