from database import db


class Tracker(db.Model):
    __tablename__ = 'tracker'
    sr_number=db.Column('SrNumber',db.Integer,primary_key=True,autoincrement=True)
    trackerid = db.Column('TrackerID', db.Integer, nullable=False)
    userid = db.Column('UserID', db.Integer, nullable=False)
    last_tracked = db.Column('LastTracked', db.String)




class TrackerList(db.Model):
    __tablename__ = "trackerlist"
    tid = db.Column("TrackerID", db.Integer, autoincrement=True, primary_key=True)
    tracker_name=db.Column("TrackerName",db.String,nullable=False)
    trackerdescription = db.Column("TrackerDescription", db.String, nullable=False)
    trackertype=db.Column("TrackerType",db.String,nullable=False)
    mcqvalue=db.Column("MCQValue",db.String)

class User(db.Model):

    __table__name = "user"
    userid = db.Column("UserID", db.Integer, autoincrement=True, primary_key=True)
    useremail = db.Column("UserEmail", db.String,nullable=False,unique=True)
    userpass = db.Column("Password", db.String,nullable=False)


