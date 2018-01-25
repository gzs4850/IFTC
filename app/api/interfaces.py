# coding:utf-8
from flask import jsonify, request, url_for, current_app
from .. import db
from ..models import Interface
from . import api

@api.route('/interfaces/')
def get_interfaces():
    page = request.args.get('page', 1, type=int)
    pagination = Interface.query.filter_by(status=1).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    interfaces = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_interfaces', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_interfaces', page=page+1)
    return jsonify({
        'code': 1,
        'interfaces': [interface.to_json() for interface in interfaces],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/interfaces/<int:id>')
def get_interface(id):
    interface = Interface.query.get_or_404(id)
    return jsonify({
        'code': 1,
        'interface': interface.to_json()
    })

@api.route('/interfaces/', methods=['POST'])
def new_interface():
    interface = Interface.from_json(request.json)
    interface.status = 1
    db.session.add(interface)
    db.session.commit()
    return jsonify({
        'code': 1,
        'interface': interface.to_json()
})

@api.route('/interfaces/<int:id>', methods=['PUT'])
def edit_interface(id):
    interface = Interface.query.get_or_404(id)
    interface.name = request.json.get('name', interface.name)
    interface.desc = request.json.get('desc', interface.desc)
    interface.system_id = request.json.get('system_id', interface.system_id)
    interface.project_id = request.json.get('project_id', interface.project_id)
    interface.protocol = request.json.get('protocol', interface.protocol)
    interface.method = request.json.get('method', interface.method)
    interface.url = request.json.get('url', interface.url)
    interface.autotest = request.json.get('autotest', interface.autotest)
    db.session.add(interface)
    db.session.commit()
    return jsonify({
        'code': 1,
        'interface': interface.to_json()
    })

@api.route('/interfaces/<int:id>', methods=['DELETE'])
def delete_interface(id):
    interface = Interface.query.get_or_404(id)
    interface.status = 0
    db.session.add(interface)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})