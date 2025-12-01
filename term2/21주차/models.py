from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class Question(Base):
    __tablename__ = 'question'  # 테이블 이름

    id = Column(Integer, primary_key=True)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
