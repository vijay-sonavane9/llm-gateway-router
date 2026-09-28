from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from src.config import DB_PATH

# This automatically creates a metrics.db file in your project folder
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LogEntry(Base):
    __tablename__ = "routing_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tier = Column(Integer)
    model_used = Column(String)
    routing_latency_ms = Column(Float)

# Create tables instantly if they don't exist
Base.metadata.create_all(bind=engine)

def log_request(tier: int, model_used: str, latency: float):
    db = SessionLocal()
    try:
        log = LogEntry(tier=tier, model_used=model_used, routing_latency_ms=latency)
        db.add(log)
        db.commit()
    except Exception:
        pass # Never crash the main app if logging fails
    finally:
        db.close()