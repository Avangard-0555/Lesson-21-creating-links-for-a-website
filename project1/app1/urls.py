from django.urls import path
from . import views
#from . project1.urls import urlpatterns

urlpatterns = [
    path('', views.home_page),
    path('about', views.about_page),
    path('contacts', views.contacts_page)

]















