from turtle import title
from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User


class newuser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    purchase_history = models.CharField(max_length=10000)

    def __str__(self):
        return self.user.username


'''def update_user_profile(sender, instance, created, **kwargs):
    """
    Signals the Profile about User creation.
    """
    if created:
        newuser.objects.create(user=instance)
    instance.newuser.save()'''


class Product_series(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    photo = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "Tutorial Seriess in admin"
        verbose_name_plural = "series"

    def __str__(self):
        return self.title


class Products(models.Model):
    Name = models.CharField(max_length=200)
    series_title = models.ForeignKey(
        Product_series, default=1, verbose_name='series', on_delete=models.SET_DEFAULT)
    Price = models.DecimalField(max_digits=4, decimal_places=2)
    photo = models.CharField(max_length=200)

    def __str__(self):
        return self.Name
