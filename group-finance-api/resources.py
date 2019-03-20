from flask_restful import Resource
from models import db, Group, group_schema, groups_schema
from models import Member, member_schema, members_schema
from flask import request, jsonify
from utils import list_json
import json


class GroupResource(Resource):
    def __init__(self):
        self.user_id = request.headers.get('User-ID')

    def get(self, group_id=None):
        if group_id is None:
            groups = Group.query.filter_by(created_by=self.user_id).all()
            return jsonify(groups_schema.dump(groups).data)
        else:
            group = Group.query.filter_by(
                created_by=self.user_id, id=group_id).first()
            return jsonify(group_schema.dump(group).data)

    def delete(self, group_id=None):
        if group_id is None:
            return jsonify({'result': -1, 'message': 'Invalid group id'})
        else:
            m = Group.query.filter_by(id=group_id).first()
            db.session.delete(m)
            db.session.commit()
            return jsonify({'result': 0, 'message': 'Successfully deleted group'})

    def post(self, group_id=None):
        data = request.get_json()
        g = Group(created_by=self.user_id, name=data['name'])
        db.session.add(g)
        db.session.commit()
        return {'result': 0, 'message': 'Success', 'id': g.id}


class MemberResource(Resource):
    def __init__(self):
        self.user_id = request.headers.get('User-ID')

    def delete(self, group_id, member_id=None):
        if member_id is None or group_id is None:
            return jsonify({'result': -1, 'message': 'Invalid member or group id'})
        else:
            m = Member.query.filter_by(group_id=group_id, id=member_id).first()
            print(m)
            db.session.delete(m)
            db.session.commit()
            return jsonify({'result': 0, 'message': 'Successfully deleted member'})

    def get(self, group_id, member_id=None):
        if member_id is None:
            members = Member.query.filter_by(group_id=group_id).all()
            return jsonify(members_schema.dump(members).data)
        else:
            member = Member.query.filter_by(
                group_id=group_id, id=member_id).first()
            return jsonify(member_schema.dump(member).data)

    def post(self, group_id, member_id=None):
        data = request.get_json()
        m = Member(group_id=group_id, name=data['name'])
        db.session.add(m)
        db.session.commit()
        return {'result': 0, 'message': 'Success', 'id': m.id}
