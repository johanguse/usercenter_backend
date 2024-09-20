from sqlalchemy import Column, DateTime, Enum, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ModelStatus(Enum):
    TRAINING = 'training'
    COMPLETED = 'completed'
    FAILED = 'failed'


class TrainingData(Base):
    __tablename__ = 'training_data'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(ModelStatus), default=ModelStatus.TRAINING)
    created_at = Column(DateTime)
    # Add other relevant fields as needed
