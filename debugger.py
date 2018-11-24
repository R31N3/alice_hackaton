from erundophel import *
class DeRequest():
    def __init__(self,isNewSession,userID):
        self.is_new_session = isNewSession
        self.user_id = userID
        self.command = ""
class DeResponse():
    def __init__(self):
        self.text = ""
        self.tss = ""
        self.buttons = []
    def set_text(self,text):
        self.text = text
    def set_tts(self,text):
        self.tss = text
    def set_buttons(self,buttons):
        self.buttons = buttons

def printResponce(response):
    print("Текст: "+response.text)
    print("Алиса говорит: "+response.tss)
    print("Кнопки:")
    for button in response.buttons:
        print("----")
        print("Текст: "+button["title"],"; Видно: "+"да" if button['hide'] else "нет")
    print("----")
print("DE: Введите ID пользователя")
id = input()
stResponce = DeResponse()
responce, userStorage = handle_dialog(DeRequest(True,id),stResponce,{})
printResponce(responce)
while True:
    res = input()
    stResponce = DeResponse()
    mRequest = DeRequest(False, id)
    mRequest.command = res
    responce, userStorage = handle_dialog(mRequest, stResponce, userStorage)
    printResponce(stResponce)