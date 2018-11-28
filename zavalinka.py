# coding: utf-8
from __future__ import unicode_literals
import random, json
import database_module

global flag, another_flag
flag = False
another_flag = False

def read_data():
    with open("words.json", encoding="utf-8") as file:
        data = json.loads(file.read())
        return data

def read_answers_data():
    with open("alice_answers.json", encoding="utf-8") as file:
        data = json.loads(file.read())
        return data

aliceAnswers = read_answers_data()

def aliceSpeakMap(myAns,withAccent=False):
    if(withAccent): return  myAns.strip()
    else: return myAns.replace("+","").strip()

def map_answer(myAns,withAccent=False):
    if(withAccent): return  myAns.replace(".", "").replace(";","").strip()
    else: return myAns.replace(".", "").replace(";", "").replace("+","").strip()


def handle_dialog(request, response, user_storage, database, wrd):
    global flag, another_flag
    answered = False
    if request.is_new_session or flag:
        answered = True
        user_storage = {
            "asking_name":True,
            'play_times':0,'total_score':0
        }
        if user_storage["asking_name"] and not (database.get_entry(request.user_id) and request.is_new_session):
            if request.is_new_session:
                flag = True
                answered = True
                response.set_text(aliceSpeakMap("Добрый день! Как тебя зовут?"))
                response.set_tts(aliceSpeakMap("Добрый день! Как тебя зовут?"))
                return response, user_storage
            if "name" not in user_storage.keys():
                if not database.get_entry(request.user_id):
                    user_storage["asking_name"] = False
                    user_storage["name"] = request.command.split(" ")[0]
                    database.add_user(request.user_id, user_storage["name"])
                    database.update_score(request.user_id, 0)
                else:
                    user_storage["name"] = database_module.show_score(database, request.user_id)[1]
            buttons, user_storage = get_suggests(user_storage)
            response.set_buttons(buttons)
            user_storage['suggests']= [
                "Хорошо",
                "А что это?",
                "Таблица лидеров"
            ]
            buttons, user_storage = get_suggests(user_storage)
            if not another_flag:
                choice = random.choice(aliceAnswers["thanksVariations"])+ " " + random.choice(aliceAnswers["helloTextVariations"]).capitalize()
            else:
                choice = random.choice(aliceAnswers["helloTextVariations"]).capitalize()
            response.set_text(aliceSpeakMap(choice))
            response.set_tts(aliceSpeakMap(choice,True))
            response.set_buttons(buttons)
            flag = False
            return response, user_storage
        another_flag = True
        flag = True
        response.set_text("Здравствуйте, а я тебя помню!")
        response.set_tts("Здравствуйте, а я тебя п+омню!")
        return response, user_storage
    if request.command.lower() in ['ладно', 'хорошо', 'ок', 'согласен','да','не, играть хочу'] and not user_storage.get(request.user_id):
        answered = True
        user_storage[request.user_id] = {"movesLeft": random.randint(15, 25), "text": "Начинаем! ","textToSpeech":"Начин+аем!", "words":read_data(),"answer":"","score":0}
    if request.command.lower().strip("?!.") in ['а что это', 'чего', 'в смысле', 'что такое ерундопель', "что"] and not answered:
        answered = True
        response.set_text('Завалинка - это игра на интуинтивное знание слов. Я называю Вам слово, например,'
                          ' Кукушляндия. Я предлагаю Вам ответы внизу, например, страна кукушек.'
                          ' Если Вы угадали, то вам насчитывается балл.')
        response.set_tts('Зав+алинка - это игра на интуинт+ивное знание слов. Я назыв+аю Вам слово, например,'
                                  ' Кукушл+яндия. Я предлагаю Вам ответы внизу, наприм+ер, страна кук+ушек.'
                                  ' Если Вы угад+али, то вам насч+итывается балл. Доступные команды'+
                                  ", ".join(user_storage["suggests"]))
        buttons, user_storage = get_suggests(user_storage)
        response.set_buttons(buttons)
        return response, user_storage
    if request.command.lower().strip("?!.") in ['нет', 'не хочется', 'в следующий раз', 'выход', "не хочу", 'выйти']:
        answered = True
        choice = random.choice(aliceAnswers["quitTextVariations"])
        response.set_text(aliceSpeakMap(choice))
        response.set_tts(aliceSpeakMap(choice,True))
        response.end_session = True
        return response, user_storage
    if "таблица лидер" in request.command.lower().strip("?!.") or request.command.lower().strip("?!.") in ["посмотреть"]:
        answered = True
        choice = random.choice(aliceAnswers["resultsShowVariations"])
        results = database_module.show_leaderboard(database, 10)
        resultsText = "\n"
        for i in range(len(results)):
            resultsText+=str(i+1)+" место: "+list(results[i].keys())[0]+" ("+str(list(results[i].values())[0])+" "+wrd.make_agree_with_number(list(results[i].values())[0]).word+")\n"
        resultsText+="А у вас счёт "+str(database_module.show_score(database, request.user_id)[1])+"! И всё таки, " + random.choice(aliceAnswers["helloTextVariations"]).lower()
        response.set_text(aliceSpeakMap(choice+resultsText))
        response.set_tts(aliceSpeakMap(choice+resultsText,True)+" Доступные команды: К началу")
        another_flag = True
        flag = True
        user_storage["suggests"] = ["К началу"]
        buttons, user_storage = get_suggests(user_storage)
        response.set_buttons(buttons)
        return response, user_storage

    if user_storage.get(request.user_id):
        answered = True
        if user_storage[request.user_id]["answer"] and not another_flag:
            if map_answer(request.command).lower() == map_answer(user_storage[request.user_id]["answer"][:len(request.command)]).lower():
                user_storage[request.user_id]["text"] = "Правильно! Следующий вопрос: "
                user_storage[request.user_id]["textToSpeech"] = "Пр+авильно! Сл+едующий вопр+ос: "
                otvet = random.choice([["Правильно!","Пр+авильно!"],["Отлично!","Отл+ично!"],["Молодец!","Молод+ец!"]])
                user_storage[request.user_id]["text"] = otvet[0]+" Следующий вопрос: "
                user_storage[request.user_id]["textToSpeech"] = otvet[1]+" Сл+едующий вопр+ос: "
                database.update_score(request.user_id, database_module.show_score(database,request.user_id)[1]+1)
            else:
                user_storage[request.user_id]["text"] = "Неправильно, это {}. Следующий вопрос: ".format(map_answer(user_storage[request.user_id]["answer"]))
                user_storage[request.user_id]["textToSpeech"] = "Непр+авильно, это {}. Сл+едующий вопр+ос: ".format(map_answer(user_storage[request.user_id]["answer"],True))
                otvet = random.choice([["Неправильно!","Непр+авильно!"],["Неверно!","Нев+ерно!"],["Вы ошиблись!","Вы ош+иблись!"]])
                user_storage[request.user_id]["text"] = otvet[0]+" Это {}. Следующий вопрос: ".format(map_answer(user_storage[request.user_id]["answer"]))
                user_storage[request.user_id]["textToSpeech"] = otvet[1]+" Это {}. Сл+едующий вопр+ос: ".format(map_answer(user_storage[request.user_id]["answer"],True))

        word = random.choice(list(user_storage[request.user_id]["words"].keys()))
        answers = user_storage[request.user_id]["words"][word]
        answer = list(map(lambda x:x[0],answers))
        del user_storage[request.user_id]["words"][word]
        user_storage[request.user_id]["movesLeft"]-=1
        if user_storage[request.user_id]["movesLeft"] > 0:
            user_storage["suggests"] = [i.lower().replace(".", "").replace(";","").strip() for i in answer]
            #print(user_storage)
            buttons, user_storage = get_suggests(user_storage)
            response.set_buttons(buttons)
            response.set_text(user_storage[request.user_id]["text"]+"{} - это:".format(map_answer(word)))
            response.set_tts(user_storage[request.user_id]["textToSpeech"]+"{} - это: {}".format(map_answer(word,True), ", ".join(user_storage["suggests"])))
            for e in answers:
                if e[1]:
                    user_storage[request.user_id]["answer"] = e[0]
                    break
        else:
            choice = random.choice(aliceAnswers["winTextVariations"])
            if((user_storage["play_times"]+1)%3!=0):
                response.set_text(user_storage[request.user_id]["text"] + aliceSpeakMap(choice).format(user_storage[request.user_id]["score"]))
                response.set_tts(user_storage[request.user_id]["text"] + aliceSpeakMap(choice,True).format(user_storage[request.user_id]["score"]))
                user_storage['suggests'] = ["Хорошо","Согласен", "Таблица лидеров"]

                buttons, user_storage = get_suggests(user_storage)
                response.set_buttons(buttons)
            else:
                choice2 = random.choice(aliceAnswers["checkResultVariations"])
                response.set_text(user_storage[request.user_id]["text"] + aliceSpeakMap(choice).format(
                    user_storage[request.user_id]["score"])+aliceSpeakMap(choice2))
                response.set_tts(user_storage[request.user_id]["text"] + aliceSpeakMap(choice, True).format(
                    user_storage[request.user_id]["score"])+aliceSpeakMap(choice2))
                user_storage['suggests'] = ["Не, играть хочу", "Таблица лидеров"]
                buttons, user_storage = get_suggests(user_storage)
                response.set_buttons(buttons)
            del user_storage[request.user_id]
            user_storage["total_score"]+=int(user_storage[request.user_id]["score"])
        another_flag = False
        return response,user_storage

    if not answered:
        choice = random.choice(aliceAnswers["cantTranslate"])
        response.set_text(aliceSpeakMap(choice))
        response.set_tts(aliceSpeakMap(choice, True))
        buttons, user_storage = get_suggests(user_storage)
        response.set_buttons(buttons)
    return response, user_storage


def get_suggests(user_storage):
    if "suggests" in user_storage.keys():
        suggests = [
            {'title': suggest, 'hide': True}
            for suggest in user_storage['suggests']
        ]
    else:
        suggests = []

    return suggests, user_storage
