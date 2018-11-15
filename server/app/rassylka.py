import time
import requests
import math
from json import loads, dumps
from bs4 import BeautifulSoup
import urllib.request

url = 'https://api.vk.com/method/'
meth_name = ''
params = ''
token = 'access_token=504e9431504e9431504e943152502867565504e504e94310bab289c9cc9b34368fea727&'
version = 'v=5.87'


# residents = session.query(User).filter_by(Role='resident').all()
# residentIds = [res['id'] for res in residents]
# all = session.query(User).all()
# allIds = [one['id'] for one in all]


# вызывать после того как резидента оставит заявку на проведение мероприятия
def SendMesToResident(user_id, message):
    meth_name = 'messages.send?'
    #message = 'Здравствуйте! Вы заполнили заявку на проведение мероприятия, она одобрена. Если возникнут вопросы или ' \
    #          'изменения в планах, пишите в сообщения группы '
    params = 'user_id=' + user_id + '&' + 'message=' + message + '&'

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

    return temp

# ======================================================

def SendNotificationToUsers(userIds, message):
    meth_name = 'messages.send?'
    #message = 'Мероприятие "Название" начнет уже завтра, не пропусти!'
    user_id = ""
    for id in userIds:
        user_id += str(id) + ','
    if user_id == "":
        return None
    user_id = user_id[:-1]
    params = 'users_id=' + user_id + '&' + 'message=' + message + '&'

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

    return temp



# ======================================================

def SendNotificationToAll(allIds, message):
    #meth_name = 'messages.send?'
    message = 'Все мероприятия на завтра к сожалению отменяются по техническим причинам!'
    user_id = ""
    for id in allIds:
        user_id += str(id) + ','
    if user_id == "":
        return None
    user_id = user_id[:-1]
    params = 'users_id=' + user_id + '&' + 'message=' + message + '&'

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

    return temp
