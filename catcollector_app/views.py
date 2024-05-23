import uuid
import boto3
import os
from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Cat, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

"""
#goes below imports
cats = [
  {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
  {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
]
"""

# Create your views here.
def home(request):
    #res.send("hello") in express
    #return HttpResponse("hello there!!!")
    return render(request, 'cats/home.html')

def about(request):
    return render(request, 'cats/about.html')

@login_required
def cats_index(request):
    cats = Cat.objects.filter(user=request.user)
    #passing data is similar to how we did in EJS
    return render(request, 'cats/index.html', {
        'cats': cats
    })

@login_required
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id) #cat_id is from urls.py
    toys = Toy
    id_list = cat.toys.all().values_list('id')
    print(id_list)
    #query for toys whose id(PK) are not in the list using exclude
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    feeding_form = FeedingForm()
    # making an instance of FeedinfForm to render in the template
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have,
    })

@login_required
def add_feeding(request, pk):
    # create a ModelForm instance using data in request.POST (this is like our 'req.body' in Express)
    form = FeedingForm(request.POST)
    #validate
    if form.is_valid():
        # don't save the form to the db until it has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = pk
        new_feeding.save()
    return redirect('detail', cat_id=pk)

@login_required
def assoc_toy(request, pk, toy_pk):
    Cat.objects.get(id=pk).toys.add(toy_pk)
    #associated^^
    return redirect('detail', cat_id=pk)

@login_required
def assoc_delete(request, pk, toy_pk):
    Cat.objects.get(id=pk).toys.remove(toy_pk)
    return redirect('detail', cat_id=pk)

def signup(request):
  error_message = ''
  #if method is a POST request
  if request.method == 'POST':
    # user data from the signup form
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # if our new user is saved!
      user = form.save()
      # log in our newly signed up user
      login(request, user)
      #redirect to the home page
      return redirect('index')
    # if method is a GET request
    else: 
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required # make sure only logged in users can upload!!
def add_photo(request, cat_pk):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, cat_id=cat_pk)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', cat_id=cat_pk)



class CatCreate(CreateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age']

  #inherited method when a valid cat form
  def form_valid(self, form):
    #form instance assigning 'user' field to logged in user
    form.instance.user = self.request.user
    #let the create view do its thing
    return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys'
    

# cat.feeding_set.all() | parent.child_set.all()