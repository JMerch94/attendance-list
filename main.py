from flask import Flask, render_template, request, redirect, abort
from models import db, AttendeeModel
from datetime import datetime

app = Flask(__name__)
# Using a development configuration
app.config.from_object('config.DevConfig')
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()



@app.route('/')
def initialLoad():
    return render_template('home.html')

@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        registrationDate = datetime.now()
        name = request.form['name']
        company = request.form['company']
        attendee = AttendeeModel(registrationDate=registrationDate, name=name, company=company)
        db.session.add(attendee)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def RetrieveDataList():
    attendees = AttendeeModel.query.all()
    return render_template('datalist.html', attendees=attendees)


@app.route('/data/<int:id>')
def RetrieveSingleAttendee(id):
    attendee = AttendeeModel.query.filter_by(id=id).first()
    if attendee:
        return render_template('data.html', attendee=attendee)
    return f"Attendee with id ={id} Doenst exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    attendee = AttendeeModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if attendee:
            db.session.delete(attendee)
            db.session.commit()
            registrationDate = attendee.registrationDate
            name = request.form['name']
            company = request.form['company']
            attendee = AttendeeModel(registrationDate=registrationDate, name=name, company=company)

            db.session.add(attendee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist"

    return render_template('update.html', attendee=attendee)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    attendee = AttendeeModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if attendee:
            db.session.delete(attendee)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')
