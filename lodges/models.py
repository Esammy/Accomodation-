from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import secrets
import numpy as np
import datetime
import os

class Lodge(models.Model):
    name = models.CharField(max_length=200, null=True)
    homeImg = models.ImageField(default='Profile-Photo-Place-Holder.PNG', upload_to='home_img', null=True, blank=True)
    elec_water = models.CharField(default='Stable Electricity and Water', max_length=200)
    distance = models.CharField(default='200 meters from school', max_length=200)
    price = models.FloatField()

    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.homeImg.url
        except:
            url = ''
        return url


class LodgeProperties(models.Model):
    lodge = models.OneToOneField(Lodge, on_delete=models.CASCADE)
    sorrounding = models.ImageField(upload_to='home_img', null=True, blank=True)
    lodge_interior = models.ImageField(upload_to='home_img', null=True, blank=True)
    roomFront = models.ImageField(upload_to='home_img', null=True, blank=True)
    roomBack = models.ImageField(upload_to='home_img', null=True, blank=True)
    roomKitchen = models.ImageField(upload_to='home_img', null=True, blank=True)
    roomToiletBath = models.ImageField(upload_to='home_img', null=True, blank=True)
    bedRoom = models.ImageField(upload_to='home_img', null=True, blank=True)

    roomsTotalNum = models.PositiveSmallIntegerField()
    roomsAvailable = models.PositiveSmallIntegerField()


    def __str__(self):
        return str(self.lodge)

    @property
    def sorroundingImageURL(self):
        try:
            url = self.sorrounding.url
        except:
            url = ''
        return url

    @property
    def lodge_interiorImageURL(self):
        try:
            url = self.lodge_interior.url
        except:
            url = ''
        return url

    @property
    def roomFrontImageURL(self):
        try:
            url = self.roomFront.url
        except:
            url = ''
        return url

    @property
    def roomBackImageURL(self):
        try:
            url = self.roomBack.url
        except:
            url = ''
        return url

    @property
    def roomKitchenImageURL(self):
        try:
            url = self.roomKitchen.url
        except:
            url = ''
        return url

    @property
    def toiletRoomImageURL(self):
        try:
            url = self.bedRoom.url
        except:
            url = ''
        return url           

    @property
    def bedRoomImageURL(self):
        try:
            url = self.bedRoom.url
        except:
            url = ''
        return url      

class Profile(models.Model):

    level_choice = (
        ('100L','100L'),
        ('200L','200L'),
        ('300L','300L'),
        ('400L','400L'),
        ('500L','500L')
        )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='profile_pics')
    uni_level = models.CharField(max_length=200, choices = level_choice, default = level_choice[0][1])
    phone_number = models.IntegerField(null=True)
    email = models.EmailField(default= 'egwusamuel2015@gmail.com')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class NewPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lodge_name = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    email = models.EmailField()
    date_created = models.DateTimeField(default = datetime.date.today)

    def __str__(self):
        return f'{self.user.username}'

class AgentPersonalInfo(models.Model):
    state_choice = (
        ("abuja", "Abuja"), ("abia","Abia"),
        ("adamawa","Adamawa"),("anambra","Anambra"),
        ("akwa Ibom","Akwa Ibom"),("bauchi","Bauchi"),
        ("bayelsa","Bayelsa"),("benue","Benue"),("borno","Borno"),
        ("cross River","cross River"),("delta","Delta"),
        ("ebonyi","Ebonyi"),("edo","Edo"),("ekiti","Ekiti"),
        ("enugu","Enugu"),("gombe","Gombe"),("imo","Imo"),
        ("jigawa","Jigawa"),("kaduna","Kaduna"),("kano","Kano"),
        ("katsina","Katsina"),("kebbi","kebbi"),
        ("kogi","Kogi"),("kwara","Kwara"),("lagos","Lagos"),
        ("nassarawa","Nassarawa"),("niger","Niger"),("ogun","Ogun"),
        ("ondo","Ondo"),("osun","Osun"),("oyo","Oyo"),
        ("plateau","Plateau"),("rivers","Rivers"),
        ("sokoto","Sokoto"),("taraba","Taraba"),
        ("yobe","Yobe"), ("zamfara","Zamfara")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    agent_fname = models.CharField(max_length=200)
    agent_lname = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    phone_number2 = models.IntegerField(null=True, blank=True)
    agent_email = models.EmailField()
    home_address1 = models.CharField(max_length=500) 
    home_address2 = models.CharField(max_length=500, null = True, blank = True)
    state = models.CharField(max_length=200, choices = state_choice) 
    
    
    def __str__(self):
        return self.agent_fname +' '+ self.agent_lname


# def get_upload_path(instance, filename):
#     return 'documents/{0}/{1}'.format(instance.user.username, filename)

class AgentProperties(models.Model):

    

    agent_ersonal_info = models.ForeignKey(AgentPersonalInfo,  on_delete=models.CASCADE)

    lodge_name = models.CharField(max_length=200, null=True)
    

    homeImg = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='agent_img')
    sorrounding = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='agent_img')
    lodge_interior = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='agent_img')
    roomFront = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='agent_img')
    roomBack = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='agent_img')
    roomKitchen = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='agent_img')
    roomToiletBath = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='agent_img')
    bedRoom = models.ImageField(default='Profile-Photo-Place-Holder.png', upload_to='agent_img')
    price = models.FloatField()
    elec_water = models.CharField(default='Stable Electricity and Water', max_length=200)
    distance = models.CharField(default='200 meters from school', max_length=200)
    roomsTotalNum = models.PositiveSmallIntegerField()
    roomsAvailable = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lodge_name

class Pop_searched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    searched = models.CharField(max_length=200)

    def __str__(self):
        return self.searched

class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name