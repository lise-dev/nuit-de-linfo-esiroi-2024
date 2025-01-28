from . import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    student_number = db.Column(db.String(50), unique=True, nullable=False)
    school = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))  # Référence à une équipe

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('student.id'))  # Chef d'équipe
    leader = db.relationship('Student', foreign_keys=[leader_id], backref='led_team')
    members = db.relationship('Student', backref='team', foreign_keys='Student.team_id')
