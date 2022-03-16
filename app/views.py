import email
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def index(request):
    """Shows the main page"""

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE email = %s", [request.POST['email']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY first_name")
        users = cursor.fetchall()

    result_dict = {'records': users}

    return render(request,'app/index.html',result_dict)

# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        user = cursor.fetchone()
    result_dict = {'user': user}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM users WHERE email = %s", [request.POST['email']])
            user = cursor.fetchone()
            ## No customer with same id
            if user == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['lat'] , request.POST['long'] ])
                return redirect('index')    
            else:
                status = 'user with email %s already exists' % (request.POST['email'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

def locate(request,id):
    '''show location of id'''
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        user = cursor.fetchone()
    result_dict = {"user":user}
    return render(request,'app/locate.html',result_dict)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET first_name = %s, last_name = %s, email = %s, lat = %s , long = %s WHERE email = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['lat'] , request.POST['long'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM users WHERE email = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)