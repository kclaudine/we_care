from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='images/', default='a.png')


    def __str__(self):
         return self.user.username

    @receiver(post_save, sender=User)
    def save_user(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def delete_user(self):
        self.delete()
         

class House( models.Model):

    ACTION = (
        ('Renting','Renting'),
        ('Selling','Selling'),
    )

    TYPE = (
        ('House','House'),
        ('Apartment','Apartment'),
    )

    type    = models.CharField(max_length=800,choices=TYPE, default='House')
    description    = models.TextField(blank=True, null=True,)
    image      = models.ImageField(upload_to='contents',null=True)
    masseuse_name=models.CharField(max_length=800, blank=True, null=True,)
    district    = models.CharField(max_length=800)
    sector    = models.CharField(max_length=800)
    map    = models.CharField(max_length=800, default='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3987.460324616631!2d30.10826551379186!3d-1.9699443985638305!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x19dca64fc7cb6bdd%3A0x1217fae35e7296d7!2sKK%2012%20Ave%2C%20Kigali!5e0!3m2!1sen!2srw!4v1616058045674!5m2!1sen!2srw')
    published_date = models.DateField(auto_now_add=True)
    beds = models.PositiveIntegerField(default=0)
    baths = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    action = models.CharField(max_length=10, choices=ACTION, default='Renting')
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='Houses')


    def __str__(self):
        return self.masseuse_name

    class Meta:
        ordering = ["-pk"]

    @classmethod
    def search_house(cls,search):
    	house = cls.objects.filter(type__icontains=search)
    	return house

class Booking(models.Model):
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=100, null=False)
    booking_date   = models.DateTimeField(auto_now_add = True)
    therapist_name = models.CharField(max_length=50, null=True)
    house = models.ForeignKey(House,on_delete=models.CASCADE, related_name='house')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-pk"]



