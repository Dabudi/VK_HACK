from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from gensim.models.fasttext import FastText
import sqlite3 as sql
DB_PATH = 'C:/Users/User/Desktop/VK_HACK/VK_HACK/server/app/tables.db'

nlpModel = FastText.load('app/nlpModel/araneum_none_fasttextskipgram_300_5_2018.model')
app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Config)
db.init_app(app)
from app.users.models import *
db.create_all()
db.session.commit()
from app.tools import InitTestData

conn = sql.connect(DB_PATH)
if not [i for i in conn.execute('SELECT count(1) FROM events_event')][0][0]:
    print('first')
    print('-----------------'*50)
    #InitTestData()
else:
    print('$'*50)
InitTestData()

from app.users.models import *
db.create_all()
from app import routes
