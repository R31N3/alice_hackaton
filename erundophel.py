from __future__ import unicode_literals
import random, json


def read_data():
    with open("words.json", encoding="utf-8") as file:
        data = json.loads(file.read())
        return data


def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        user_storage = {
            'suggests': [
                "Хорошо","ОК",
                "А что это?",
            ]
        }

        buttons, user_storage = get_suggests(user_storage)
        response.set_text('Привет! Давай поиграем в Ерундопель!')
        response.set_buttons(buttons)


        return response, user_storage

    if request.command.lower() in ['ладно', 'хорошо', 'ок', 'согласен'] and not user_storage.get("gameData"):
        user_storage[request.user_id] = {"movesLeft": random.randint(15, 25), "text": "Начинаем! ","words":read_data(),"answer":"","score":0}

    if user_storage.get(request.user_id):
        if user_storage[request.user_id]["answer"]:
            if request.command.lower().replace(",.!?:;\\|/") == user_storage[request.user_id]["answer"].lower().replace(",.!?:;\\|/"):
                user_storage[request.user_id]["text"] = "Правильно! Следующий вопрос: "
                user_storage[request.user_id]["score"]+=1
            else:
                user_storage[request.user_id]["text"] = "Неправильно, это {}. Следующий вопрос: ".format(user_storage[request.user_id]["answer"])

        word = random.choice(user_storage[request.user_id]["words"].keys())
        answers = user_storage[request.user_id]["words"][word]
        answer = list(map(lambda x:x[0],answers))
        del user_storage[request.user_id]["words"][word]
        user_storage[request.user_id]["movesLeft"]-=1
        if user_storage[request.user_id]["movesLeft"] > 0:
            response.set_text(user_storage[request.user_id]["text"]+"{} - это:".format(word)+" ".join(answer))
        else:
            response.set_text(user_storage[request.user_id]["text"] + "ой! Это всё за эту игру. Вы заработали {} баллов. Предлагаю сыграть ещё!".format(user_storage[request.user_id]["score"]))

    if request.command.lower().strip("?!.") in ['а что это', 'чего', 'всмысле', 'что такое ерундопель']:
        response.set_text('Ерундопель - это игра на интуинтивное знание слов. Я называю Вам слово, например,'
                          ' Кукушляндия. Я предлагаю Вам ответы внизу, например, страна кукушек.'
                          ' Если Вы угадали, то вам насчитывается балл.')


    buttons, user_storage = get_suggests(user_storage)
    response.set_text(''.format(request.command))
    response.set_buttons(buttons)

    return response, user_storage


def get_suggests(user_storage):
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in user_storage['suggests'][:2]
    ]
    user_storage['suggests'] = user_storage['suggests'][1:]
    if len(suggests) < 2:
        suggests.append({
             "title": "Ладно",
             "url": "https://market.yandex.ru/search?text=слон",
             "hide": True
         })

    return suggests, user_storage
