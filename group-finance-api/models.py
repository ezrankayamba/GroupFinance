from flask_sqlalchemy import SQLAlchemy
import json
from functools import singledispatch
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()


@singledispatch
def model_to_dict(val):
    """Used by default."""
    return str(val)


@model_to_dict.register(db.Model)
def ts_model(val):
    return val.to_dict()


class Group(db.Model):
    __tablename__ = 'tbl_group'
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Group: {}/>'.format(self.name)


class GroupSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_by', 'name')


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)


class Member(db.Model):
    __tablename__ = 'tbl_member'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Member: {}/>'.format(self.name)


class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'group_id', 'name')


member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
