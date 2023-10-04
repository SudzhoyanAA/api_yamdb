### Описание
Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка»
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.


## Стек технологий

- Django v3.2 - используемый фреймворк
- Django REST Framework v.3.12.4 - библиотека для работы с REST API
- Simple JWT(djangorestframework-simplejwt v.4.7.2) - работа с JWT-токеном
- django-filter v2.4.0 - библиотека для работы с фильтрами в Django

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:SudzhoyanAA/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
Linux/macOS: python3 -m venv venv;
Windows: python -m venv venv или py -3 -m venv venv
```

```
Linux/macOS: source venv/bin/activate;
Windows: source venv/Scripts/activate.
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
py manage.py migrate
```

Запустить проект:

```
Windows: python manage.py runserver
Linux/macOS: python3 manage.py runserver
```


### Некоторые примеры из API.

```
Информация о произведении Права доступа: Доступно без токена
REQUEST: GET http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Content-Type: application/json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

```
Регистрация пользователя.

REQUEST: POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json
{
	"email": "user@example.com",
	"username": "string"
}
```



### Авторство

Проект выполнен группой №5, состоящей из:
Ольги Степановой, которая работала с аунтентификацией и пользователями
Альберта Суджояна, который работал с категориями, жанрами и произведениями
Матвея Сухих, который работал с отзывами и комментариями.