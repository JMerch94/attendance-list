from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AttendeeModel(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    registrationDate = db.Column(db.DateTime())
    name = db.Column(db.String())
    company = db.Column(db.String(80))

    def __init__(self, registrationDate, name, company):
        self.registrationDate = registrationDate
        self.name = name
        self.company = company

    def __repr__(self):
        return f"{self.name}: {self.registrationDate}"
