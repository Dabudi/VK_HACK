import sqlalchemy as sql

session = #здесь должна быть сессия

def get_events(resident_id):
    return session.query(Event).filter_by(ResidentId=resident_id).all()

def get_rating(event_id):
    return session.query(Attendate.EventId, Attendance.Rating ,sql.func.count(Attendance.Rating)).\
        filter_by(EventId=event_id).group_by(Attendance.Rating, Attendance.EventId).all()

def get_comments(event_id):
    return session.query(Attendance.EventId, Attendance.Rating, Attendance.Comment).filter_by(EventId=event_id).all()

def get_attendants(event_id):
    return session.query(Attendance.EventId, sql.func.count(*)).\
        filter_by(EventId=event_id).group_by(Attendance.EventId).first()


session.query(User).filter_by(Role='user').all()
session.query(User).filter_by(Role='resident').all()