from django.contrib import admin
from .models import Game, Buyer, News

# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title','cost','size',) # Поля для отображения в списке
    list_filter = ('size', 'cost')
    search_fields = ('title',) # Поля для поиска
    list_per_page = 20


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'age',)
    list_filter = ('balance', 'age')
    search_fields = ('name',)
    list_per_page = 30

    # Разбиение полей на секции
    fieldsets = (
        (None, {
            'fields': ('name', 'balance', 'age','email')
        }),
        ('Дополниельные настройки',{
            'classes': ('collapse',),
            'fields': ('message', 'subscribe',)
        }),
    )

    # Только для чтения полей balance
    readonly_fields = ('balance',)

admin.site.register(News)