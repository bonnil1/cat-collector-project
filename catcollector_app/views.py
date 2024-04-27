from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.
def home(request):
    #res.send("hello") in express
    #return HttpResponse("hello there!!!")
    return render(request, 'cats/home.html')

def about(request):
    return render(request, 'cats/about.html')
