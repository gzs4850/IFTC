from datetime import datetime
from . import db
from app.exceptions import ValidationError

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.Text)
    status = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    systems = db.relationship('System', backref='project')

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
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.Text)
    status = db.Column(db.Boolean)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

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