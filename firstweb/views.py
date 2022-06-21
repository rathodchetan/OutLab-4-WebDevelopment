from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.shortcuts import  render, redirect
from .forms import RegistrationForm
from .models import Profile, Repos
import os, requests

def explore(request):
 Profiles  = list(Profile.objects.values())
 allprofile =[]
 for prof in Profiles:
  profile = Profile.objects.filter(username=prof['username'])
  allprofile.append( [ str(os.path.join("/webdev/ALLProfile/", prof['username'] ) ), profile[0] ] )
 return render(request, 'registration/Explore.html', {'allprofile': allprofile} )
 
                                
def register(request):
 if request.method == 'POST':
  form = RegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   form = RegistrationForm()
   return render(request, 'registration/register.html', {'form': form} )
 else :
  form = RegistrationForm()
 return render(request, 'registration/register.html', {'form': form} )

def myprofile(request):
 if request.user.is_authenticated:
  website = os.path.join("https://github.com/",request.user.username)
  return render(request, 'registration/myprofile.html', {'profile': request.user.profile, 'repos': Repos.objects.filter(owner_of_repo=request.user.profile).order_by('-No_of_stars'), 'website' : website } )
 else:
  return redirect('home')

def allprofile(request, usernm):
 website = os.path.join("https://github.com/", usernm)
 profile = Profile.objects.filter(username=usernm)
 repo = Repos.objects.filter(owner_of_repo=request.user.profile)
 print( profile, request.user.profile.username, repo)
 return render(request, 'registration/profile.html', {'profiles': profile , 'repos': Repos.objects.filter(owner_of_repo=profile[0]).order_by('-No_of_stars'), 'website' : website } )
 

def update(request):
 if request.user.is_authenticated:
  user = request.user
  path1 = os.path.join("https://api.github.com/users/", str(user))
  reqprofile = requests.get(path1)
  reqprofile_json = reqprofile.json()
  follower = reqprofile_json['followers']
  updation_time = reqprofile_json['updated_at']

  path3 = str(user) + "/repos"
  path2 = os.path.join("https://api.github.com/users/", path3)
  response = requests.get(path2)
  json_response = response.json()

  repoall = list(Repos.objects.filter( owner_of_repo=user.profile ).values())
  for repos in repoall :
   del_repo = True
   for i in range(len(json_response)):
    if ( json_response[i]['name'] == repos['Name_of_repo'] ):
      del_repo = False
      break
   if del_repo :
     Repos.objects.filter( owner_of_repo=user.profile , Name_of_repo=repos['Name_of_repo']).delete() 

  for i in range(len(json_response)):
   repository = json_response[i]
   if (Repos.objects.filter(Name_of_repo=repository['name']).exists()) :
    repo =  Repos.objects.filter(Name_of_repo=repository['name'])
    repo[0].No_of_stars = repository["stargazers_count"]
   else :
    Repos.objects.create(owner_of_repo = user.profile , Name_of_repo = repository["name"], No_of_stars = repository["stargazers_count"] )

  user.profile.Followers = follower
  user.profile.time = updation_time
  user.profile.No_of_repos = len(json_response)
  user.profile.save()
  request.user.save()
  request.user.profile.save()
  website = os.path.join("https://github.com/",request.user.username)
  return render(request, 'registration/myprofile.html', {'profile': request.user.profile, 'repos': Repos.objects.filter(owner_of_repo=request.user.profile), 'website' : website } )
 else:
  return redirect('home')