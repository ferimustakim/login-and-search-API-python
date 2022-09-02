from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

import string
import random
db = SQLAlchemy()


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    referal_code = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    update_at = db.Column(db.DateTime, onupdate=datetime.now())
    #write here
    def __repr__(self) -> str:
        return 'User>>> {self.username}'

#untu boomark in here