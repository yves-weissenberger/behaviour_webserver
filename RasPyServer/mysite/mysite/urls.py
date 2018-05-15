"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""


#This is accessed first, because it is pointed to in the root_urlconf setting.


from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    #each URL pattern has 2 or more arguments. The first argument is a regex
    #django starts at the first regular expression and makes its way down this
    #list looking for matches to the requested site by the browser
    #The second argument is the view function that is called when there is a regex
    #match. Common third agument is just the name
######url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^getData/',include('getData.urls',namespace="getData")),   
    url(r'^polls/', include('polls.urls',namespace="polls")),  
    #the namespace makes sure that search in polls subdirectories only
    url(r'^admin/', include(admin.site.urls)), 

#the include function basically appends other, specified url.py files
]
