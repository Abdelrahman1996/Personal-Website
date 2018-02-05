import sqlite3   
from db import db

class ItemModel(db.Model): 
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(2000))
    image = db.Column(db.String(200))
    
    def __init__(self, name, description, image):
      self.name = name
      self.description = description
      self.image = image

    def json(self):
      return {'name': self.name, 'description': self.description, 'image': self.image}
    
    @staticmethod
    def find_by_name(name):
        #return itemModel object with name and content
        return ItemModel.query.filter_by(name=name).first()
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
   