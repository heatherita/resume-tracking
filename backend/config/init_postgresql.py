from pathlib import Path
import sys

# Allow running this file directly from project root or other working dirs.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from database import Base, engine
from models import models  # noqa: F401 - ensures model tables are registered on Base.metadata



# usage:
# docker exec -it answerbank-backend python /backend/config/init_postgresql.py



if not Base.metadata.tables:
    raise RuntimeError("No tables found in Base.metadata. Ensure models are imported before create_all().")

Base.metadata.create_all(bind=engine)
print(f"Initialized tables: {', '.join(sorted(Base.metadata.tables.keys()))}")
