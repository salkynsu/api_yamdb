# api_yamdb

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). 
Произведения делятся на категории: (Categories). 
Произведению также может быть присвоен жанр (Genre).
Сами произведения не хранятся в YaMDB.
Пользователи оставляют к произведениям текстовые отзывы (Review) 
и ставят произведению оценку в диапазоне от одного до десяти (целое число); 
из пользовательских оценок формируется усреднённая оценка произведения — 
рейтинг (целое число). 
На одно произведение пользователь может оставить только один отзыв.

У проекта есть backend, API, нет frontend.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:salkynsu/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver

```
По адресу http://127.0.0.1:8000/redoc/ можно найти документацию к API.
