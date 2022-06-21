from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save
import requests, os
from datetime import datetime
import calendar
# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=CASCADE)

  Followers = models.CharField(max_length=20)
  time = models.CharField(max_length=20)
  username = models.CharField(max_length=40, null=True, blank =True, unique=True )
  No_of_repos = models.IntegerField(null=True, blank=True)

  def __str__(self):
    return self.user.username


class Repos(models.Model):
  owner_of_repo = models.ForeignKey( Profile, on_delete=models.CASCADE, )
  Name_of_repo =  models.CharField(max_length=100)
  No_of_stars = models.IntegerField()

  def __str__(self):
    return self.Name_of_repo


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    prof = Profile.objects.create(user=instance)
    user = instance
    user.profile.username = user.username
    path1 = os.path.join("https://api.github.com/users/", str(user))
    reqprofile = requests.get(path1)
    reqprofile_json = reqprofile.json()
    follower = reqprofile_json['followers']
    updation_time = reqprofile_json['updated_at']
    
    path3 = str(user) + "/repos"
    path2 = os.path.join("https://api.github.com/users/", path3)

    response = requests.get(path2)
    print(path2)
    json_response = response.json()
    print (response.text)
  
    for i in range(len(json_response)):
        repository = json_response[i]
        Repos.objects.create(owner_of_repo = prof, Name_of_repo = repository["name"], No_of_stars = repository["stargazers_count"] )

    user.profile.Followers = follower
    user.profile.time = updation_time
    user.profile.No_of_repos = len(json_response)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()


