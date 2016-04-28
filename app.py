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
def hello_world():
    return 'Hello World!'


@app.route('/crashtracker/show/<path:query_filter>', methods=['GET'])
def show_crash_report(query_filter):
    key_value_pair = query_filter.split('/')
    if len(key_value_pair) <= 2:
        if key_value_pair[0] == 'all':
            result = my_db_session.query(CrashRecord).order_by(CrashRecord.id)
        else:
            result = my_db_session.query(CrashRecord).filter(getattr(CrashRecord, key_value_pair[0]) == key_value_pair[1])
        if result.count() == 0:
            return 'no record found'
        else:
            # Flask use jinja2 as the default html template language
            if key_value_pair[0] == 'id':
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


