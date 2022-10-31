from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MatrixParams(Base):
    __tablename__ = 'matrix_params'

    id = Column(String(64), primary_key=True)
    student_id = Column(ForeignKey('students.id'))
    size = Column(Integer)
    matrix_limit = Column(Integer)
    seeds = Column(Text)

    student = relationship('Students')


class Students(Base):
    __tablename__ = 'students'

    id = Column(String(64), primary_key=True)
    student_name_group = Column(String(512))