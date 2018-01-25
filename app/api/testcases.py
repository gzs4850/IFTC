# coding:utf-8
from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Testcase
from . import api

@api.route('/testcases/')
def get_testcases():
    page = request.args.get('page', 1, type=int)
    pagination = Testcase.query.filter_by(status=1).paginate(
        page, per_page=current_app.config['FLASKY_PER_PAGE'],
        error_out=False)
    testcases = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_projects', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_projects', page=page+1)
    return jsonify({
        'code': 1,
        'testcases': [testcase.to_json() for testcase in testcases],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/testcases/<int:id>')
def get_testcase(id):
    testcase = Testcase.query.get_or_404(id)
    return jsonify({
        'code': 1,
        'testcase': testcase.to_json()
    })

@api.route('/testcases/', methods=['POST'])
def new_testcase():
    testcase = Testcase.from_json(request.json)
    db.session.add(testcase)
    db.session.commit()
    return jsonify({
        'code': 1,
        'testcase': testcase.to_json()
    })

@api.route('/testcases/<int:id>', methods=['PUT'])
def edit_testcase(id):
    testcase = Testcase.query.get_or_404(id)
    testcase.name = request.json.get('name', testcase.name)
    testcase.interface_id = request.json.get('interface_id', testcase.interface_id)
    testcase.request_json = request.json.get('request_json', testcase.request_json)
    testcase.request_head = request.json.get('request_head', testcase.request_head)
    testcase.request_path = request.json.get('request_path', testcase.request_path)
    testcase.response_json = request.json.get('response_json', testcase.response_json)
    testcase.response_head = request.json.get('response_head', testcase.response_head)
    testcase.check_json = request.json.get('check_json', testcase.check_json)
    testcase.ref_json = request.json.get('ref_json', testcase.ref_json)
    db.session.add(testcase)
    db.session.commit()
    return jsonify({
        'code': 1,
        'testcase': testcase.to_json()
    })

@api.route('/testcases/<int:id>', methods=['DELETE'])
def delete_testcase(id):
    testcase = Testcase.query.get_or_404(id)
    testcase.status = 0
    db.session.add(testcase)
    db.session.commit()
    return jsonify({'code': 1, 'message': '删除成功'})