from django.db import models


class Recipe(models.Model):
    creator = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    description = models.TextField()
    image_url = models.URLField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
