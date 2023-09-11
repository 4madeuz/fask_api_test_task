from datetime import datetime
from sqlalchemy.orm import validates

from ... import db


class Note(db.Model):
    id = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('author'))

    @validates('description')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value


class Subject(db.Model):
    id = db.Column(db.String(50), primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(50), nullable=False)
