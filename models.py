from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AttendeeModel(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    registrationDate = db.Column(db.DateTime())
    firstName = db.Column(db.String())
    lastName = db.Column(db.String())
    email = db.Column(db.String())
    company = db.Column(db.String(80))

    def __init__(self, registrationDate, firstName, lastName, email, company):
        self.registrationDate = registrationDate
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.company = company

    def __repr__(self):
        return f"{self.firstName} {self.lastName}: {self.registrationDate}"
