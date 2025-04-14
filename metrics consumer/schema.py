from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    
    row_id = Column(Integer, primary_key=True, autoincrement=True) # surrogate key
    server_id = Column(Integer)
    cpu = Column(Integer)
    mem = Column(Integer)
    disk = Column(Integer)