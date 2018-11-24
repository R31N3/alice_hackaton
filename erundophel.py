from __future__ import unicode_literals
import random, json
import database_module

def read_data():
    with open("words.json", encoding="utf-8") as file:
        data = json.loads(file.read())
        return data

def map_answer(myAns,withAccent=False):
    res = myAns
    if(withAccent): return  myAns.replace(".", "").replace(";","").strip()
    else: return myAns.replace(".", "").replace(";", "").replace("+","").strip()

def saveResult(resultData): #Функция для сохранения результата (возвращает True если успешно)
    return True


def getAllResults(): #Функция для получения всех результатов из данных (возвращает результаты по типу [{"Имя":очки},{"Имя2":очки}])
    return []


def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        user_storage = {
            'suggests': [
                "Хорошо","ОК",
                "А что это?",
            ]
        }

        buttons, user_storage = get_suggests(user_storage)
        response.set_text('Привет! Давай поиграем в Завалинку!')
        response.set_tts('Прив+ет! -  Дав+ай поигр+аем в Зав+алинку!')
        response.set_buttons(buttons)


        return response, user_storage

    if request.command.lower() in ['ладно', 'хорошо', 'ок', 'согласен'] and not user_storage.get(request.user_id):
        user_storage[request.user_id] = {"movesLeft": random.randint(15, 25), "text": "Начинаем! ", "words":read_data(),"answer":"","score":0}

    if user_storage.get(request.user_id):
        if user_storage[request.user_id]["answer"]:
            if map_answer(request.command).lower() == map_answer(user_storage[request.user_id]["answer"]).lower():
                user_storage[request.user_id]["text"] = "Правильно! Следующий вопрос: "
                user_storage[request.user_id]["textToSpeech"] = "Пр+авильно! Сл+едующий вопр+ос: "
                user_storage[request.user_id]["score"]+=1
            else:
                user_storage[request.user_id]["text"] = "Неправильно, это {}. Следующий вопрос: ".format(map_answer(user_storage[request.user_id]["answer"]))
                user_storage[request.user_id]["textToSpeech"] = "Непр+авильно, это {}. Сл+едующий вопр+ос: ".format(map_answer(user_storage[request.user_id]["answer"],True))

        word = random.choice(list(user_storage[request.user_id]["words"].keys()))
        answers = user_storage[request.user_id]["words"][word]
        answer = list(map(lambda x:x[0],answers))
        del user_storage[request.user_id]["words"][word]
        user_storage[request.user_id]["movesLeft"]-=1
        if user_storage[request.user_id]["movesLeft"] > 0:
            user_storage["suggests"] = [i.lower().replace(".", "").replace(";","").strip() for i in answer]
            print(user_storage)
            buttons, user_storage = get_suggests(user_storage)
            response.set_buttons(buttons)
            response.set_text(user_storage[request.user_id]["text"]+"{} - это:".format(map_answer(word)))
            response.set_tts(user_storage[request.user_id]["textToSpeech"]+"{} - это:".format(map_answer(word,True)))
            for e in answers:
                if e[1]:
                    user_storage[request.user_id]["answer"] = e[0]
                    break
        else:
            response.set_text(user_storage[request.user_id]["text"] + "ой! Это всё за эту игру. Вы заработали {} баллов. Предлагаю сыграть ещё!".format(user_storage[request.user_id]["score"]))
            response.set_tts(user_storage[request.user_id]["text"] + "ой! Это всё за эту игру. Вы зараб+отали {} баллов. Предлаг+аю сыграть ещё!".format(user_storage[request.user_id]["score"]))
    if request.command.lower().strip("?!.") in ['а что это', 'чего', 'всмысле', 'что такое ерундопель']:
        response.set_text('Завалинка - это игра на интуинтивное знание слов. Я называю Вам слово, например,'
                          ' Кукушляндия. Я предлагаю Вам ответы внизу, например, страна кукушек.'
                          ' Если Вы угадали, то вам насчитывается балл.')
        response.set_tts('Зав+алинка - это игра на интуинт+ивное знание слов. Я назыв+аю Вам слово, например,'
                                  ' Кукушл+яндия. Я предлагаю Вам ответы внизу, наприм+ер, страна кук+ушек.'
                                  ' Если Вы угад+али, то вам насч+итывается балл.')        
        buttons, user_storage = get_suggests(user_storage)
        response.set_buttons(buttons)

    return response, user_storage


def get_suggests(user_storage):
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in user_storage['suggests']
    ]

    return suggests, user_storage
