# Куда пойти — Москва глазами Артёма

Сайт - интерактивная карта Москвы, на которой отмечены места активного отдыха с подробными описаниями и комментариями.

Учебный проект курса "От джуна до мидла" компании Devman. 

Использованная технология - Django.

[Демка сайта](https://iba.pythonanywhere.com/) .

## Возможности

* Добавление локаций, описаний и коментариев, загрузка фото через админ-панель
* Быстрое добавление списка новых локаций из файлов JSON. 

## Локальная установка

1. Клонируйте данный репозиторий на локальную машину, создайте виртуальное окружение и установите зависимости из файла requirements.txt.  
2. В корневой директории приложения создайте файл .env со следующим содержимым.  
```
SECRET_KEY=secretvalue
DEBUG=True
```
Опционально: при использовании внешней базы данных добавьте переменную окружения DATABASE_URL [(подробнее)](https://pypi.org/project/dj-database-url/#url-schema). При необходимости использования нестандартных названий и расположений папок для статики и медиафайлов настройте переменные STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT.  Подробнее о настройке параметров Django читайте в [документации](https://docs.djangoproject.com/en/4.0/ref/settings/).

3. Примените миграции
```
python manage.py migrate
```
4. Создайте учетную запись администратора
```
python manage.py createsuperuser --username admin
```
5. Запустите сайт
```
python manage.py runserver
```
6. Загрузите тестовые данные (см. раздел Использование ниже).  
7. Проверьте работоспособность сайта по адресу http://127.0.0.1:8000/  


## Установка на хостинге

1. Ниже приведена инструкция по деплою сайта на хостинг [pythonanywhere.com](https://pythonanywhere.com). Для других хостингов ознакомьтесь с их документацией в части деплоя Django-приложений.
2. Войдите в аккаунт pythonanywhere.com, при необходимости предварительно зарегистрируйтесь.
3. Перейдите на страницу Consoles, в разделе Start new console нажмите Bash.
4. Введите команду 
```
git clone https://github.com/IBA20/where_to_go
```
Содержимое этого репозитория будет скопировано в директорию home/myusername/where_to_go, где myusername - ваш логин.

5. Создайте виртуальное окружение командой
```
mkvirtualenv --python=/usr/bin/python3.9 myvirtualenv
```
6. Перейдите в папку приложения и установите необходимые библиотеки 
```
cd where_to_go
pip install -r requirements.txt
```
7. Перейдите на страницу Web и создайте новое приложение (Add new web app). На шаге Select a Python Web framework выберите Manual configuration затем Python 3.9.
8. В разделе Virtualenv введите имя виртуального окружения, созданного на шаге 5 (myvirtualenv).
9. В разделе Code откройте wsgi-файл по ссылке WSGI configuration file. Удалите все, кроме раздела DJANGO. Раскомментируйте команды, откорректируйте имя директории с приложением. В итоге должно получиться примерно следующее:
```
import os
import sys

# assuming your django settings file is at '/home/myusername/mysite/mysite/settings.py'
# and your manage.py is is at '/home/myusername/where_to_go/manage.py'
path = '/home/myusername/where_to_go'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'where_to_go.settings'

# then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
Не забудьте сохранить файл кнопкой Save.

10. На странице Files перейдите в директорию home/myusername/where-to_go и создайте файл .env со следующим содержимым. 
```
SECRET_KEY=secretvalue
ALLOWED_HOSTS=myusername.pythonanywhere.com
```
Замените secretvalue на надежный секретный ключ для Django, a myusername - на ваш логин. Сохраните файл.
11. Вернитесь в Bash-консоль и ввведите команды
```
python manage.py collectstatic
python manage.py migrate
```
12. Создайте учетную запись администратора
```
python manage.py createsuperuser --username admin
```
13. На странице Web в разделе Static files пропишите следующее:

URL&emsp;&emsp;Directory

/static/ &emsp;/home/myusername/where_to_go/static	 

/media/&emsp;/home/myusername/where_to_go/media

14. В разделе Security установите Force HTTPS: Enabled. Нажмите кнопку Reload: myusername.pythonanywhere.com
15. Загрузите тестовые данные (см. раздел Использование ниже) и проверьте работоспособность сайта.  
16. Дополнительные сведения по деплою [здесь](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject)
17. Опционально: для работы с внешними базами данных пропишите переменную окружения DATABASES_URL в файле .env.

## Использование

1. Вход в админку по адресу имя_сайта/admin. 

[Пример админки на демосайте](https://iba.pythonanywhere.com/admin).

2. Быстрое добавление одной или нескольких локаций из файлов JSON:

В консоли ввести команду
```
python3 manage.py load_place url [url] ...
```
где url - ссылка на JSON файл.

*Пример корректного файла JSON:*
```
{
    "title": "Экскурсионный проект «Крыши24.рф»",
    "imgs": [
        "https://kudago.com/media/images/place/d0/f6/d0f665a80d1d8d110826ba797569df02.jpg",
        "https://kudago.com/media/images/place/66/23/6623e6c8e93727c9b0bb198972d9e9fa.jpg",
        "https://kudago.com/media/images/place/64/82/64827b20010de8430bfc4fb14e786c19.jpg",
    ],
    "description_short": "Хотите увидеть Москву с высоты птичьего полёта?",
    "description_long": "<p>Проект «Крыши24.рф» проводит экскурсии ...</p>",
    "coordinates": {
        "lat": 55.753676,
        "lng": 37.64
    }
}
```

[Тестовые данные в формате JSON](https://github.com/devmanorg/where-to-go-places)

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

Тестовые данные взяты с сайта [KudaGo](https://kudago.com).

