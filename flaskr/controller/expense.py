from flask import Blueprint, request, jsonify, make_response
from flaskr.model.expenses import Expenses
from flaskr.model.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import re
import datetime

route = Blueprint("expense_route", __name__, static_folder="static")


@route.post('/e/add')
@jwt_required()
def add_new_expense():
    data: dict = request.get_json()
    user_id = get_jwt_identity()
#     : number;
#   category: string;
#   description: string;
#   payment_method: string;
#   date: string;
    print(data.get("amount_spent"))
    print(data.get("date"))
    print(type(data.get("date")))
    category_pattern = r'^Food$|^Bills$|^Entertainment$|^Groceries$|^Merchandise$|^Travel$|^Other$|^Transportation$|^Pharmacy$'
    if not re.match(category_pattern, data.get("category")):
        return (jsonify({"msg": "Bad request, category doesn't exist."}), 200)

    payment_method_pattern = r'^Cash$|^Credit Card$|^Debit Card$|^Mobile Payment$'
    if not re.match(payment_method_pattern, data.get("payment_method")):
        return (jsonify({"msg": "Bad request, payment method doesn't exist."}), 200)

    date = data.get("date").split("-")
    year: int = int(date[0])
    month: int = int(date[1])
    day: int = int(date[2])
    date_mod = datetime.date(year, month, day)
    exp = Expenses.add(amount_spent=-abs(float(data.get("amount_spent"))), day=date_mod.weekday(), category=data.get(
        "category"), description=data.get("description"), payment_method=data.get("payment_method"), posting_date=date_mod, user_id=user_id)

    response = jsonify({"msg": "Expense added successfully"}), 200

    return response


@route.post('/e/delete')
@jwt_required()
def delete_expense():
    data: dict = request.get_json()
    # Check if user has expense with this id
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    for i in range(0, len(user.expenses)):
        if (user.expenses[i].id == data.get("id")):
            user.expenses[i].delete(user.expenses[i].id)
    # user = User.get_by_id(user_id)
    # if user.delete():
    #    return jsonify('User deleted successfully!')
    # else:
    return jsonify('Something went wrong, please try again later...', 200)


@route.get('/e/recent')
@jwt_required()
def get_recent_expense():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    # data: dict = request.get_json()
    expenses = []
    if (len(user.expenses) > 6):
        for i in range(len(user.expenses) - 5, len(user.expenses)):
            exp = user.expenses[i]
            exp_data = {"id": exp.id, "amount_spent": abs(exp.amount_spent), "day": exp.day, "category": exp.category,
                        "description": exp.description, "payment_method": exp.payment_method, "posting_date": exp.posting_date.strftime('%Y/%m/%d')}
            expenses.append(exp_data)
    else:
        for i in range(0, len(user.expenses)):
            exp = user.expenses[i]
            exp_data = {"id": exp.id, "amount_spent": abs(exp.amount_spent), "day": exp.day, "category": exp.category,
                        "description": exp.description, "payment_method": exp.payment_method, "posting_date": exp.posting_date.strftime('%Y/%m/%d')}
            expenses.append(exp_data)

    response = make_response(
        {"err": False, "data": expenses}, 200)
    return response


@route.get('/e/todaysum')
@jwt_required()
def get_todays_expenses():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    # data: dict = request.get_json()
    expenses = []
    now = str(datetime.date.today())
    sum = 0

    for i in range(0, len(user.expenses)):
        exp = user.expenses[i]
        if (exp.posting_date.strftime('%Y-%m-%d') == now):
            sum += exp.amount_spent

    response = make_response(
        {"err": False, "data": sum}, 200)
    return response
