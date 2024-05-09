import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
# from flask import current_app as app 

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
db = SQLAlchemy()
# from werkzeug.local import LocalProxy

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
# db = LocalProxy(setup_db)


def create_db_with_data():
    db.drop_all()
    db.create_all()
    food = Food(
        title='Crispy Salt and Pepper Potatoes',
        ingredient='2 large egg whites, 1 pound new potatoes (about 1 inch in diameter), 2 teaspoons kosher salt'
    )
    food.insert()
    food_2 = Food(
        title='Crispy Salt and Pepper Potatoes 1',
        ingredient='2 large egg whites, 1 pound new potatoes (about 1 inch in diameter), 2 teaspoons kosher salt 1'
    )
    food_2.insert()


class Food(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)
    ingredient = Column(String(180), nullable=False)

    def just_title(self):
        return {
            'id': self.id,
            'title': self.title
        }

    def full_version(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredient': self.ingredient
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
