from time import time
import requests
from json import loads
from bs4 import BeautifulSoup
import urllib.request
import json
import sqlite3 as sql
from app import nlpModel, db, DB_PATH
from app.nlpModel.model import Processor
from app.users.models import Event
from threading import Thread

url = 'https://api.vk.com/method/'
meth_name = ''
params = ''
token = 'access_token=bdd4f04384e64fca69b320980a74f961b1a6913d4af63bb03beb114f1d64bf962f44dc60669f3da551d3d&'
version = 'v=5.87'


class MyThread(Thread):
    """
    A threading example
    """

    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        """Запуск потока"""
        msg = "%s is running" % self.name
        print(msg)

def parse_instant_view(url):
    html = urllib.request.urlopen(url).read().decode('utf-8')
    data = BeautifulSoup(html, 'lxml')
    text = ''
    node = data.find('p', {'class': 'article_decoration_first'})
    text += node.getText()
    while True:
        node = node.nextSibling
        if node is None:
            break
        if node.has_attr("article_decoration_last"):
            break
        text += node.getText()
    return text


def GetUser(id):
    meth_name = 'users.get?'
    params = 'user_ids=' + id
    link = url + meth_name + params + token + version

    temp = None
    _count = 0
    while temp is None:
        ans = requests.get(link).text
        ans = loads(ans)
        temp = ans.get('response')
        if _count > 1:
            time().sleep(1)
        _count += 1
        if _count == 5:
            return None

    new_id = temp[0].get('id')
    return new_id


def GetGroups(id, extended='0&', count='10&'):
    meth_name = 'groups.get?'
    params = 'user_id=' + id + 'extended=' + extended + 'count=' + count
    link = url + meth_name + params + token + version

    temp = None
    _count = 0
    while temp is None:
        ans = requests.get(link).text
        ans = loads(ans)
        temp = ans.get('response')
        if _count > 1:
            time().sleep(1)
        _count += 1
        if _count == 5:
            return None

    groups = temp.get('items')
    return groups


def GetWall(owner_id, offset='0&', extended='0&', count='10&'):
    meth_name = 'wall.get?'
    params = 'owner_id=' + owner_id + 'extended=' + extended + 'offset=' + offset + 'count=' + count
    link = url + meth_name + params + token + version

    temp = None
    _count = 0
    while temp is None:
        ans = requests.get(link).text
        ans = loads(ans)
        temp = ans.get('response')
        if _count > 1:
            time.sleep(1)
        _count += 1
        if _count == 5:
            return None

    walls = []
    items = temp.get('items')
    for i in range(len(items)):
        walls.append(items[i].get('text'))
    return walls


def GetInfoGroup(id):
    meth_name = 'groups.getById?'
    params = 'group_id=' + id
    link = url + meth_name + params + token + version

    temp = None
    _count = 0
    A = {}
    while temp is None:
        ans = requests.get(link).text
        ans = loads(ans)
        temp = ans.get('response')
        if _count > 1:
            time.sleep(1)
        _count += 1
        if _count == 5:
            return None

    name = temp[0].get('name')
    description = temp[0].get('description')
    A = {'name': name, 'description': description}
    return A


def getExecute(code):
    meth_name = 'execute?'
    params = 'code=' + code + '&'
    link = url + meth_name + params + token + version

    temp = None
    count = 0
    while temp is None:
        execute = requests.get(link).text
        execute = loads(execute)
        temp = execute.get('response')
        if count > 1:
            time.sleep(1)
        count += 1
        if count == 5:
            return None
    return execute.get('response')


def getVkScriptForWallExecute(allTheGroups):
    requestString = 'return [ '
    for item in allTheGroups:
        requestString += 'API.wall.get({"owner_id": -' + str(item) + ', "count": "10"' + ' }), '
    requestString = requestString[0:-2]
    requestString += ' ];'
    return requestString


def getVkScriptForInfoExecute(allTheGroups):
    requestString = 'return [ '
    for item in allTheGroups:
        requestString += 'API.groups.getById({"group_id": ' + str(item) + ', "fields": "description"' + ' }), '
    requestString = requestString[0:-2]
    requestString += ' ];'
    return requestString


def getData(id_int):
    start_time = time()

    # id_int = GetUser('andreyvolkov1999' + '&')

    groups = GetGroups(str(id_int) + '&')
    code_info = getVkScriptForInfoExecute(groups)
    code_wall = getVkScriptForWallExecute(groups)
    res = getExecute(code_info)
    res_wall = getExecute(code_wall)
    for i in range(len(res)):
        name = res[i][0]['name']
        description = res[i][0]['description']
        posts = res_wall[i]['items']
        for j in range(len(posts)):
            if posts[j].get('attachments') is not None and posts[j]['attachments'][0]['type'] == 'link':
                try:
                    posts[j] = parse_instant_view(posts[j]['attachments'][0]['link']['url'])
                except:
                    posts[j] = posts[j]['text']
            else:
                posts[j] = posts[j]['text']

        res[i] = {'name': name, 'description': description, 'wall': posts}

    print("--- %s seconds ---" % (time() - start_time))

    return res

def InitTestData(path = '../tmp/events_1.json'):
    with open(path, encoding='utf-8') as f:
        data = json.loads(f.read()[1:])

    processor = Processor(nlpModel)
    for elem in data:

        vector = processor.event_processing(elem)
        event = Event(name=elem['name'], description=elem['description'],
                      photo=elem['photo'], link=elem['link'],
                      data=elem['from'], vector=vector, resident_id=1)

        db.session.add(event)
    db.session.commit()
    print("Init ends!!!"*3)


class Statistics:
    @staticmethod
    def get_events(resident_id):
        conn = sql.connect(DB_PATH)
        return [i for i in conn.execute(f'select * from events_event where resident_id = {resident_id}')]

    def get_rating(self, event_id):
        conn = sql.connect(DB_PATH)
        return [i for i in conn. \
            execute(f'select avg(rating) from users_events where events_id = {event_id} group by events_id')][0][0]

    def get_comments(self, event_id):
        conn = sql.connect(DB_PATH)
        return [i for i in conn.execute(f'select rating, comment from users_events where events_id = {event_id}')]

    def get_attendants(self, event_id):
        conn = sql.connect(DB_PATH)
        return [i for i in conn. \
            execute(f'select count(1) from users_events where events_id = {event_id} group by events_id')][0][0]

    def get_metrics(self, _id):
        temp = dict()
        temp['rating'] = self.get_rating(_id)
        temp['attendants'] = self.get_attendants(_id)
        temp['comments'] = self.get_comments(_id)
        return temp