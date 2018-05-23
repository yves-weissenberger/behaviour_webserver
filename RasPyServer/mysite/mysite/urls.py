"""RasPyServer URL Configuration

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
import sys



if sys.version_info[0] < 3:

    urlpatterns = [
        url('',include('getData.urls',namespace="getData")),  
        url(r'^getData/',include('getData.urls',namespace="getData")),   
        #the namespace makes sure that search in polls subdirectories only
        url(r'^admin/', include(admin.site.urls)), 

    ]
else:

        urlpatterns = [
        url('',include(('getData.urls','getDdata'),namespace="getData")),  
        url(r'^getData/',include(('getData.urls','getDdata'),namespace="getData")),   
        #the namespace makes sure that search in polls subdirectories only
        url(r'^admin/', include(('getData.urls','getDdata'),namespace="getData")), 

    #the include function basically appends other, specified url.py files
    ]

