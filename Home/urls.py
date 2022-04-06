"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.index, name='index'),
    path('add/<str:id>', app.views.add, name='add'),
    path('login', app.views.loginPage, name='login'),
    path('logout', app.views.logoutUser, name='logout'),
    path('register', app.views.register, name='register'),
    path('view/<str:id>', app.views.view, name='view'),
    path('adminPage', app.views.adminPage, name='adminPage'),
    path('exchange/<str:id>', app.views.exchange, name='exchange'),
    path('manage/<str:id>', app.views.manage, name='manage'),
    path('options/<str:id>', app.views.options, name='options'),
    path('myexchange/<str:id>', app.views.myexchange, name='myexchange'),
    path('complaint/<str:id>', app.views.complaint, name='complaint'),
    path('profile/<str:id>', app.views.profile, name='profile'),
    #path('view/locate/<str:id>', app.views.locate, name='locate')
    path('edit/<str:id>', app.views.edit, name='edit'),
    path('view/addimage/<str:id>', app.views.addimage, name='addimage'),
    path('population-chart/', app.views.population_chart, name='population-chart'),
    path('property-chart/', app.views.property_chart, name='property-chart'),
    path('aduser', app.views.aduser, name='aduser'),
    path('adviewproperty/<str:id>',
         app.views.adviewproperty, name='adviewproperty'),
    path('adproperty', app.views.adproperty, name='adproperty'),
    path('adcase', app.views.adcase, name='adcase'),
    path('adexchange', app.views.adexchange, name='adexchange')
    # path('locate/<str:id>',app.views.locate,name='locate'),
]
