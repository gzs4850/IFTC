# coding:utf-8
from flask import jsonify
from ..models import Testresult
from . import api


@api.route('/testresults/<int:id>')
def get_testresult(id):
    testresult = Testresult.query.get_or_404(id)

    return jsonify({
        'code': 1,
        'testresult': testresult.to_json()
    })