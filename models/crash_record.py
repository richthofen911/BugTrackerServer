from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CrashRecord(Base):
    __tablename__ = "crash_log"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    timestamp = Column(String(50))
    appname = Column(String(50))
    username = Column(String(100))
    userappid = Column(String(100))
    deviceinfo = Column(String(100))
    message = Column(Text(65535))
    cause = Column(Text(65535))

    def __repr__(self):
        return "<CrashRecord(" \
               "timestamp='%s', " \
               "appname='%s', " \
               "username='%s', " \
               "userappid='%s', " \
               "deviceinfo='%s', " \
               "message='%s', " \
               "cause='%s'" \
               ")>" % \
               (self.timestamp, self.appname, self.username, self.userappid, self.deviceinfo, self.message, self.cause)





