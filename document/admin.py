from django.contrib import admin
from document.models import *

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

admin.site.register(Document, DocumentAdmin)

class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'index']

admin.site.register(Section, SectionAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content']

admin.site.register(Content, ContentAdmin)


