from django.contrib import admin

# Register your models here.
from .models import Cart, Item, Record, Myuser
admin.site.register(Item)
# admin.site.register(Record)


class RecordInline(admin.StackedInline):
    model = Record
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = [RecordInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(Myuser)
