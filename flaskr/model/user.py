from flaskr.utils.db_conn import db
from sqlalchemy import Integer, String
import os


class User(db.Model):
    id = db.Column("id", Integer, primary_key=True)
    username = db.Column("username", String(100), nullable=False)
    password = db.Column("password", String(100), nullable=False)
    expenses = db.relationship('Expenses', backref="user")

    @classmethod
    def delete(cls):
        try:
            user = User.get_by_id(cls.id)
            db.session.delete(user)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def create(cls, username, password):
        try:
            if User.query.filter_by(username=username).first():
                print(f"User already exists #{username}")
                return False
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                return new_user.username
        except Exception as e:
            print(f"Database error... {e}")
            return False

    @classmethod
    def get_by_id(cls, id):
        user = User.query.get(id)
        return user

    @classmethod
    def get_by_username(cls, username):
        user = User.query.filter_by(username=username).first()
        return user
