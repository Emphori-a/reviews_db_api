from django.contrib import admin
from .models import Category, Comment, Genre, Review, Title

from django.contrib import admin

from .models import Category, Genre, Title

admin.site.empty_value_display = 'Не задано'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category')
    list_editable = ('description', 'category')
    search_fields = ('name',)
    list_display_links = ('name',)
    list_filter = ('genre', 'category')
    filter_horizontal = ('genre',)
    list_per_page = 10


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (TitleInline,)
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('slug',)
    list_per_page = 10


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ('slug',)
    list_per_page = 10

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass