
import web
import MySQLdb
import datetime
import time

db = web.database(dbn='mysql', user='root', pw='qwer1234', db='crash_tracker')
urls = (
    '/log/(.+)', 'log',
    '/report', 'report'
)

class log:
    def GET(self, params):
        query_statement = 'select * from crash_log'
        where = ';'
        isLegal = True
        if params != 'all':
            condition = params.split('/')
            if len(condition) == 2:
                if condition[0] == 'timestamp':
                    where = " where Timestamp = '" + condition[1] + "' "  + where
                elif condition[0] == 'appname':
                    where = " where AppName = '" + condition[1] + "' "  + where
                elif condition[0] == 'username':
                    where = " where Username = '" + condition[1] + "' "  + where
                elif condition[0] == 'userappid':
                    where = " where UserAppId = '" + condition[1] + "' "  + where
                else:
                    isLegal = False
                    where = 'Illegal Key: ' + condition[0] + '\nLegal Keys: timestamp, username, userobjectid'
            else:
                isLegal = False
                where = 'Illegal parameter form, expected parameter form: /condition/key'
            if isLegal == False:
                return where
        
        query_statement = query_statement + where
        print 'query_statement: ' + query_statement
        render = web.template.render('templates/')
        entries = db.query(query_statement)
        if len(entries) == 0:
            return 'no record(s) found'
        else:
            return render.index(entries)

    
class report:
    def POST(self):
        i = web.input()
        appname = i.appname
        username = i.username
        user_app_id = i.userappid
        device_info = i.deviceinfo
        cause = i.cause
        time_formatted = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        db.insert('crash_log', Timestamp=time_formatted, AppName=appname, Username=username, UserAppId=user_app_id, DeviceInfo = device_info, Cause=cause)
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

