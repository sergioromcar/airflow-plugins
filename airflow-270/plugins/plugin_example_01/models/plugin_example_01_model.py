from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  relationship
from flask_sqlalchemy.model import DefaultMeta
from airflow.utils.session import provide_session
from airflow.utils.log.logging_mixin import LoggingMixin


Base = declarative_base(metaclass=DefaultMeta)


class PluginExample01TelecomDataModel(Base, LoggingMixin):
    """
    Base class for model objects.
    """
    __table_args__ = {'schema': 'data'}
    __tablename__ = "telecom_data"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    phone_number = Column(String(20), nullable=True)
    call_duration = Column(Integer, nullable=True)
   
    def __repr__(self):
        return '<telecom_data "{id}">'.format(id=self.id)
    

class PluginExample01UsersModel(Base, LoggingMixin):
    """
    Base class for model objects.
    """
    __table_args__ = {'schema': 'data'}
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
   
    def __repr__(self):
        return '<Users "{id}">'.format(id=self.id)



    @classmethod
    @provide_session
    def delete(regs, session=None):
        if isinstance(regs, PluginExample01UsersModel):
            regs = [regs]
        for reg in regs:
            if not isinstance(reg, regs):
                raise TypeError(
                    'Expected Users; received {}'.format(PluginExample01UsersModel.__class__.__name__)
                )
            session.delete(reg)
        session.commit()

    @classmethod
    @provide_session
    def updateVal(regs, name, email, session=None):
        for reg in regs:
            session.query(PluginExample01UsersModel).filter(PluginExample01UsersModel.id==reg.id).update({PluginExample01UsersModel.name : name, PluginExample01UsersModel.email: email})
        session.commit()

