import io

from flask import Flask, render_template, request, redirect, abort, flash, make_response, url_for
from models import db, AttendeeModel
from datetime import datetime
import csv

app = Flask(__name__)
# Using a development configuration
app.config.from_object('config.DevConfig')
app.secret_key = 'super secret'
db.init_app(app)

global config
config = app.config

@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def initialLoad():
    attendees = AttendeeModel.query.all()
    totalAttendees = len(attendees)
    return render_template('home.html', totalAttendees=totalAttendees)


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
    if request.method == 'POST':
        registrationDate = datetime.now()
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        company = request.form['company']
        attendee = AttendeeModel(registrationDate=registrationDate, firstName=firstName, lastName=lastName, email=email,
                                 company=company)
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
    return f"Attendee with id = {id} was not found."


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    attendee = AttendeeModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if attendee:
            db.session.delete(attendee)
            db.session.commit()
            registrationDate = attendee.registrationDate
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']
            company = request.form['company']
            attendee = AttendeeModel(registrationDate=registrationDate, firstName=firstName, lastName=lastName,
                                     email=email, company=company)
            attendee.id = id
            db.session.add(attendee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Attendee with id = {id} was not found."

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

    return render_template('delete.html', id=attendee.id)


@app.route('/data/export', methods=['GET', 'POST'])
def export():
    time = datetime.now().strftime("%Y-%m-%d-")
    fileName = time + 'attendees'
    con = db.session

    try:
        # downloads exported file locally
        cursor = con.execute("select * from 'table'")
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerows(cursor.fetchall())
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=" + \
            fileName + ".csv"
        output.headers["Content-type"] = "text/csv"
    except Exception as e:
        flash("Couldn't open or write to file (%s)." % e, 'warning')
        return redirect('/data')

    return output
