# Интернет магазин по продаже техники "MEGANO"  
Данный сервис написан на языке **Python**.  
Использует framework **Django**, СУБД **SQLite**.  
Страницы отображаются через пакет **diploma-frontend**  
Обращение за данными происходит по **API** с помощью **Django Rest Framework**.  

## Установка и запуск проекта:  
* ```git clone https://gitlab.skillbox.ru/andrei_iaroshenko/Python_django_diploma_dpo.git```, создать виртуальное ```venv``` окружение  
* ```pip install -r megano/requirements.txt``` - установка зависимостей  
### Установка diploma-frontend:  
* ```cd diploma-frontend && python setup.py sdist``` - собираем пакет  
* ```pip install ./dist/diploma-frontend-0.6.tar.gz``` - установка полученного пакета в виртуальное окружение  
### Создание бд и загрузка фикстур:  
* ```cd ../megano && python manage.py makemigrations``` - создание миграций  
* ```python manage.py migrate``` - миграция  
* ```python manage.py loaddata ./fixtures/*```  - установка фикстур  
* ```python manage.py runserver``` - запуск сервиса  

В фикстурах собраны товары, заказы, категории и т.д.  
Так же суперпользователь и обычный зарегистрированный пользователь:  


Логин для входа| Пароль | Группа    |
---------------|--------|-----------|
admin          | 123    | superuser |
bob            | 123    | user      |
