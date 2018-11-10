import sqlite3 as sql

DB_PATH = 'tables.db'

class Statistics:
    @staticmethod
    def get_events(resident_id):
        return [i for i in conn.execute(f'select * from events_event where resident_id = {resident_id}')]

    def get_rating(self, event_id):
        return [i for i in conn.\
            execute(f'select avg(rating) from users_events where events_id = {event_id} group by events_id')][0][0]

    def get_comments(self, event_id):
        return [i for i in conn.execute(f'select rating, comment from users_events where events_id = {event_id}')]

    def get_attendants(self, event_id):
        return [i for i in conn.\
            execute(f'select count(1) from users_events where events_id = {event_id} group by events_id')][0][0]

    def get_metrics(self, _id):
        temp = dict()
        temp['rating'] = self.get_rating(_id)
        temp['attendants'] = self.get_attendants(_id)
        temp['comments'] = self.get_comments(_id)
        return temp





