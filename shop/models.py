from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Cart(models.Model):
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f'cart {self.id}'


class Record(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    num = models.IntegerField('数量')

    def __str__(self):
        return f'{self.item.name} x {self.num}'


class Myuser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
