from django.contrib import admin
from .models import Bb, Rubric,  Shop, BbImage, ShopPrice

# Register your models here.
admin.site.register(Rubric)

admin.site.register(Shop)
admin.site.register(ShopPrice)


class BbImageInline(admin.TabularInline):
    model = BbImage
    extra = 1

@admin.register(Bb)
class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'rubric')
    inlines = [BbImageInline]
