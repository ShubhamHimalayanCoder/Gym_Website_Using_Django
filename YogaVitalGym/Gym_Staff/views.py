from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password
from . import models as staff_model
from Gym_Customers import models as customer_model
from django.db import IntegrityError
from django.db.models import Q
import pandas as pd
from django.conf import settings
import os



# Create your views here.
def gym_signup(request):
    if request.POST:
        full_name = request.POST['full_name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        pin = request.POST['pin']
        designation = request.POST['designation']
        if all([full_name,mobile,email,password,confirm_password,address,city,state,country,pin,designation]):
            if designation != 'None':
                if designation == 'Admin' and staff_model.Gym_Staff_Data.objects.filter(staff_user_designation__iexact = 'Admin').exists():
                    error = {
                        'error' : 'admin-exists'
                    }
                else:
                    if password == confirm_password:
                        encrypt_password = make_password(password)
                        try:
                            staff_model.Gym_Staff_Data.objects.create(staff_user_name = full_name,
                                                                staff_user_mobile = mobile,
                                                                staff_user_email = email,
                                                                staff_user_password = encrypt_password,
                                                                staff_user_address = address,
                                                                staff_user_city = city,
                                                                staff_user_state = state,
                                                                staff_user_country = country,
                                                                staff_user_pin = pin,
                                                                staff_user_designation = designation)
                            return render(request, 'Gym_Staff/gym-signup.html', context={'success' : 'done'})
                        except IntegrityError as e:
                            if 'user_mobile' in str(e):
                                error = {
                                    'error' : 'mobile-error'
                                }
                            else:
                                error = {
                                    'error' : 'email-error'
                                }
                    else:
                        error = {
                            'error' : 'password-mismatch'
                        }
            else:
                error = {
                    'error' : 'no-option'
                }
        else:
            error = {
                'error' : 'empty-fields'
            }
        return render(request, 'Gym_Staff/gym-signup.html', context=error)
    
    return render(request, 'Gym_Staff/gym-signup.html')


def administrator(request):
    if not (request.session.get('gym_id')):
        return redirect('login')
    
    if request.GET:
        query = request.GET['search']
        customers = customer_model.Gym_Customer_Data.objects.filter(Q(customer_name__icontains=query)
        | Q(customer_email__icontains=query) | Q(customer_mobile__icontains=query)
        | Q(customer_services__icontains=query)).all()
        data = {
            'gym_customers_data' : customers
        }
        return render(request,'Gym_Staff/searching.html',context=data)

    
    if request.POST:
        try:
            user = staff_model.Gym_Staff_Data.objects.get(staff_user_id= request.session.get('gym_id'))
            if request.FILES.get('image'):
                user.staff_user_image.delete()
                user.staff_user_image = request.FILES['image']
            user.save()
            customers_data = customer_model.Gym_Customer_Data.objects.all()
            query = customer_model.Query.objects.filter(staff = user_data, is_answered=False)
            staff_data = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
            staff_query = staff_model.Staff_Query.objects.filter(receiver_id = user_data, is_answered=False)
            staff_query_response = staff_model.Staff_Query_Response.objects.all()
            data = {
                'success':'done',
                'gym_user_data': user,
                'gym_customers_data' : customers_data,
                'queries' : query,
                'staff_data' : staff_data,
                'staff_querries' : staff_query,
                'my_query_response' : staff_query_response
            }
            return render(request, 'Gym_Staff/administrator-homepage.html',context=data)
        except:
            error = {
                'error' : 'not-updated'
            }
            return render(request, 'Gym_Staff/administrator-homepage.html',context=error)


    user_data = staff_model.Gym_Staff_Data.objects.get(staff_user_id = request.session.get('gym_id'))
    customers_data = customer_model.Gym_Customer_Data.objects.all()
    query = customer_model.Query.objects.filter(staff = user_data, is_answered=False)
    staff_data = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
    staff_query = staff_model.Staff_Query.objects.filter(receiver_id = user_data, is_answered=False)
    staff_query_response = staff_model.Staff_Query_Response.objects.all()
    
    data = {
        'success':'done',
        'gym_user_data': user_data,
        'gym_customers_data' : customers_data,
        'queries' : query,
        'staff_data' : staff_data,
        'staff_querries' : staff_query,
        'my_query_response' : staff_query_response
    }    
    return render(request, 'Gym_Staff/administrator-homepage.html',context=data)


def trainer(request):
    if not (request.session.get('gym_id')):
            return redirect('login')
    
    if request.POST:
        try:
            user = staff_model.Gym_Staff_Data.objects.get(staff_user_id= request.session.get('gym_id'))
            customers_data = customer_model.Gym_Customer_Data.objects.filter(customer_services__icontains = 'Gym')
            if request.FILES.get('image'):
                user.staff_user_image.delete()
                user.staff_user_image = request.FILES['image']
            user.save()
            query = customer_model.Query.objects.filter(staff = user_data, is_answered=False)
            staff_data = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
            staff_query = staff_model.Staff_Query.objects.filter(receiver_id = user_data, is_answered=False)
            staff_query_response = staff_model.Staff_Query_Response.objects.all()
            
            data = {
                'success':'done',
                'gym_user_data': user,
                'gym_customers_data' : customers_data,
                'queries' : query,
                'staff_data' : staff_data,
                'staff_querries' : staff_query,
                'my_query_response' : staff_query_response
            }    
            return render(request, 'Gym_Staff/trainer-homepage.html',context=data)
        except:
            error = {
                'error' : 'not-updated'
            }
            return render(request, 'Gym_Staff/trainer-homepage.html',context=error)


    user_data = staff_model.Gym_Staff_Data.objects.get(staff_user_id = request.session.get('gym_id'))
    customers_data = customer_model.Gym_Customer_Data.objects.filter(customer_services__icontains = 'Gym')
    query = customer_model.Query.objects.filter(staff = user_data, is_answered=False)
    staff_data = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
    staff_query = staff_model.Staff_Query.objects.filter(receiver_id = user_data, is_answered=False)
    staff_query_response = staff_model.Staff_Query_Response.objects.all()

    data = {
        'success':'done',
        'gym_user_data': user_data,
        'gym_customers_data' : customers_data,
        'queries' : query,
        'staff_data' : staff_data,
        'staff_querries' : staff_query,
        'my_query_response' : staff_query_response
    }
    return render(request, 'Gym_Staff/trainer-homepage.html',context=data)


def instructor(request):
    if not (request.session.get('gym_id')):
        return redirect('login')
    
    if request.POST:
        try:
            user = staff_model.Gym_Staff_Data.objects.get(staff_user_id= request.session.get('gym_id'))
            customers_data = customer_model.Gym_Customer_Data.objects.filter(customer_services__icontains = 'Yoga')
            if request.FILES.get('image'):
                user.staff_user_image.delete()
                user.staff_user_image = request.FILES['image']
            user.save()
            query = customer_model.Query.objects.filter(staff = user_data, is_answered=False)
            staff_data = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
            staff_query = staff_model.Staff_Query.objects.filter(receiver_id = user_data, is_answered=False)
            staff_query_response = staff_model.Staff_Query_Response.objects.all()
            data = {
                'success':'done',
                'gym_user_data': user,
                'gym_customers_data' : customers_data,
                'queries' : query,
                'staff_data' : staff_data,
                'staff_querries' : staff_query,
                'my_query_response' : staff_query_response
            }
            return render(request, 'Gym_Staff/instructor-homepage.html',context=data)
        except:
            error = {
                'error' : 'not-updated'
            }
            return render(request, 'Gym_Staff/instructor-homepage.html',context=error)


    user_data = staff_model.Gym_Staff_Data.objects.get(staff_user_id = request.session.get('gym_id'))
    customers_data = customer_model.Gym_Customer_Data.objects.filter(customer_services__icontains = 'Yoga')
    query = customer_model.Query.objects.filter(staff = user_data, is_answered=False)
    staff_data = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
    staff_query = staff_model.Staff_Query.objects.filter(receiver_id = user_data, is_answered=False)
    staff_query_response = staff_model.Staff_Query_Response.objects.all()

    data = {
        'success':'done',
        'gym_user_data': user_data,
        'gym_customers_data' : customers_data,
        'queries' : query,
        'staff_data' : staff_data,
        'staff_querries' : staff_query,
        'my_query_response' : staff_query_response
    }
    return render(request, 'Gym_Staff/instructor-homepage.html',context=data)


def dietician(request):
    if not (request.session.get('gym_id')):
        return redirect('login')
    
    if request.POST:
        try:
            user = staff_model.Gym_Staff_Data.objects.get(staff_user_id= request.session.get('gym_id'))
            customers_data = customer_model.Gym_Customer_Data.objects.filter(customer_services__icontains = 'Diet-Planning')
            if request.FILES.get('image'):
                user.staff_user_image.delete()
                user.staff_user_image = request.FILES['image']
            user.save()
            query = customer_model.Query.objects.filter(staff = user_data, is_answered=False)
            staff_data = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
            staff_query = staff_model.Staff_Query.objects.filter(receiver_id = user_data, is_answered=False)
            staff_query_response = staff_model.Staff_Query_Response.objects.all()
            data = {
                'success':'done',
                'gym_user_data': user,
                'gym_customers_data' : customers_data,
                'queries' : query,
                'staff_data' : staff_data,
                'staff_querries' : staff_query,
                'my_query_response' : staff_query_response
            }
            return render(request, 'Gym_Staff/dietician-homepage.html',context=data)
        except:
            error = {
                'error' : 'not-updated'
            }
            return render(request, 'Gym_Staff/dietician-homepage.html',context=error)


    user_data = staff_model.Gym_Staff_Data.objects.get(staff_user_id = request.session.get('gym_id'))
    customers_data = customer_model.Gym_Customer_Data.objects.filter(customer_services__icontains = 'Diet-Planning')
    query = customer_model.Query.objects.filter(staff = user_data, is_answered=False)
    staff_data = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
    staff_query = staff_model.Staff_Query.objects.filter(receiver_id = user_data, is_answered=False)
    staff_query_response = staff_model.Staff_Query_Response.objects.all()

    data = {
        'success':'done',
        'gym_user_data': user_data,
        'gym_customers_data' : customers_data,
        'queries' : query,
        'staff_data' : staff_data,
        'staff_querries' : staff_query,
        'my_query_response' : staff_query_response
    }
    return render(request, 'Gym_Staff/dietician-homepage.html',context=data)


def update_staff(request):
    if not (request.session.get('gym_id')):
        return redirect('login')
    
    if request.POST:
        name =  request.POST.get('user_name')
        email =  request.POST.get('user_email')
        mobile =  request.POST.get('user_mobile')
        address =  request.POST.get('user_address')
        city =  request.POST.get('user_city')
        state =  request.POST.get('user_state')
        country =  request.POST.get('user_country')
        pin =  request.POST.get('user_pin')
        if all([name, email, mobile, address, city, state, country, pin]):
            try:
                staff = staff_model.Gym_Staff_Data.objects.get(staff_user_id = request.session.get('gym_id'))
                staff.staff_user_name = name
                staff.staff_user_email = email
                staff.staff_user_mobile = mobile
                staff.staff_user_address = address
                staff.staff_user_city = city
                staff.staff_user_state = state
                staff.staff_user_country = country
                staff.staff_user_pin = pin
                if request.FILES.get('image'):
                    staff.staff_user_image.delete()
                    staff.staff_user_image = request.FILES.get('image')
                staff.save()
                return render(request, 'Gym_Staff/staff-updation.html', context={'success':'done','gym_user_data' : staff})
            except IntegrityError as e:
                    if 'user_email' in str(e):
                        error = {
                            'error': 'email-error'
                        }
                    elif 'user_mobile' in str(e):
                        error = {
                            'error' : 'mobile-error'
                        }
                    else:
                        error = {
                            'error' : 'anything else'
                        }
        else:
            error = {
                'error':'empty-fields'
            }
        error['staff'] = staff
        return render(request,'Gym_Staff/staff-updation.html',context=error)
        
    staff = staff_model.Gym_Staff_Data.objects.get(staff_user_id=request.session.get('gym_id'))
    data = {
        'gym_user_data' : staff
    }
    return render(request, 'Gym_Staff/staff-updation.html',context=data)




def delete_staff(request):
    if not (request.session.get('customer_id')):
        return redirect('login')
    ex_staff = staff_model.Gym_Staff_Data.objects.get(staff_user_id=request.session.get('gym_id'))
    ex_staff.staff_user_image.delete()
    ex_staff.delete()
    request.session.pop('gym_id')
    request.session.pop('gym_name')
    request.session.pop('gym_designation')
    request.session.pop('user')
    return redirect("login")





def respond_query(request, query_id):
    if 'gym_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        query_subject = customer_model.Query.query_subject
        response_text = request.POST['response']
        query = customer_model.Query.objects.get(id=query_id)
        staff_model.Response.objects.create(query=query, response_text=response_text)
        query.is_answered = True
        query.save()
        if request.session.get('gym_designation') == 'Admin':
            return redirect('Gym_Staff:administrator-homepage')
        elif request.session.get('gym_designation') == 'Trainer':
            return redirect('Gym_Staff:trainer-homepage')
        elif request.session.get('gym_designation') == 'Instructor':
            return redirect('Gym_Staff:instructor-homepage')
        elif request.session.get('gym_designation') == 'Dietician':
            return redirect('Gym_Staff:dietician-homepage')
        else:
            return HttpResponse('No Designation')
    else:
        query = customer_model.Query.objects.get(id=query_id)
        return render(request, 'Gym_Staff/administrator-homepage.html', {'queries': query})



def send_staff_query(request):
    if 'gym_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        receiver_id = request.POST.get('recipient')
        query_subject = request.POST.get('subject')
        query_text = request.POST.get('query')
        if query_subject and query_text and receiver_id:
            sender = staff_model.Gym_Staff_Data.objects.get(staff_user_id=request.session['gym_id'])
            receiver = staff_model.Gym_Staff_Data.objects.get(staff_user_id=receiver_id)
            staff_model.Staff_Query.objects.create(sender=sender, receiver=receiver, query_subject=query_subject, query_text=query_text)
            if request.session.get('gym_id') == 1:
                return redirect('Gym_Staff:administrator-homepage')
            elif request.session.get('gym_id') == 2:
                return redirect('Gym_Staff:trainer-homepage')
            elif request.session.get('gym_id') == 3:
                return redirect('Gym_Staff:instructor-homepage')
            elif request.session.get('gym_id') == 4:
                return redirect('Gym_Staff:dietician-homepage')
            else:
                return HttpResponse('No gym_id')
        else:
            error = {
                'error' : 'All fields are required.'
            }
            if request.session.get('gym_id') == 1:
                return redirect('Gym_Staff:administrator-homepage')
            elif request.session.get('gym_id') == 2:
                return redirect('Gym_Staff:trainer-homepage')
            elif request.session.get('gym_id') == 3:
                return redirect('Gym_Staff:trainer-homepage')
            elif request.session.get('gym_id') == 4:
                return redirect('Gym_Staff:trainer-homepage')
            else:
                return HttpResponse('No gym_id')
    else:
        staff_list = staff_model.Gym_Staff_Data.objects.exclude(staff_user_id=request.session['gym_id'])
        return render(request, 'send_staff_query.html', {'staff_list': staff_list})




def respond_staff_query(request, query_id):
    if 'gym_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        response_text = request.POST.get('response')
        query = staff_model.Staff_Query.objects.get(id=query_id)
        staff_model.Staff_Query_Response.objects.create(query=query,response_text=response_text)   # Create a response (you might need to create a Response model for this)
        query.is_answered = True
        query.save()
        if request.session.get('gym_designation') == 'Admin':
            return redirect('Gym_Staff:administrator-homepage')
        elif request.session.get('gym_designation') == 'Trainer':
            return redirect('Gym_Staff:trainer-homepage')
        elif request.session.get('gym_designation') == 'Instructor':
            return redirect('Gym_Staff:instructor-homepage')
        elif request.session.get('gym_designation') == 'Dietician':
            return redirect('Gym_Staff:dietician-homepage')
        else:
            return HttpResponse('No Designation')
    else:
        query = customer_model.Query.objects.get(id=query_id)
        return render(request, 'Gym_Staff/administrator-homepage.html', {'queries': query})











def gallery(request):
    if 'gym_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        about_image = request.POST.get('about_image')
        gallery_image = request.FILES.get('gallery_image')
        staff_model.Gallery.objects.create(gallery_image=gallery_image, about_image = about_image)
        if request.session.get('gym_designation') == 'Admin':
                return redirect('Gym_Staff:administrator-homepage')
        elif request.session.get('gym_designation') == 'Trainer':
            return redirect('Gym_Staff:trainer-homepage')
        elif request.session.get('gym_designation') == 'Instructor':
            return redirect('Gym_Staff:instructor-homepage')
        elif request.session.get('gym_designation') == 'Dietician':
            return redirect('Gym_Staff:dietician-homepage')
        else:
            return HttpResponse('No Designation')
    

        


def blog(request):
    if 'gym_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        blog_title = request.POST.get('about_image')
        blog_text = request.POST.get('about_image')
        blog_image = request.POST.get('about_image')
    



def convert_to_excel(request):
    if not (request.session.get('gym_id')):
        return redirect('login')
    customers = customer_model.Gym_Customer_Data.objects.all().values('customer_id','customer_name','customer_email','customer_mobile','customer_address', 'customer_city','customer_state', 'customer_country', 'customer_pin', 'customer_services')
    columns = ['ID', 'Name', 'Email', 'Mobile', 'Address', 'City', 'State', 'Country', 'PIN', 'Gym Services']
    raw =pd.DataFrame(customers)
    raw.columns = columns
    file_path = os.path.join(settings.MEDIA_ROOT,'customers_excel_file/customers.xlsx')
    raw.to_excel(file_path)
    return redirect('Gym_Staff:download-excel')

def download_excel_file(request):
    if not (request.session.get('gym_id')):
        return redirect('login')    
    file_path = os.path.join(settings.MEDIA_ROOT, 'customers_excel_file/customers.xlsx')
    if os.path.exists(file_path):
        with open(file_path,'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'
            return response
    else:
        return HttpResponse('File not found')
