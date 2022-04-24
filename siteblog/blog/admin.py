from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    save_on_top = True
    list_display = ('id', 'title', 'author', 'category', 'created_at', 'get_photo')
    list_display_links = ('id', "title")
    search_fields = ('title', 'author')
    list_filter = ('created_at', 'category', 'tags')
    readonly_fields = ('views', 'created_at', 'get_photo')
    save_on_top = True
    fields = ('title', 'slug', 'author', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at',)

    def get_photo(self, obj):  # метод для показывания фото в админке
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return 'Фото не установлено'

    get_photo.short_description = 'Миниатюра'  # меняем имя в админке, метода get_photo


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)