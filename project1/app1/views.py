from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    return render(request, 'home.html')
      # return HttpResponse('Hello, World')


def about_page(request):
    return render(request, 'about.html')

def contacts_page(request):
    return render(request, 'contacts.html')













