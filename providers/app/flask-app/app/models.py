from app import db
from datetime import datetime

class Provider(db.Model):
    __tablename__ = 'Provider'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    trucks = db.relationship('Truck', backref='truck_provider', lazy='dynamic')
    rates = db.relationship('Rate', backref='scope_provider', lazy='dynamic')
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
        }
    def __repr__(self):
        return '<Provider {}>'.format(self.id)

class Rate(db.Model):
    __tablename__ = 'Rates'
    product_id = db.Column(db.String(50), primary_key=True)
    rate = db.Column(db.Integer)
    scope = db.Column(db.String(50), db.ForeignKey('Provider.id'))
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'product_id': self.product_id,
            'rate': self.rate,
            'scope': self.scope,
        }
    def __repr__(self):
        return '<Rate {}>'.format(self.rate)

class Truck(db.Model):
    __tablename__ = 'Trucks'
    id = db.Column(db.String(10), primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('Provider.id'))
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'         : self.id,
           'provider_id': self.provider_id,
       }
    def __repr__(self):
        return '<Truck {}>'.format(self.id)
