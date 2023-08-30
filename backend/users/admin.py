from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email',
                    'recipes_count',
                    'subscribers_count')
    list_filter = ('email', 'first_name')

    def recipes_count(self, obj):
        return obj.recipes.count()

    def subscribers_count(self, obj):
        return obj.author.count()


admin.site.register(User, UserAdmin)
