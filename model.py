import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import sqlalchemy as sql
from utils import vectorize
import pandas as pd

DB_PATH = ''

class Recommender:
    def __init__(self, model):
        self.engine = sql.create_engine('sqlite:////' + DB_PATH)
        self.conn = self.engine.connect()
        self.model = model

    def user_recommend(self, user_id):
        #Исправить на норм взаимодействие с бд
        user = pd.read_sql(f'select <vector> from users where id = {user_id}', self.engine).values
        distances = self.sorted_distances(user)
        ids = np.array(pd.read_sql('select id from events'), self.engine)
        ordered = []
        for idx in distances:
            ordered.append(ids[idx])
        return ordered

    def event_recommend(self, new_event):
        ids = np.array(pd.read_sql('select id from events'))
        distances = self.sorted_distances(new_event)
        return ids[distances[0]]

    def sorted_distances(self, vector):
        events = np.array(pd.read_sql('select <vector> from events'), self.engine)
        return np.argsort(cosine_distances(vector.reshape(1, -1), events))

class Processor:
    def __init__(self, data, model):
        self.model = model
        self.data = data

    def user_processing(self, data):
        groups = []
        for group in data:
            name = vectorize(self.model, group['name'])
            description = vectorize(self.model, group['description'])
            posts = np.mean(list(map(lambda x: vectorize(model=self.model, text=x), group['wall'])), axis=0)
            groups.append(np.mean([name, description, posts], axis=0))
        return np.mean(groups, axis=0)

    def event_processing(self, data):
        if isinstance(data, list):
            events = []
            for event in data:
                name = vectorize(self.model, data['name'])
                description = vectorize(self.model, data['description'])
                events.append(np.mean([name, description], axis=0))
            return np.mean(events, axis=0)
        else:
            name = vectorize(self.model, event['name'])
            description = vectorize(self.model, event['description'])
            return np.mean([name, description], axis=0)

    def process(self):
        try:
            return self.user_processing(self.data)
        except:
            return self.event_processing(self.data)