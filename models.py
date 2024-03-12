from django.db import models


class NewsCategoryModel(models.Model):
    news_category_title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.news_category_title

    class Meta:
        verbose_name = "News category"
        verbose_name_plural = "News categories"


class NewsModel(models.Model):
    news_title = models.CharField(max_length=50)
    news_category = models.ForeignKey(NewsCategoryModel, on_delete=models.CASCADE)
    news_count = models.IntegerField()
    news_descriptions = models.TextField()
    news_image = models.FileField(upload_to="news_images")
    news_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.news_title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
