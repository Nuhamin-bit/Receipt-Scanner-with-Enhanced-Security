from sqlalchemy import create_engine, Column, Integer, Float, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///receipts.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    merchant = Column(String)
    date = Column(String)
    total = Column(Float)
    tax = Column(Float)
    items = Column(JSON)

Base.metadata.create_all(bind=engine)