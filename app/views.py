from asyncio import protocols
import email
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Photo
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
import http.client
import urllib.parse


# Create your views here.
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get("email")
            contact = form.cleaned_data.get('contact')
            credit_card = form.cleaned_data.get('credit_card')
            identification_card = form.cleaned_data.get(
                'identification_card')
            passport = form.cleaned_data.get('passport')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            with connection.cursor() as cursor:  # userid is pk
                cursor.execute("INSERT INTO users (userid,first_name, last_name, email, contact, credit_card, identification_card, passport) VALUES('test2',%s,%s,%s,%s,%s,%s,%s)", [
                    first_name, last_name, email, contact, credit_card, identification_card, passport])

    ##### insert into sql ####

    context = {'form': form}
    return render(request, 'app/register.html', context)


@allowed_users(allowed_roles=['admin'])
def adminPage(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM property ORDER BY city")
        property = cursor.fetchall()

    # Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM property WHERE propertyid = %s", [
                               request.POST['id']])
    if request.GET:
        query = request.GET.get('search')
        if query == '':
            property = property
        else:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM property WHERE country = %s", [
                    query])
                property = cursor.fetchall()
    result_dict = {'records': property}

    return render(request, 'app/adminPage.html', result_dict)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            print(email, password, username)
            print(user)
            if user is not None:
                login(request, user)
                if request.user.groups.all()[0].name == 'admin':
                    return redirect('adminPage')
                else:
                    return redirect('index')
            else:
                messages.info(request, 'email or password is incorrect!')
        else:
            messages.info(request, "please register first!")
    return render(request, 'app/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    """Shows the main page"""
    # Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM property ORDER BY city")
        property = cursor.fetchall()

    # Delete customer
    '''
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM property WHERE propertyid = %s", [
                               request.POST['id']])
    '''
    if request.GET:
        query = request.GET.get('search')
        if query == '':
            property = property
        else:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM property WHERE country = %s", [
                    query])
                property = cursor.fetchall()
    result_dict = {'records': property}

    return render(request, 'app/index.html', result_dict)

# Create your views here.


def view(request, id):
    """Shows the main page"""

    # Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM property WHERE propertyid = %s", [id])
        property = cursor.fetchone()
        cursor.execute(
            "SELECT userid FROM property WHERE propertyid = %s", [id])
        user_id = cursor.fetchone()
        cursor.execute("SELECT * FROM users WHERE userid = %s", [user_id])
        user = cursor.fetchone()

    conn = http.client.HTTPConnection('api.positionstack.com')
    print(property[1])
    params = urllib.parse.urlencode({
        'access_key': '13313c42d97f227972d164fce0a81f4f',
        'query': property[1],
        'region': property[2],
        'limit': 1,
    })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = res.read()
    res = data.decode('utf-8')
    print(res)
    lat = float(res[21:29])
    long = float(res[42:52])

    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE property SET latitude=%s WHERE propertyid = %s", [lat, id])
        cursor.execute(
            "UPDATE property SET longitute=%s WHERE propertyid = %s", [long, id])
    # need handle exceptions
    if Photo.objects.filter(user_id=int(user_id[0])).exists():
        result_dict = {'user': user, 'property': property,
                       'lat': lat, 'long': long, 'pictures': Photo.objects.filter(user_id=int(user_id[0]))}

    else:
        result_dict = {'user': user, 'property': property,
                       'lat': lat, 'long': long}
    print(result_dict)
    return render(request, 'app/view.html', result_dict)

# Create your views here.


def addimage(request, id):
    categories = Category.objects.all()
    print(id)

    with connection.cursor() as cursor:
        cursor.execute("SELECT userid FROM users WHERE userid = %s", [id])
        user_id = cursor.fetchone()

    if request.POST:
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['createcategory'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            desc=data['description'],
            image=image,
            user_id=int(user_id[0])
        )
    context = {'categories': categories}
    return render(request, 'app/addimage.html', context)


@login_required(login_url='login')
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        # Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM users WHERE email = %s",
                           [request.POST['email']])
            user = cursor.fetchone()
            # No customer with same id
            if user == None:
                # TODO: date validation
                cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s)", [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                                                                                 request.POST['lat'], request.POST['long']])
                return redirect('index')
            else:
                status = 'user with email %s already exists' % (
                    request.POST['email'])

    context['status'] = status

    return render(request, "app/add.html", context)


def locate(request, id):
    '''show location of id'''
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        user = cursor.fetchone()
    result_dict = {"user": user}
    return render(request, 'app/locate.html', result_dict)

# Create your views here.


def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        # TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET first_name = %s, last_name = %s, email = %s, lat = %s , long = %s WHERE email = %s", [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                                                                                                                                   request.POST['lat'], request.POST['long'], id])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM users WHERE email = %s", [id])
            obj = cursor.fetchone()

    context["obj"] = obj
    context["status"] = status

    return render(request, "app/edit.html", context)
