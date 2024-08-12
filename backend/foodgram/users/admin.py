from django.contrib import admin
from users.models import Subscriber, User

admin.site.empty_value_display = 'None'
admin.site.site_header = 'Foodgram Admin'
admin.site.site_title = 'Foodgram Admin Portal'
admin.site.index_title = 'Welcome to Foodgram admin panel'


@admin.action(description='Удалить пользователя')
def delete(modeladmin, request, obj):
    obj.delete()


@admin.display(description='Имя')
def upper_case_name(obj):
    return f'{obj.first_name} {obj.last_name}'.title()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', upper_case_name, 'email',)
    search_fields = ('first_name', 'email')
    actions = [delete]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Subscriber, SubscriptionAdmin)
