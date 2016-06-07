from flask import Flask, request, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
import time

from models.crash_record import Base, CrashRecord

app = Flask(__name__)

db_engine = create_engine('mysql://root:qwer1234@localhost/my_util_services')
Base.metadata.create_all(db_engine, checkfirst=True)

db_session = sessionmaker(bind=db_engine)
my_db_session = db_session()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # check login info
        # then redirect to dashboard page
    elif request.method == 'GET':
        return render_template('sign_in.html')


@app.route('/dashboard', methods=['GET'])
def show_dashboard():
    return render_template('dashboard.html')


@app.route('/crashtracker/show/<path:query_filter>', methods=['GET'])
def show_crash_report(query_filter):
    key_value_pair = query_filter.split('/')
    if len(key_value_pair) <= 2:
        key = key_value_pair[0]
        if key == 'all':
            result = my_db_session.query(CrashRecord).order_by(CrashRecord.id)
        else:
            attr = getattr(CrashRecord, key_value_pair[0], None)
            if attr is None:
                return key_value_pair[0] + " is not a column"
            else:
                result = my_db_session.query(CrashRecord).filter(attr == key_value_pair[1])
        if result.count() == 0:
            return 'no record found'
        elif key == 'id':
            return render_template('crash_record_detail.html', record=result)
        else:
            return render_template('crash_report.html', entries=result)

    else:
        return 'illegal argument numbers, need to be /crashtracker/show/all or /crashtracker/show/key/value'


@app.route('/crashtracker/report', methods=['POST'])
def report_bug():
    time_formatted = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    crash_record = CrashRecord(
        timestamp=time_formatted,
        appname=request.form.get('appname'),
        username=request.form.get('username'),
        userappid=request.form.get('userappid'),
        deviceinfo=request.form.get('deviceinfo'),
        message=request.form.get('message'),
        cause=request.form.get('cause')
    )
    my_db_session.add(crash_record)
    my_db_session.flush()
    my_db_session.commit()
    return 'success'


if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.128.57', port=3999)


