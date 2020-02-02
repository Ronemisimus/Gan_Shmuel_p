from app import db
from datetime import datetime

class Provider(db.Model):
    __tablename__ = 'Provider'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    def __repr__(self):
        return '<Provider {}>'.format(self.id)

class Rate(db.Model):
    __tablename__ = 'Rates'
    product_id = db.Column(db.String(50), primary_key=True)
    rate = db.Column(db.Integer)
    scope = db.Column(db.String(50))
    def __repr__(self):
        return '<Rate {}>'.format(self.rate)

class Truck(db.Model):
    __tablename__ = 'Trucks'
    id = db.Column(db.String(10), primary_key=True)
    provider_id = db.Column(db.Integer)
    def __repr__(self):
        return '<Truck {}>'.format(self.id)
