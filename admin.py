from django.contrib import admin

from .models import NewsCategoryModel, NewsModel


@admin.register(NewsCategoryModel)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ["news_category_title", "created_at"]
    search_fields = ["news_category_title"]
    list_filter = ["created_at"]
    ordering = ["news_category_title"]


@admin.register(NewsModel)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["news_title", "news_created_at"]
    search_fields = ["news_title"]
    list_filter = ["news_created_at"]
    ordering = ["news_title"]
