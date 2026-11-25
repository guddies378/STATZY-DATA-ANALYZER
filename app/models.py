from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.sql import func
from app.database.connection import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    filename = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class DataRecord(Base):
    __tablename__ = "data_records"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(
        Integer, 
        ForeignKey("datasets.id"), 
        nullable=False
    )
    record_data = Column(JSON, nullable=False)
