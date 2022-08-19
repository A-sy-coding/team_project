from django.contrib import admin
from . models import Profile
@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'user_pw',
        'user_name',
        'user_email',
        'user_register_dttm',
    )


# Register your models here.
