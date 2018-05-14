# Хакатон по Алисе
Этот репозиторий содержит материалы для хакатона Яндекс.Лицея по Алисе.

## Структура репозитория
- `skill_example/`. Здесь находится код тестового навыка "Купи слона".
- `skills_data/`. Здесь содержатся вспомогательные данные, которые помогут при написании некоторых навыков.
- `setup/`. Содержит инструкцию по настройке ноутбуков для хакатона. Эта директория нужна только менторам и техническому персоналу.

## Тестовый навык "Купи слона"
В директории `skill_example` находится полностью рабочий пример навыка.
Он позаимствован из официальной документации к Алисе https://tech.yandex.ru/dialogs/alice/doc/quickstart-python-docpage/ и немного переработан специально для хакатона.
- В файле `elephant.py` реализована логика навыка (функция `handle_dialog`), т.е. обработка пользовательского ввода и реакция на него.
- В файле `alice_sdk.py` находится небольшая библиотека для работы с API Алисы.
- В файле `alice_app.py` находится программа, запускающая веб-сервис с навыком.

### Локальный запуск и отладка
Сперва установите все зависимости: `pip install -r requirements.txt` (лучше сделать это в виртуальном окружении).
Чтобы запустить навык, используйте команду `python alice_app.py`.
На вашем компьютере запустится веб-сервис, который будет принимать запросы локально.
Чтобы сделать его видимым "наружу", воспользуйтесь утилитой `ngrok`, которая уже установлена на вашем компьютере.
- Зарегистрируйтесь на сайте https://ngrok.com/.
- Зайдите на страницу https://dashboard.ngrok.com/auth и скопируйте оттуда токен (Your Tunnel Authtoken)
- Выполните команду `ngrok authtoken ВАШ_ТОКЕН`
- Выполните команду `ngrok http 5000`
Готово! В консоли появится строка, содержащая сгенерированный URL (обязательно https!):
```
Forwarding                    https://87436678.ngrok.io -> localhost:5000
```
Этот URL нужно будет подставить в Webhook URL в настройках навыка (интерфейс https://beta.dialogs.yandex.ru/).
**После того, как навыки отправятся на модерацию, не перезапускайте ngrok, т.к. для модерации нужен URL навыка.**

### Развертывание навыков в облаке
Для развертывания мы будем пользоваться утилитой now (https://zeit.co/now), которая уже установлена на ваших ноутбуках.
Чтобы развернуть свой навык в облаке, нужно выполнить команду `now --public` в директории с кодом навыка (флаг `--public` означает, что исходный код вашего приложения будет находиться в открытом доступе).
При первом вызове вам будет предложено залогиниться и создать аккаунт на сайте zeit.co -- сделайте это.
После вызова этой команды в консоль выведется URL вида https://имя-навыка-и-случайная-строка.now.sh.
Этот URL нужно будет подставить в Webhook URL в настройках навыка (интерфейс https://beta.dialogs.yandex.ru/).

При следующем запуске команды `now --public` будет развернуто новое приложение с новым URL.
Все версии развернутых навыков можно увидеть в дашборде https://zeit.co/dashboard.
Кликнув на URL приложения, вы попадете на страницу с логами -- это полезно для отладки.

**Внимание!** Поскольку мы будем пользоваться бесплатным облаком, это накладывает некоторые ограничения.
В частности, одновременно можно развернуть не более трех версий вашего навыка.
Для целей хакатона это несущественно, поэтому вы можете удалять старые версии навыков командой `now rm имя-развернутого-приложения`.
Чтобы увидеть название вашего развернутого приложения, нужно воспользоваться командой `now ls`.


## Навыки

### Завалинка
Алиса называет слово, пользователь выбирает из вариантов правильное значение.
Файл со словами и их значениями можно взять из репозитория: `skills_data/zavalinka.txt`

### Крокодил
Алиса загадывает слово, его надо показать жестами.

### Шляпа
Алиса показывает набор слов, их надо объяснить другими словами, Алиса запоминает счёт.

### Что? Где? Когда?
Алиса задаёт вопрос, проверяет ответ, ведёт счёт зрителей против знатоков.
База вопросов для ЧГК: https://db.chgk.info/

### Тезаурус
Пользователь говорит слово, Алиса объясняет смысл.
Рекомендуем воспользоваться API словарей ABBYY Lingvo: https://developers.lingvolive.com/ru-ru/

### Синонимы
Пользователь говорит слово, Алиса подбирает синонимы.
Рекомендуем воспользоваться API Яндекс.Словаря: https://tech.yandex.ru/dictionary/

### Быки и Коровы
Алиса загадывает четырехзначное число, игрок пытается отгадать это число, перебирая различные варианты.
На каждый вариант игрока Алиса отвечает два числа:
- количество "быков" -- количество правильных цифр на правильных местах
- количество "коров" -- количество правильных цифр, но на неправильных местах
Подробные правила с примерами: https://ru.wikipedia.org/wiki/Быки_и_коровы

Для обработки голосового ввода можно воспользоваться таблицей числительных `skills_data/numerals.csv`.

### Викторина про города
Алиса называет страну, игрок отгадывает столицу страны.
Данные о городах можно взять из файла `skills_data/big-city-data.csv`.

### Викторина по истории России
Алиса называет событие из истории России, игрок отгадывает год, когда это событие состоялось.
Данные о событиях истории России находятся в файле `skills_data/russian-history-events.csv`.
Для обработки голосового ввода можно воспользоваться
- таблицей числительных `skills_data/numerals.csv`;
- библиотекой `pymorphy2`.

### Перевертыш
Алиса называет предложение, в котором каждое слово заменено на противоположное по значению, а игрок пытается назвать исходное предложение.
Набор предложений для данной игры можно взять: https://www.psyoffice.ru/4-0-1146.htm

### Я беру с собой на север
Игрок называет слово, а Алиса говорит берет ли его на север, следуя различным правилам.
Правила могут быть совершенно разными:
- все слова на одну определенную букву
- заданное количество гласных в слове
- слова с одинаковым корнем

## Полезные ссылки
- Документация по разработке навыков для Алисы начинается здесь: https://tech.yandex.ru/dialogs/alice/doc/about-docpage/
- Интерфейс для разработки навыков: https://beta.dialogs.yandex.ru/
