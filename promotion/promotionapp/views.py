from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import date
import datetime


User = get_user_model()

@csrf_exempt
def loginpage(request):
    return render(request, 'loginpage.html')
def logoutpage(request):
    promoter_id=request.user.id
    logout(request)
    with connection.cursor() as cursor:
        query = 'UPDATE promotions.users SET is_logged_in = 0 WHERE id = "{}"'.format(promoter_id)
        cursor.execute(query)
        return redirect('loginpage')

@csrf_exempt
def authentication(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        if user.is_active and user.is_superuser:
            return redirect('adminpage')
        elif getattr(user, 'is_user', False):
            return redirect('target_filters')
        else:
            return redirect('promotions')
        
    
    return render(request, 'loginpage.html', {'error':'Invalid username or password'})

def adminpage(request):
    loggedin_user = (request.user)
    return render(request, 'dashboard.html', {'loggedin_user' : loggedin_user})
def promotions(request):
    loggedin_promoter = (request.user)
    return render(request, 'promotions.html',{'loggedin_promoter' : loggedin_promoter})
    
def promoterregistration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('Role')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        company_name = request.POST.get('companyname')
        contact = request.POST.get('contact')

        if role == "Admin":
            is_superuser = True
            is_staff = True
        else:
            is_superuser = False
            is_staff = False
        if age and age.isdigit():
            age = int(age)
        else:
            age = None
        if User.objects.filter(username=username).exists():
            return render(
                request,
                'promoterregistration.html',
                {'error': 'Username already exists'}
            )
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                gender=gender,
                age=age,
                is_user=False,
                companyname=company_name,
                contact=contact,
                is_superuser=is_superuser,
                is_staff=is_staff,
                is_active=False,
                first_name="",
                last_name=""
            )

            return render(
                request,
                'loginpage.html',
                {'success': 'Successfully Created'}
            )
    else:
        return render(request, 'promoterregistration.html')



@csrf_exempt
def list_of_admins(request):
    with connection.cursor() as cursor:
        query='select username from promotions.users where is_superuser = 1'
        cursor.execute(query)
        query_response=cursor.fetchall()
        return render(request, 'list_of_admins.html', {'query_response': query_response})

@csrf_exempt
def list_of_promoters(request):
    print(request.user.is_authenticated)
    with connection.cursor() as cursor:
        query='select id, username, email, age, gender, is_superuser, is_active, is_logged_in, companyname from promotions.users where is_superuser = 0 '
        cursor.execute(query)
        query_response=cursor.fetchall()
        return render(request, 'list_of_promoters.html', {'query_response': query_response})
def list_of_promotions(request):
    current_date = date.today()

    with connection.cursor() as cursor:
        query = '''
            SELECT *
            FROM promotions.promotions
            WHERE start_date <= %s AND end_date >= %s
        '''
        cursor.execute(query, [current_date, current_date])
        query_response = cursor.fetchall()

    return render(
        request,
        'list_of_promotions.html',
        {'query1_response': query_response}
    )

def list_of_promotions_completed(request):
    current_date = date.today()

    with connection.cursor() as cursor:
        query = '''
            SELECT *
            FROM promotions.promotions
            WHERE end_date < %s
        '''
        cursor.execute(query, [current_date])
        query_response = cursor.fetchall()

    return render(
        request,
        'list_of_promotions_completed.html',
        {'query1_response': query_response}
    )
@csrf_exempt
def approve_promoters(request):
    with connection.cursor() as cursor:
        query='UPDATE promotions.users SET is_active = "{}" WHERE id = "{}"'.format(1, request.POST['approve'])
        cursor.execute(query)
        print(query)
    return redirect('list_of_promoters')
@csrf_exempt
def reject_promoters(request):    
    with connection.cursor() as cursor:
        query='update promotions.users set is_active = "{}" where id = "{}"'.format(0, request.POST['reject'])
        cursor.execute(query)
        cursor.execute(query)
        return redirect('list_of_promoters')
@csrf_exempt
def update_promoters(request, promoter_id):
    with connection.cursor() as cursor:
        query='select id, username, email, age, gender, is_superuser, is_active, companyname from promotions.users where id = "{}"'.format(promoter_id)
        cursor.execute(query)
        query_response=cursor.fetchall()
        dict={
            'promoter_id': promoter_id,
            'query_response' : query_response
        }
        
        return render(request, 'update_promoters.html', dict)
@csrf_exempt
@login_required(login_url='loginpage')
def update_promoters_sql(request, promoter_id):
    with connection.cursor() as cursor:
        query1='update promotions.users set email = "{}", gender = "{}", age = "{}", companyname = "{}" where id = "{}"'.format(request.POST.get('email'), request.POST.get('gender'), request.POST.get('age'), request.POST.get('companyname'), promoter_id)
        cursor.execute(query1)
        return redirect('list_of_promoters')
    
#@csrf_exempt
@login_required(login_url='loginpage')
def delete_promoter(request, promoter_id):
    with connection.cursor() as cursor:
        query='delete from promotions.users where id ="{}"'.format(promoter_id)
        cursor.execute(query)
        return redirect('list_of_promoters') 
    
        
@csrf_exempt
@login_required(login_url='loginpage')
def list_of_users(request):
    with connection.cursor() as cursor:
        query='select * from promotions.users_data'
        cursor.execute(query)
        query_response=cursor.fetchall()
        return render(request, 'list_of_users.html', {'query_response': query_response})
      
def end_user(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        hashed_password=make_password(password)
        email = request.POST.get('email')
        age = request.POST.get('age')
        location = request.POST.get('location')  
        gender = request.POST.get('gender')
        intrest = request.POST.get('intrest')
        user = request.POST.get('user')
        error = "Invalid Email is incorrect or already existed"
        is_user = 1
        is_active = 1
        if age:
            age = int(age)
        else:
            age = None
        if User.objects.filter(username=username).exists():
            return render(request, 'end_user.html', {'error': 'Username already exists'})
        else:
            user = User.objects.create_user(
            username=username,
            password=password,  
            email=email,
            gender=gender,
            age=age,
            is_user=is_user,
            is_active=is_active,
            companyname="",
            contact="",
            first_name="",
            last_name=""
            )
        with connection.cursor() as cursor:
            query3='select email from promotions.users_data where email = "{}"'.format(email)
            cursor.execute(query3)
            query3_response=cursor.fetchall()
            print(query3_response)
            if(query3_response):
                return render(request, 'userpage.html',{'error' : error})
            else:
                pass  
            with connection.cursor() as cursor:
                query = 'INSERT INTO users_data (name, email, age, gender, location, interests, password) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(query, [username, email, age, gender, location, intrest, hashed_password]) 
                return redirect('loginpage')
    else:
        return render(request, 'end_user.html')
    
def savepromotions(request):
    promoter_id=request.user.id
    with connection.cursor() as cursor:
        query = 'INSERT INTO promotions.promotions (title, description, start_date, end_date, target_filters, promoter_id) VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'.format(
        request.POST['title'],
        request.POST['description'],
        request.POST['start_date'],
        request.POST['end_date'],
        request.POST['intrest'],
        promoter_id ) 
        cursor.execute(query)
    return redirect('campaign')
def campaign(request):
    return redirect('promotions')
def dashboard(request):
    return render(request, 'dashboard.html')
def target_filters(request):
    current_date = date.today()
    username=request.user.username
    with connection.cursor() as cursor:
        query='select interests from users_data where name ="{}"'.format(username)
        cursor.execute(query)
        query_response=cursor.fetchall()
    with connection.cursor() as cursor:
        query2='select start_date, end_date, target_filters from promotions.promotions '
        cursor.execute(query2)
        query2_response=cursor.fetchall()
        for promotions in query2_response:
                start_date = promotions[0]
                end_date = promotions[1]   
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date) 
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)
        if(start_date <= current_date <= end_date):
            with connection.cursor() as cursor:
                query1='select * from promotions.promotions where target_filters = "{}" and start_date <= "{}" and end_date >= "{}"'.format(query_response[0][0], current_date, current_date)
                cursor.execute(query1)
                query1_response=cursor.fetchall()
                print(query1_response)
            return render(request, 'target_filters.html', {'query1_response' : query1_response})
        else:
            no_promotions_found="no_promotions_found"
            return render(request,'loginpage.html', {'no_promotions_found' : no_promotions_found})


def editpromotions(request, promoter_id):
    if request.method == "POST":
        promo_id = request.POST.get('promo_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        print(start_date)
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE promotions.promotions SET start_date=%s, end_date=%s WHERE promo_id=%s AND promoter_id=%s',
                [start_date, end_date, promo_id, promoter_id]
            )
        return redirect('list_of_promotions')

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT promo_id, promoter_id, title, description, start_date, end_date, target_filters FROM promotions.promotions WHERE promoter_id=%s',
            [promoter_id]
        )
        query_response = cursor.fetchall()

    return render(request, 'editpromotions.html', {'query_response': query_response})


def after_promoter_login(request):
    return render(request, 'after_promoter_login1.html')

def promoter(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('Role')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        company_name = request.POST.get('companyname')
        contact = request.POST.get('contact')

        if role == "Admin":
            is_superuser = True
            is_staff = True
        else:
            is_superuser = False
            is_staff = False
        if age and age.isdigit():
            age = int(age)
        else:
            age = None
        if User.objects.filter(username=username).exists():
            return render(
                request,
                'promoterregistration.html',
                {'error': 'Username already exists'}
            )
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                gender=gender,
                age=age,
                is_user=False,
                companyname=company_name,
                contact=contact,
                is_superuser=is_superuser,
                is_staff=is_staff,
                is_active=False,
                first_name="",
                last_name=""
            )

            return render(
                request,
                'loginpage.html',
                {'success': 'Successfully Created'}
            )
    else:
        return render(request, 'promoter.html')



   

    

    


            
                
                
        
             
    
    

        

