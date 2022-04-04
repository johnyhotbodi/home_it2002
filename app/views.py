from asyncio import protocols
import email
from email import message
from pickle import FALSE
from pickletools import read_uint1
import re
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
from string import ascii_letters
from random import choice
from datetime import datetime
from django.db import transaction
from django.urls import reverse
# Create your views here.


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            '''
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get("email")
            country_code = form.cleaned_data.get("country_code")
            contact = form.cleaned_data.get('contact')
            credit_card = form.cleaned_data.get('credit_card')
            identification_card = form.cleaned_data.get(
                'identification_card')
            passport = form.cleaned_data.get('passport')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            '''
            email = form.cleaned_data.get("email")
            country_code = form.cleaned_data.get("country_code")
            contact = form.cleaned_data.get('contact')
            identification_card = form.cleaned_data.get(
                'identification_card')
            passport = form.cleaned_data.get('passport')
            print(type(contact))
            with connection.cursor() as cursor:  # userid is pk
                cursor.execute("SELECT * FROM users WHERE email=%s", [email])
                exist_email = cursor.fetchone()
                print(exist_email)
                if exist_email != None:
                    print("hehe")
                    messages.info(
                        request, 'This email is already connected to another account')
                    return redirect('register')
                cursor.execute(
                    "SELECT * FROM users WHERE contact=%s AND country_code=%s", [str(contact), country_code])
                exist_contact = cursor.fetchone()
                if exist_contact != None:
                    messages.info(
                        request, 'This contact is already connected to another account')
                    return redirect('register')
                cursor.execute(
                    "SELECT * FROM users WHERE identification_card=%s AND country_code=%s", [identification_card, country_code])
                exist_identity = cursor.fetchone()
                if exist_identity != None:
                    messages.info(
                        request, 'This identification card number is already connected to another account')
                    return redirect('register')
                cursor.execute(
                    "SELECT * FROM users WHERE passport=%s AND country_code=%s", [passport, country_code])
                exist_passport = cursor.fetchone()
                if exist_passport != None:
                    messages.info(
                        request, 'This passport number is already connected to another account')
                    return redirect('register')
                print(passport)
                if len(passport) != 8 and len(passport) != 9:
                    print('wrong')
                    messages.info(
                        request, 'Please enter a valid passport (8 to 9 characters)')
                    return redirect('register')
                if (not (country_code == '+65' and len(str(contact)) == 8) and not(country_code == '+66' and len(str(contact)) == 8) and not(country_code == '+60' and (len(str(contact)) == 9 or len(str(contact)) == 10))):
                    messages.info(
                        request, 'Please enter a valid contact number')
                    return redirect('register')
                if country_code != '+60' and country_code != '+65' and country_code != '+66':
                    messages.info(
                        request, 'Please enter +60/+65/+66 for country code')
                    return redirect('register')
                else:
                    print('haha')

                    user = form.save()
                    username = form.cleaned_data.get('username')
                    first_name = form.cleaned_data.get("first_name")
                    last_name = form.cleaned_data.get('last_name')
                    email = form.cleaned_data.get("email")
                    country_code = form.cleaned_data.get("country_code")
                    contact = form.cleaned_data.get('contact')
                    credit_card = form.cleaned_data.get('credit_card')
                    identification_card = form.cleaned_data.get(
                        'identification_card')
                    passport = form.cleaned_data.get('passport')

                    group = Group.objects.get(name='customer')
                    user.groups.add(group)
                    cursor.execute("INSERT INTO users (userid,first_name, last_name, email, country_code, contact, credit_card, identification_card, passport) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", [
                        username, first_name, last_name, email, country_code, contact, credit_card, identification_card, passport])
                    return redirect('login')

    context = {'form': form}
    return render(request, 'app/register.html', context)


@ allowed_users(allowed_roles=['admin'])
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


@ unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print('email:', email)
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
            print('haha')
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
    return render(request, 'app/trylogin2.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@ login_required(login_url='login')
def index(request):
    """Shows the main page"""
    # Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM property WHERE userid <> %s AND active=true ORDER BY country", [request.user.username])
        property = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM pending WHERE requested_to = %s", [request.user.username])
        pendings = cursor.fetchall()
    # print(pendings[0][0])
    # Delete customer
    '''
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM property WHERE propertyid = %s", [
                               request.POST['id']])
    '''
    if request.GET:
        country = request.GET.get('country')
        start_date = request.GET.get('startdate')
        end_date = request.GET.get('enddate')
        print('first:', start_date, end_date)

        if start_date != '':
            print('check')
            if re.search("^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d\d$", start_date) != None:
                print('check2')
                start_date = datetime.strptime(start_date, '%d/%m/%y').date()
                print(start_date)
            else:
                messages.info(
                    request, "Please enter valid start date")
                return redirect('index')
        if end_date != '':
            if re.search("^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d\d$", start_date) != None:
                print('check2')
                end_date = datetime.strptime(end_date, '%d/%m/%y').date()
                print(start_date)
            else:
                messages.info(
                    request, "Please enter valid end date")
                return redirect('index')
        if start_date == '':
            start_date = datetime.strptime('1/1/80', '%d/%m/%y').date()
        if end_date == '':
            end_date = datetime.strptime('31/12/50', '%d/%m/%y').date()
        print("second", start_date, end_date)
        if start_date > end_date:
            property = property
            messages.info(
                request, "Please enter valid start date and end date")

        elif country == '':
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM property WHERE active=true  AND start_available >=%s
                AND end_available <= %s  AND userid<>%s''', [
                    start_date, end_date, request.user.username])
                property = cursor.fetchall()
                print('property:', property)

        else:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * FROM property WHERE active=true AND country = %s AND (start_available >=%s)
                AND (end_available <=%s )AND userid<>%s''', [country, start_date, end_date, request.user.username])
                property = cursor.fetchall()
    result_dict = {'records': property, 'pendings': pendings}
    return render(request, 'app/index.html', result_dict)

# Create your views here.


@ login_required(login_url='login')
def view(request, id):
    """Shows the main page"""

    # Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM property WHERE propertyid = %s", [id])
        property = cursor.fetchone()
        cursor.execute(
            '''SELECT * FROM users WHERE userid IN (
            SELECT userid FROM property WHERE propertyid = %s)''', [id])
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
    '''
    if Photo.objects.filter(user_id=int(user_id[0])).exists():
        result_dict = {'user': user, 'property': property,
                       'lat': lat, 'long': long, 'pictures': Photo.objects.filter(user_id=int(user_id[0]))}
    '''
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


@ login_required(login_url='login')
def add(request, id):
    """Shows the main page"""
    context = {}
    # status = ''
    print(id)
    if request.POST:
        propertyid = str(id) + request.POST['address']
        propertyid = propertyid.replace(" ", "")
        # Check if propertyid is already in the table
        address_post = request.POST['address']
        try:
            start_date = datetime.strptime(
                request.POST['startdate'], '%d/%m/%y').date()
            end_date = datetime.strptime(
                request.POST['enddate'], '%d/%m/%y').date()
        except:
            messages.info(request, "Please enter your date in dd/mm/yy")
            start_date = datetime.strptime(
                request.POST['startdate'], '%d/%m/%y').date()
            end_date = datetime.strptime(
                request.POST['enddate'], '%d/%m/%y').date()
        finally:
            if start_date > end_date:
                messages.info(request, 'Please enter valid start and end date')
            else:
                with connection.cursor() as cursor:
                    print('insert')
                    cursor.execute(
                        "SELECT * FROM property WHERE address = %s", [address_post])
                    flag = cursor.fetchone()
                    house = request.POST.get("housetype")
                    if flag == None:
                        print('inserting')
                        print(house)
                        cursor.execute('''INSERT INTO property(propertyid, address,city,country,house_type,number_of_bedrooms,
                        number_of_guests_allowed,start_available,end_available,house_rules,amenities,userid)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                       [propertyid, request.POST['address'], request.POST['city'], request.POST['country'],
                                        house, request.POST['bedrooms'], request.POST['guest'], start_date,
                                        end_date, request.POST['rules'], request.POST['amenities'], id])
                        messages.info(
                            request, 'Your property is successfully listed!')
                        return redirect('index')
                    else:
                        messages.info(
                            request, 'This property is already listed :(')

        '''
        if start_date and end_date:
            with connection.cursor() as cursor:
                address_exist = cursor.execute(
                    "SELECT * FROM property WHERE address = %s", [address_post])
                flag = cursor.fetchone()
                house = request.POST.get("housetype")
                if house == None:
                    house = 'other'
                if flag == None:
                    cursor.execute('INSERT INTO property(propertyid, address, city, country, house_type, number_of_bedrooms,
                                                           number_of_guests_allowed, start_available, end_available, house_rules, amenities, userid)
        VALUES( % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)',
                                   [propertyid, request.POST['address'], request.POST['city'], request.POST['country'],
                                    house, request.POST['bedrooms'], request.POST['guest'], start_date,
                                    end_date, request.POST['rules'], request.POST['amenities'], id])
                    messages.info(
                        request, 'Your property is successfully listed!')
                    return redirect('index')
                else:
                    messages.info(
                        request, 'This property is already listed :(')
    # context['status'] = status
    '''
    return render(request, "app/tryadd2.html", context)


@ login_required(login_url='login')
def exchange(request, id):
    if request.POST:
        start = request.POST['startdate']
        end = request.POST['enddate']
        if re.search("^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d\d$", start) != None:
            print('check2')
            start = datetime.strptime(start, '%d/%m/%y').date()
            print(start)
        else:
            messages.info(
                request, "Please enter valid start date")
            redirect_to = '/exchange/'+id
            return redirect(redirect_to)

        if re.search("^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d\d$", end) != None:
            print('check2')
            end = datetime.strptime(end, '%d/%m/%y').date()
            print(end)
        else:
            messages.info(
                request, "Please enter valid end date")
            redirect_to = '/exchange/'+id
            return redirect(redirect_to)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT userid FROM property WHERE propertyid = %s", [id])
            ownerid = cursor.fetchone()
            cursor.execute(
                "SELECT start_available FROM property WHERE propertyid = %s", [id])
            owner_start = cursor.fetchone()
            cursor.execute(
                "SELECT end_available FROM property WHERE propertyid = %s", [id])
            owner_end = cursor.fetchone()
            # owner_end = datetime.strptime(owner_end, '%d/%m/%y').date()

            print(start < owner_end[0], start > owner_start[0],
                  end > owner_start[0], end < owner_end[0])
            # print(owner_end[0], type(owner_end[0]))
            cursor.execute("SELECT propertyid FROM property WHERE userid = %s", [
                           request.user.username])
            prop = cursor.fetchone()
            if prop == None:
                messages.info(request, "Please list your property first!")
                redirect_to = '/exchange/'+id
                return redirect(redirect_to)

            if (not(start <= owner_end[0] and start >= owner_start[0] and end >= owner_start[0] and end <= owner_end[0])):
                messages.info(
                    request, "The owner is not available on the proposed exchange date")
                redirect_to = '/exchange/'+id
                return redirect(redirect_to)

            cursor.execute('''SELECT requested_from,requested_to  FROM pending WHERE requested_from = %s AND requested_to 
            IN(SELECT userid from property WHERE propertyid = %s)''', [
                           request.user.username, id])
            exist_pending = cursor.fetchone()
            if exist_pending != None:
                print(exist_pending)
                messages.info(
                    request, "You already have a pending exchange request with the owner")
                redirect_to = '/exchange/'+id
                return redirect(redirect_to)
            else:
                cursor.execute("INSERT INTO pending VALUES(%s,%s,%s,%s,%s)",
                               [request.user.username, ownerid, id, start, end])
                messages.info(
                    request, "Exchange request submitted!")
    return render(request, 'app/exchange.html')


def locate(request, id):
    '''show location of id'''
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        user = cursor.fetchone()
    result_dict = {"user": user}
    return render(request, 'app/locate.html', result_dict)


# def notification(request, id):

@ login_required(login_url='login')
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM property WHERE propertyid = %s", [id])
        obj = cursor.fetchone()
        cursor.execute(
            "SELECT active FROM property WHERE propertyid = %s", [id])
        active = cursor.fetchone()
    # save the data from the form

    if active == 'false':
        messages.info(request,
                      "Your property is booked currently, you can't change the details now")
        return redirect("app/manage.html")

    context["obj"] = obj
    if request.POST:
        try:
            start_date = datetime.strptime(
                request.POST['startdate'], '%d/%m/%y').date()
            print(start_date)
            end_date = datetime.strptime(
                request.POST['enddate'], '%d/%m/%y').date()
            print(end_date)
            if start_date > end_date:
                messages.info(
                    request, 'Please enter a valid start and end date')
            else:
                with connection.cursor() as cursor:
                    print("haha")
                    cursor.execute("UPDATE property SET number_of_bedrooms= %s, number_of_guests_allowed = %s, start_available= %s, end_available= %s , house_rules= %s ,amenities = %s WHERE propertyid = %s;", [
                        request.POST['bedrooms'], request.POST['accomodate'], start_date, end_date, request.POST['rules'], request.POST['amenities'], id])
                    transaction.commit()
                    messages.info(request, "Property edited successfully!")
        except:
            messages.info(request, "Please enter a valid date format")

    return render(request, "app/edit.html", context)


@ login_required(login_url='login')
def manage(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM property WHERE userid = %s", [id])
        obj = cursor.fetchall()
    print(obj)
    if len(obj) == 0:
        messages.info(request, "You do not have any properties listed")
    if request.POST:
        if request.POST.get("action"):
            if request.POST['action'] == 'delete':
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM property WHERE propertyid = %s", [
                        request.POST['delete']])
                    print('deleted')
                    messages.info(request, "Your property is delisted")
    # save the data from the form

    context["obj"] = obj

    return render(request, "app/manage.html", context)


@ login_required(login_url='login')
def options(request, id):
    print(id)
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM property WHERE userid = %s", [id])
        record = cursor.fetchall()
    context["records"] = record
    context['name'] = id
    if request.POST:
        chosen_id = request.POST.get("acceptance")
        exchangeid = ''.join([choice(ascii_letters) for i in range(16)])
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT *  FROM pending WHERE requested_from = %s AND requested_to = %s", [id, request.user.username])
            res = cursor.fetchone()
            print(res)
            cursor.execute("INSERT INTO exchange (exchangeid,userid1,userid2,propertyid1,propertyid2,start,ends) VALUES(%s,%s,%s,%s,%s,%s,%s)", [
                           exchangeid, res[0], res[1], res[2], chosen_id, res[3], res[4]])
            print('done')
            cursor.execute('''DELETE FROM pending WHERE (requested_from = %s AND requested_to = %s) OR
                             (requested_to = %s OR requested_to = %s)AND ((start_date > %s AND start_date < %s) OR (end_date > %s AND end_date < %s))''', [
                           id, request.user.username, id, request.user.username, res[3], res[4], res[3], res[4]])
            print('done2')

            cursor.execute("UPDATE property SET active=false WHERE propertyid= %s OR propertyid = %s", [
                           res[2], chosen_id])
            messages.info(request, "Your exchange has been activated")
        return redirect('index')
    return render(request, "app/options.html", context)


@ login_required(login_url='login')
def myexchange(request, id):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM exchange WHERE status1='Confirmed' AND(userid1 = %s)", [id])
        ongoing1 = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM exchange WHERE status2='Confirmed' AND(userid2 = %s)", [id])
        ongoing2 = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM exchange WHERE status1='Closed' OR status1='Closed with Complain' AND(userid1 = %s)", [id])
        closed1 = cursor.fetchall()
        cursor.execute(
            "SELECT * FROM exchange WHERE status2='Closed' OR status2='Closed with Complain' AND(userid2 = %s)", [id])
        closed2 = cursor.fetchall()
    if ongoing1 == None and closed1 == None and ongoing2 == None and closed2 == None:
        messages.info(request, "You have no active or past exchanges")
    else:
        print('ongoing1:', ongoing1)
        print('ongoing2:', ongoing2)
        context['ongoing1'] = ongoing1
        context['ongoing2'] = ongoing2
        context['closed1'] = closed1
        context['closed2'] = closed2

    if request.POST:
        ex_id = request.POST.get("end")
        if ex_id != None:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT userid1 FROM exchange WHERE exchangeid = %s', [ex_id])
                user1 = cursor.fetchone()
                cursor.execute(
                    'SELECT userid2 FROM exchange WHERE exchangeid = %s', [ex_id])
                user2 = cursor.fetchone()
                print(request.user.username)
                print(user1)
                print(user2)
                if user1[0] == request.user.username:
                    print('closed1')
                    cursor.execute(
                        "UPDATE exchange SET status1='Closed',deposit_refunded='true'  WHERE exchangeid = %s", [ex_id])
                    cursor.execute('''UPDATE property SET active='true' WHERE propertyid IN 
                    (SELECT propertyid1 FROM exchange WHERE exchangeid = %s )''', [ex_id])
                if user2[0] == request.user.username:
                    print('closed 2')
                    cursor.execute(
                        "UPDATE exchange SET status2='Closed',deposit_refunded='true'  WHERE exchangeid = %s", [ex_id])
                    cursor.execute('''UPDATE property SET active='true' WHERE propertyid IN 
                    (SELECT propertyid2 FROM exchange WHERE exchangeid = %s )''', [ex_id])
                cursor.execute(
                    "UPDATE users SET rating=rating+1, wallet=wallet+450 WHERE userid = %s", [request.user.username])
                print('done3')
                return redirect('index')
        reason = request.POST.get("reason")
        if reason != None:
            print("reason:", reason)
            caseid = ''.join([choice(ascii_letters) for i in range(16)])

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT userid1,userid2 FROM exchange WHERE exchangeid = %s", [reason[0:16]])
                ex = cursor.fetchone()
                print('extract:', ex)
                excom_id = reason[0:16]
                print('excom_id:', excom_id)
                if ex[0] == id:
                    print("closed3")
                    complained = ex[1]
                    print(excom_id)
                    cursor.execute(
                        "UPDATE exchange SET status1='Closed with Complain', deposit_refunded='true'  WHERE exchangeid = %s", [excom_id])
                    cursor.execute('''UPDATE property SET active='true' WHERE propertyid IN 
                    (SELECT propertyid1 FROM exchange WHERE exchangeid = %s )''', [excom_id])
                    print("closed3.1")
                else:
                    print("closed4")
                    complained = ex[0]
                    cursor.execute(
                        "UPDATE exchange SET status2='Closed with Complain', deposit_refunded='true'  WHERE exchangeid = %s", [excom_id])
                    cursor.execute('''UPDATE property SET active='true' WHERE propertyid IN 
                    (SELECT propertyid2 FROM exchange WHERE exchangeid = %s )''', [excom_id])
                print(reason[16:], print(complained))
                cursor.execute("INSERT INTO case_log VALUES(%s,%s,%s,%s,%s)", [
                               caseid, reason[16:], reason[0:16], id, complained])
                print("inserted into case log")
                return redirect('index')
    return render(request, 'app/myexchange.html', context)


@ login_required(login_url='login')
def profile(request, id):
    context = {}
    '''
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE userid=%s", [id])
        user = cursor.fetchone()
    context['user'] = user
    '''
    if request.POST:
        code = request.POST.get("countrycode")
        number = request.POST.get("contact")
        print(code, number)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE country_code = %s AND contact = %s", [code, number])
            num = cursor.fetchone()
            if num != None:
                messages.info(
                    request, "This contact number is already linked to another user")
                print('hehe')
            elif ((code == '+65' or code == '+66') and len(number) != 8) or (code == '+60' and (len(number) != 9 or len(number) != 10)):
                messages.info(request, "Please enter a valid contact number")
                print('hoho')
            else:
                cursor.execute("UPDATE users SET country_code = %s,contact = %s WHERE userid = %s", [
                    code, number, id])
                print('haha')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE userid=%s", [id])
        user = cursor.fetchone()
    context['user'] = user

    return render(request, 'app/profile.html', context)


@ login_required(login_url='login')
def complaint(request, id):
    context = {}
    return render(request, 'app/complaint.html', context)
