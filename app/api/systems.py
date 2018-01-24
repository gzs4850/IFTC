# coding:utf-8
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import System
from . import api

@api.route('/systems/')
def get_systems():
    page = request.args.get('page', 1, type=int)
    pagination = System.query.filter_by(status=1).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    systems = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_systems', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_systems', page=page+1)
    return jsonify({
        'code': 1,
        'systems': [system.to_json() for system in systems],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/systems/<int:id>')
def get_system(id):
    system = System.query.get_or_404(id)
    return jsonify({
        'code': 1,
        'system': system.to_json()
    })

@api.route('/systems/', methods=['POST'])
def new_system():
    system = System.from_json(request.json)
    system.status = 1
    exist_system = System.query.filter_by(name=system.name).first()
    if exist_system:
        return jsonify({'code':0, 'message': '该项目名称已存在'})
    db.session.add(system)
    db.session.commit()
    return jsonify({
        'code': 1,
        'system': system.to_json()
    })

@api.route('/systems/<int:id>', methods=['PUT'])
def edit_system(id):
    system = System.query.get_or_404(id)
    system.name = request.json.get('name', system.name)
    system.desc = request.json.get('desc', system.desc)
    system.desc = request.json.get('desc', system.project_id)
    db.session.add(system)
    db.session.commit()
    return jsonify({
        'code': 1,
        'system': system.to_json()
    })

@api.route('/systems/<int:id>', methods=['DELETE'])
def delete_system(id):
    system = System.query.get_or_404(id)
    system.status = 0
    db.session.add(system)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})