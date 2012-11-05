from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

from contacts.models import Person


class PersonAdmin(admin.ModelAdmin):
    inlines = [
    ]
    
    list_display_links = ('first_name', 'last_name',)
    list_display = ('first_name', 'last_name',)
    list_filter = ('last_name',)
    ordering = ('last_name', 'first_name')
    search_fields = ['^first_name', '^last_name']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}

admin.site.register(Person, PersonAdmin)
