from django.db import models

# Create your models here.
class Person(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category',  on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100,db_index=True)

    def __str__(self):
        return self.name