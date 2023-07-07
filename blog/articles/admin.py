from django.contrib import admin
from . import models
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','published','author')
    search_fields=('title',)
    sortable_by=('published')

admin.site.register(models.article,ArticleAdmin)
