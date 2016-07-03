from django.db import models

# Create your models here.

class publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    website = models.URLField()
    def __str__(self):
        return "%s" %(self.name)

class author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    def __str__(self):
        return "%s" %(self.first_name+self.last_name)


class book(models.Model):
    title = models.CharField(max_length=100)
    # 一个作者可以对应多本书，一本书也可以对应多个作者
    authors = models.ManyToManyField(author)
    # 一本书只能对应一个出版社，采用外键
    publisher = models.ForeignKey(publisher)
    publisher_date = models.DateField()
    def __str__(self):
        return "%s %s" %(self.title)