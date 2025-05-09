from extensions import db
from datetime import datetime

class User(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(64), unique=True, nullable=False)
    full_name   = db.Column(db.String(120), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    remarks     = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    remarks     = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'<Project {self.name}>'

class Machine(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(256))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    remarks     = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'<Machine {self.name}>'

class Setup(db.Model):
    __tablename__ = 'setup'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(128), nullable=False)
    bemerkungen = db.Column(db.Text)

    # korrekte ForeignKeys auf deine englisch benannten Tabellen
    benutzer_id = db.Column(db.Integer, db.ForeignKey('user.id'),    nullable=False)
    projekt_id  = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    maschine_id = db.Column(db.Integer, db.ForeignKey('machine.id'), nullable=False)
    # Relationships auf die englischen Klassen
    benutzer = db.relationship('User',    backref='setups')
    projekt  = db.relationship('Project', backref='setups')
    maschine = db.relationship('Machine', backref='setups')

    def __repr__(self):
        return f'<Setup {self.name}>'
