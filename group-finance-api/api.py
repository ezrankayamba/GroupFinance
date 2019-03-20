from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_restful import Resource, Api
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'group-finance.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api = Api(app)


def load_resources():
    from resources import GroupResource, MemberResource
    api.add_resource(GroupResource, '/groups', '/groups/<int:group_id>')
    api.add_resource(MemberResource, '/members/<int:group_id>',
                     '/members/<int:group_id>/<int:member_id>')


def init_db(app):
    with app.app_context():
        from models import db
        db.init_app(app)
        db.create_all()


if __name__ == '__main__':
    CORS(app)
    init_db(app)
    load_resources()
    app.run(debug=True)
