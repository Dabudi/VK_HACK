import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import sqlite3 as sql
import pickle
from app.nlpModel.utils import vectorize
from app.users.models import User, Event, UserEvnet
from app import   DB_PATH
import pandas as pd


class Recommender:
    def __init__(self, model):
        #self.engine = sql.create_engine('sqlite:////' + DB_PATH)
        #self.conn = self.engine.connect()
        self.model = model

    def user_recommend(self, user_id):
        #Исправить на норм взаимодействие с бд
        user = np.array(User.query.filter_by(vk_id=user_id).first().target)#pd.read_sql(f'select <vector> from users where id = {user_id}', self.engine).values
        distances = self.sorted_distances(user)
        conn = sql.connect(DB_PATH)

        ids = [i for i in conn.execute('SELECT id FROM events_event')]#np.array(Event.id)#np.array(pd.read_sql('select id from events'), self.engine)
        ordered = []
        for idx in distances[0]:
            ordered.append(ids[idx])
        return ordered

    def event_recommend(self, new_event):
        ids = np.array(Event.id) #np.array(pd.read_sql('select id from events'))
        distances = self.sorted_distances(new_event)
        return ids[distances[0]]

    def sorted_distances(self, vector):
        conn = sql.connect(DB_PATH)
        events = [pickle.loads(i[0]) for i in conn.execute('SELECT vector FROM events_event')]
        return np.argsort(cosine_distances([vector], events))

class Processor:
    def __init__(self, model):
        self.model = model
    #    self.data = data

    def user_processing(self, data):
        groups = []
        for group in data[:-1]:
            print('>'*50)
            print(group)
            name = vectorize(self.model, group['name'])
            description = vectorize(self.model, group['description'])
            posts = np.mean(list(map(lambda x: vectorize(model=self.model, text=x), group['wall'])), axis=0)
            groups.append(np.mean([name, description, posts], axis=0))
        return np.mean(groups, axis=0)

    def event_processing(self, data):
        if isinstance(data, list):
            events = []
            for event in data:
                name = vectorize(self.model, event['name'])
                description = vectorize(self.model, event['description'])
                events.append(np.mean([name, description], axis=0))
            return np.mean(events, axis=0)
        else:
            print('%'*50)
            print(data)
            name = vectorize(self.model, data['name'])
            description = vectorize(self.model, data['description'])
            return np.mean([name, description], axis=0)

    #def process(self):
    #    try:
    #        return self.user_processing(self.data)
    #    except Exception:
    #        return self.event_processing(self.data)