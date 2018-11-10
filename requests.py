import sqlite3 as sql
from models import *
from statistics import Statistics
from model import Recommender, Processor

DB_PATH = 'tables.db'

def get_favourites(user_id):
    conn = sql.connect(DB_PATH)
    return [i for i in conn.\
        execute(f'select e.* from events_event e join users_events u on e.id = u.events_id where user_id = {user_id}')]

def favourite(user_id, event_id, session):
    row = UserEvnet(user_id=user_id, events_id=event_id)
    session.add(row)
    session.commit()

def similar_event(data, model):
    rec = Recommender(model)
    processor = Processor(data, model)
    vector = processor.process()
    closest_event = rec.event_recommend(vector)
    return Statistics.get_metrics(closest_event)
