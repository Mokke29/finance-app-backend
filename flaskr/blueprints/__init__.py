from flaskr.controller.controller import route as security_route
from flaskr.controller.user import route as user_route
from flaskr.controller.expense import route as expense_route


def init_blueprints(app):
    with app.app_context():
        app.register_blueprint(security_route)
        app.register_blueprint(user_route)
        app.register_blueprint(expense_route)
