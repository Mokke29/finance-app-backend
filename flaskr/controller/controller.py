import datetime
from flask import Blueprint, jsonify
from flaskr.utils.db_conn import db
from flask_jwt_extended import jwt_required
from flaskr.model.expenses import Expenses
import csv
import pathlib
import os

route = Blueprint('simple_page', __name__)


@route.get("/api")
def main_page():
    print("Main page")
    return "main page"


@route.get("/fakedata")
def e_add():

    # new_expense = Expenses.add(amount_spent=5, day="Monday", category="Food",
    #                           description="Bar", payment_method="Debit card", posting_date=d, user_id=1)
    # new = Expenses.get_by_posting_date(d, 1)
    # print(new[0].delete(new[0].id))
    # print(new[1].delete(new[1].id))
    path = os.path.join(pathlib.Path().resolve(),
                        "flaskr\static\dataset.csv")
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)  # ignore header
        for row in reader:
            # 0: Converting date to datetime.date
            test_date = row[0].split("/")
            month: int = int(test_date[0])
            day: int = int(test_date[1])
            year: int = int("20"+test_date[2])
            d = datetime.date(year, month, day)
            # 1: day
            day_name = row[1]
            # 2: float amount_spent
            amount_spent = float(row[2])
            if (amount_spent > 0):
                # amount_spent = -abs(amount_spent)
                continue
            # 3: category
            category = row[3]
            # 4: description
            description = row[4]
            # 5: Converting Cards with bank name to general names..
            if (row[5] == "Chase Debit Card"):
                payment_method = row[5].replace(
                    "Chase Debit Card", "Debit Card")
            elif (row[5] == "American Express Credit Card"):
                payment_method = row[5].replace(
                    "American Express Credit Card", "Credit Card")
            elif (row[5] == "Discover Credit Card"):
                payment_method = row[5].replace(
                    "Discover Credit Card", "Credit Card")
            else:
                payment_method = row[5].replace("M&T Debit Card", "Debit Card")

            # Omit deposits..
            if (category == "Direct Deposit"):
                continue
            elif (category == "Wire Transfer"):
                continue
            elif (category == "Tuition"):
                continue
            else:
                if (category == "Uber/Lyft"):
                    category = "Transportation"
                new_expense = Expenses.add(amount_spent=amount_spent, day=day_name, category=category,
                                           description=description, payment_method=payment_method, posting_date=d, user_id=2)
            # print(amount_spent)

    return str(d)


# Initialize db

@route.get('/db')
def get_db():
    db.create_all()
    return jsonify("[database]: -> create_all")
