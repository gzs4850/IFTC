from datetime import datetime
from . import db
from app.exceptions import ValidationError


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    desc = db.Column(db.Text)
    status = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    systems = db.relationship('System', backref='project')
    interfaces = db.relationship('Interface', backref='project')

    def to_json(self):
        json_project = {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'status': self.status,
            'timestamp': self.timestamp
        }
        return json_project

    @staticmethod
    def from_json(json_project):
        name = json_project.get('name')
        desc = json_project.get('desc')
        if name is None or name == '':
            raise ValidationError('name is null')
        return Project(name=name, desc=desc)


class System(db.Model):
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.Text)
    status = db.Column(db.Boolean)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    interfaces = db.relationship('Interface', backref='system')

    def to_json(self):
        json_system = {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'status': self.status,
            'project_id': self.project_id,
            'timestamp': self.timestamp
        }
        return json_system

    @staticmethod
    def from_json(json_system):
        name = json_system.get('name')
        desc = json_system.get('desc')
        project_id = json_system.get('project_id')
        if name is None or name == '':
            raise ValidationError('name is null')
        if project_id is None or project_id == '':
            raise ValidationError('project is null')
        return System(name=name, desc=desc, project_id=project_id)


class Interface(db.Model):
    __tablename__ = 'interfaces'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    desc = db.Column(db.Text)
    method = db.Column(db.String(32))
    protocol = db.Column(db.String(32))
    url = db.Column(db.String(128))
    autotest = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    testcases = db.relationship('Testcase', backref='interface')

    def to_json(self):
        json_interface = {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'method': self.method,
            'protocol': self.protocol,
            'url': self.url,
            'autotest': self.autotest,
            'status': self.status,
            'timestamp': self.timestamp,
            'system_id': self.system_id,
            'project_id': self.project_id
        }
        return json_interface

    @staticmethod
    def from_json(json_interface):
        name = json_interface.get('name')
        desc = json_interface.get('desc')
        protocol = json_interface.get('protocol')
        method = json_interface.get('method')
        url = json_interface.get('url')
        autotest = json_interface.get('autotest')
        system_id = json_interface.get('system_id')
        project_id = json_interface.get('project_id')
        if name is None or name == '':
            raise ValidationError('name is null')
        if project_id is None or project_id == '':
            raise ValidationError('project_id is null')
        if system_id is None or system_id == '':
            raise ValidationError('system_id is null')
        if url is None or url == '':
            raise ValidationError('url is null')
        return Interface(name=name, desc=desc, protocol=protocol, method=method, url=url,
                         autotest=autotest, system_id=system_id, project_id=project_id)


class Testcase(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    interface_id = db.Column(db.Integer, db.ForeignKey('interfaces.id'))
    request_json = db.Column(db.Text)
    request_head = db.Column(db.Text)
    request_path = db.Column(db.String(128))
    response_json = db.Column(db.Text)
    response_head = db.Column(db.Text)
    check_json = db.Column(db.Text)
    ref_json = db.Column(db.Text)
    is_case = db.Column(db.Boolean, default=1)
    status = db.Column(db.Boolean, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_json(self):
        json_testcase = {
            'id': self.id,
            'name': self.name,
            'interface_id': self.interface_id,
            'request_json': self.request_json,
            'request_head': self.request_head,
            'request_path': self.request_path,
            'response_json': self.response_json,
            'response_head': self.response_head,
            'check_json': self.check_json,
            'ref_json': self.ref_json,
            'is_case': self.is_case,
            'status': self.status,
            'timestamp': self.timestamp
        }
        return json_testcase

    @staticmethod
    def from_json(json_testcase):
        name = json_testcase.get('name')
        interface_id = json_testcase.get('interface_id')
        request_json = json_testcase.get('request_json')
        request_head = json_testcase.get('request_head')
        request_path = json_testcase.get('request_path')
        response_json = json_testcase.get('response_json')
        response_head = json_testcase.get('response_head')
        check_json = json_testcase.get('check_json')
        ref_json = json_testcase.get('ref_json')
        if name is None or name == '':
            raise ValidationError('name is null')
        return Testcase(name=name, interface_id=interface_id, request_json=request_json, request_head=request_head,
                   request_path=request_path, response_json=response_json, response_head=response_head,
                   check_json=check_json, ref_json=ref_json)