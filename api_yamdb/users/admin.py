from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Добавляем поле с биографией
# к стандартному набору полей (fieldsets) пользователя в админке.
UserAdmin.fieldsets += (
    # Добавляем кортеж, где первый элемент — это название раздела в админке,
    # а второй элемент — словарь, где под ключом fields можно указать нужные поля.
    ('Extra Fields', {'fields': ('bio',)}),
)
# Регистрируем модель в админке:
admin.site.register(User, UserAdmin)


# from django.contrib import admin
#
# from .models import User
#
# admin.site.register(User)
