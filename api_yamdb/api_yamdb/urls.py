from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]













# http://127.0.0.1:8000/api/v1/auth/signup/

# Дописать пути к твоим эндпоинтам
# их 3 штуки:
# /api/v1/auth/signup/      /api/v1/auth/token/     /api/v1/users/me/

# здесь особенно много:
# Спринт 10/18 → Тема 1/3: Django Rest Framework → Урок 13/15
# https://practicum.yandex.ru/learn/backend-developer/courses/f1186d60-6f68-4f7a-8416-b6b3b7be0d38/sprints/134545/topics/a63bb0d7-efa4-48fd-bb26-5c0770cd58cd/lessons/8025b67d-0c6d-4de6-9042-f4abe75ba386/

# Авторизация по токену
# https://practicum.yandex.ru/learn/backend-developer/courses/f1186d60-6f68-4f7a-8416-b6b3b7be0d38/sprints/134545/topics/a63bb0d7-efa4-48fd-bb26-5c0770cd58cd/lessons/8025b67d-0c6d-4de6-9042-f4abe75ba386/
# Спринт 10/18 → Тема 1/3: Django Rest Framework → Урок 13/15
