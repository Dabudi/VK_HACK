from flask import request, jsonify, render_template
from app import app, db, nlpModel, DB_PATH
from app.users.models import User, Event, UserEvnet
from app.nlpModel.model import Processor, Recommender
from app.tools import *
import sqlite3 as sql

@app.route('/register')
def register():
    vkId = request.args.get('vkId')

    if not vkId:
        return jsonify({"isRegistered": False,
                        "isSuccess": True,
                        "Error": "Cant parse a number"})

    print('-------------------------------------------')
    print(vkId)
    print('-------------------------------------------')
    if User.query.filter_by(vk_id=vkId).first():
        print('isRegister')
        return jsonify({"isRegistered": True,
                        "isSuccess": True,
                        "Error": "none"})
    else:
        vk_id = request.args.get('vkId')
        role = 'User'#request.args.get('role')
        data = getData(vk_id)
        print('__________dATA______________')
        print(data)
        processor = Processor(nlpModel)
        predict = processor.user_processing(data)

        new_user = User(vk_id=vkId, Role=role, target=predict)
        db.session.add(new_user)
        db.session.commit()
        """
        except Exception:
            print('Error')
            return jsonify({"isRegistered": False,
                            "isSuccess": False,
                            "Error": "Some not happy"})
        """
        print('isNoRegister')
        return jsonify({"isRegistered": False,
                        "isSuccess": True,
                        "Error": "none"})



@app.route('/getWall')
def getWall():
    vkId = request.args.get('vkId')
    recomender = Recommender(nlpModel)

    res_events = []
    for event_id in recomender.user_recommend(vkId):
        event_id = event_id[0]
        conn = sql.connect(DB_PATH)
        cur_event = [i for i in conn.execute(f'SELECT name, description, photo, data FROM events_event WHERE id={event_id}')][0] #Event.query.filter_by(id=event_id).first()
        description = cur_event[1]
        res_events.append({"title": cur_event[0],
                           "eventId": event_id,
                           "shortDescription": ' '.join([elem for elem in description.split()[:15]]),
                           "photo": cur_event[2],
                           "date": cur_event[3],
                           "Description": description})

    return jsonify(res_events)

@app.route('/setEvent')
def setEvent():
    try:
        vkId = request.args.get('vkId')
        eventId = request.args.get('eventId')


        if UserEvnet.query.filter_by(user_id=vkId, eventId=eventId):
            return jsonify({"isSuccess": False,
                            "Error": "event already register"})

        userEvent = UserEvnet(user_id=vkId, eventId=eventId)

        db.session.add(userEvent)
        db.session.commit()

        return jsonify({"isSuccess": True})
    except Exception:
        return jsonify({"isSuccess": False,
                        "Error": "some bad"})

@app.route('/setFavourites')
def getFavourites():
    vkId = request.args.get('vkId')

    user = User.query.flter_by(vk_id=vkId).first()
    if not user:
        return jsonify({"isSuccess": False,
                        "Error": "User not register yet"})

    res_events = []
    for event_id in UserEvnet.query.filter_by(user_id=vkId):
        event_id = event_id[0]
        conn = sql.connect(DB_PATH)
        cur_event = [i for i in conn.execute(f'SELECT name, description FROM events_event WHERE id={event_id}')][0] #Event.query.filter_by(id=event_id).first()
        description = cur_event[1]
        res_events.append({"title": cur_event[0],
                           "eventId": event_id,
                           "shortDescription": ' '.join([elem for elem in description.split()[:15]]),
                           "Description": description})

    return jsonify(res_events)

@app.route('/setRating')
def setRating():
    event_id = request.args.get('eventId')
    user_id = request.args.get('userId')
    comment = request.args.get('comment')
    rating = request.args.get('rating')

    try:
        userEvent = UserEvnet.query.filter_by(user_id=user_id, event_id=event_id).first()

        userEvent.comment = comment or ''
        userEvent.rating = rating
        db.session.commit()
    except  Exception:
        return jsonify({"isSuccess": False,
                        "Error": "Some very very bad"})

    return jsonify({"isSuccess": True})

@app.route('/getRating')
def getRating():
    event_id = request.args.get('event_id')

    statistic = Statistics()
    metrics = statistic.get_metrics(event_id)

    res = {"metrics": {"avg_rating": metrics['rating'],
                       "num_attendants": metrics["attendants"],
                       "comments": []}}

    conn = sql.connect(DB_PATH)
    all_commit = [elem for elem in conn.execute(f'SELECT rating,comment FROM users_events WHERE events_id={event_id}')]

    res['metrics']['comments'] = all_commit

    return jsonify(res)


@app.route('/resident/events/getEvents')
def getEvents():
    resident_id = request.args.get('residentId')
    return jsonify([{"name": elem[1], "shortDescription": ' '.join(elem[2].split()[:15]),"description": elem[2], "date": elem[3],
      "photo": elem[4], "link": elem[5], "id": elem[0]} for elem in Statistics.get_events(resident_id)])


@app.route('/resident/events/getMetrics')
def getMetrics():
    event_id = request.args.get('eventsId')

    statistics = Statistics()

    return jsonify(statistics.get_metrics(event_id))


@app.route('/admin/addEvent', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['field1']
        desription = request.form['field5']
        date = request.form['field3']
        photo = request.form['field4']
        link = request.form['field5']
        print(name, desription, date, photo, link)

        try:
            processor = Processor(nlpModel)
            vector = processor.event_processing({"name": name, "description": desription})

            event = Event(name=name, description=desription,
                          data=date, photo=photo, link=link,
                          vector=vector, resident_id=1)

            db.session.add(event)
            db.session.commit()

            return jsonify({"isSuccess": True})
        except Exception:
            return jsonify({"isSuccess": False, "Error": "So boring news =/"})

    return render_template('adminPage.html')


@app.route('/admin/sendMessage')
def sendMessage():
    pass
