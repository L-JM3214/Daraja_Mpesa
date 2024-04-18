from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def __repr__(self):
        return f"Phone number: {self.number}"