import datetime
from flaskr.utils.db_conn import db
from sqlalchemy import DateTime, Integer, String, Float
import os


class Expenses(db.Model):
    id = db.Column("id", Integer, primary_key=True)
    amount_spent = db.Column("amount_spent", Float, nullable=False)
    day = db.Column("day", String(10), nullable=False)
    category = db.Column("category", String(50), nullable=False)
    description = db.Column("description", String(255), nullable=False)
    payment_method = db.Column("payment_method", String(50), nullable=False)
    posting_date = db.Column("posting_date", DateTime,
                             default=datetime.date.today, nullable=False)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))

    @classmethod
    def delete(cls, id: Integer):
        try:
            expense = Expenses.get_by_id(id)

            db.session.delete(expense)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def add(cls, amount_spent: float, day: str, category: str, description: str, payment_method: str, posting_date: datetime.date, user_id: int):
        try:
            new_expense = Expenses(amount_spent=amount_spent, day=day, category=category,
                                   description=description, payment_method=payment_method, posting_date=posting_date, user_id=user_id)
            db.session.add(new_expense)
            db.session.commit()
            return new_expense
        except Exception as e:
            print(f"Database error... {e}")
            return False

    @classmethod
    def get_by_id(cls, id: Integer):
        expense = Expenses.query.get(id)
        return expense

    @classmethod
    def get_by_day(cls, day: str, user_id: Integer) -> list:
        expense = Expenses.query.filter_by(day=day, user_id=user_id).all()
        return expense

    @classmethod
    def get_by_category(cls, category: str, user_id: Integer) -> list:
        expense = Expenses.query.filter_by(
            category=category, user_id=user_id).all()
        return expense

    @classmethod
    def get_by_payment_method(cls, payment_method: str, user_id: Integer) -> list:
        expense = Expenses.query.filter_by(
            payment_method=payment_method, user_id=user_id).all()
        return expense

    @classmethod
    def get_by_posting_date(cls, posting_date: datetime.date, user_id: Integer) -> list:
        expense = Expenses.query.filter_by(
            posting_date=posting_date, user_id=user_id).all()
        return expense
