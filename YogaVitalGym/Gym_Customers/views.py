from django.shortcuts import render,redirect
from . import models
from Gym_Staff.models import Gym_Staff_Data
from Gym_Staff.models import Response
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password

# Create your views here.
def customer_signup(request):
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
        option1 = request.POST.get('Gym')
        option2 = request.POST.get('Yoga')
        option3 = request.POST.get('Diet-Planning')
        if option1 or option2 or option3:
            if option1 and not option2 and not option3:
                options = option1
            elif option2 and not option1 and not option3:
                options = option2
            elif option3 and not option1 and not option2:
                options = option3
            elif option1 and option2 and not option3:
                options = option1 + ', ' + option2
            elif option1 and option3 and not option2:
                options = option1 + ', ' + option3
            elif option2 and option3 and not option1:
                options = option2 + ', ' + option3
            elif option1 and option2 and option3:
                options = option1 + ', ' + option2 + ', ' + option3
        else:
            options = 'empty'
    
        if all([full_name,mobile,email,password,confirm_password,address,city,state,country,pin,options]):
            if options != 'empty':
                if password == confirm_password:
                    encrypt_password = make_password(password)
                    try:
                        models.Gym_Customer_Data.objects.create(customer_name = full_name,
                                                            customer_mobile = mobile,
                                                            customer_email = email,
                                                            customer_password = encrypt_password,
                                                            customer_address = address,
                                                            customer_city = city,
                                                            customer_state = state,
                                                            customer_country = country,
                                                            customer_pin = pin,
                                                            customer_services = options)
                        return render(request, 'Gym_Customers/customer-signup.html', context={'success' : 'done'})
                    except IntegrityError as e:
                        if 'customer_mobile' in str(e):
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
        return render(request, 'Gym_Customers/customer-signup.html', context=error)
    
    return render(request, 'Gym_Customers/customer-signup.html')


def customer(request):
    if not (request.session.get('customer_id')):
        return redirect('login')
    
    if request.POST:
        try:
            customer = models.Gym_Customer_Data.objects.get(customer_id = request.session.get('customer_id'))
            if request.FILES.get('image'):
                customer.customer_image.delete()
                customer.customer_image = request.FILES.get('image')
            customer.save()
            staff = Gym_Staff_Data.objects.all()
            query_response = Response.objects.all()
            
            data = {
                'success' : 'done',
                'customer_data' : customer,
                'staff_data' : staff,
                'query_response' : query_response,
            }
            return render(request, 'Gym_Customers/customer-homepage.html',context=data)
        except:
            error = {
                'error' : 'not-updated'
            }
            return render(request, 'Gym_Customers/customer-homepage.html',context=error)
        

    customer_data = models.Gym_Customer_Data.objects.get(customer_id = request.session.get('customer_id'))
    staff = Gym_Staff_Data.objects.all()
    query_response = Response.objects.all()
    data = {
        'customer_data' : customer_data,
        'staff_data' : staff,
        'query_response' : query_response,
    }
    return render(request, 'Gym_Customers/customer-homepage.html',context=data)




    

def submit_query(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        staff_id = request.POST.get('recipient')
        query_subject = request.POST.get('subject')
        query_text = request.POST.get('query')
        staff = Gym_Staff_Data.objects.get(staff_user_id=staff_id)
        customer = models.Gym_Customer_Data.objects.get(customer_id=request.session['customer_id'])
        models.Query.objects.create(customer=customer, staff=staff, query_subject=query_subject, query_text=query_text)
        return redirect('Gym_Customers:customer-homepage')
    else:
        staff_list = Gym_Staff_Data.objects.all()
        return render(request, 'submit_query.html', {'staff_list': staff_list})
    


def submit_feedback(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        customer = models.Gym_Customer_Data.objects.get(customer_id = request.session['customer_id'])
        feedback_message = request.POST.get('message')
        rating = request.POST.get('rating')
        models.Feedback.objects.create(customer=customer, feedback_message = feedback_message, rating = rating)
        return redirect('Gym_Customers:customer-homepage')
    


    

def update_customer(request):
    if not (request.session.get('customer_id')):
        return redirect('login')
    
    if request.POST:
        name =  request.POST.get('customer_name')
        email =  request.POST.get('customer_email')
        mobile =  request.POST.get('customer_mobile')
        address =  request.POST.get('customer_address')
        city =  request.POST.get('customer_city')
        state =  request.POST.get('customer_state')
        country =  request.POST.get('customer_country')
        pin =  request.POST.get('customer_pin')
        if all([name, email, mobile, address, city, state, country, pin]):
            try:
                customer = models.Gym_Customer_Data.objects.get(customer_id = request.session.get('customer_id'))
                customer.customer_name = name
                customer.customer_email = email
                customer.customer_mobile = mobile
                customer.customer_address = address
                customer.customer_city = city
                customer.customer_state = state
                customer.customer_country = country
                customer.customer_pin = pin
                if request.FILES.get('image'):
                    customer.customer_image.delete()
                    customer.customer_image = request.FILES.get('image')
                customer.save()
                return render(request, 'Gym_Customers/customer-updation.html', context={'success':'done','customer_data' : customer})
            except IntegrityError as e:
                    if 'customer_email' in str(e):
                        error = {
                            'error': 'email-error'
                        }
                    elif 'customer_mobile' in str(e):
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
        error['customer'] = customer
        return render(request,'Gym_Customers/customer-updation.html',context=error)
        
    customer = models.Gym_Customer_Data.objects.get(customer_id=request.session.get('customer_id'))
    data = {
        'customer_data' : customer
    }
    return render(request, 'Gym_Customers/customer-updation.html',context=data)






def delete_customer(request):
    if not (request.session.get('customer_id')):
        return redirect('login')
    ex_customer = models.Gym_Customer_Data.objects.get(customer_id=request.session.get('customer_id'))
    ex_customer.customer_image.delete()
    ex_customer.delete()
    request.session.pop('customer_id')
    request.session.pop('customer_name')
    request.session.pop('customer_services')
    request.session.pop('user')
    return redirect("login")

def delete_customer_account(request, id):
    if not (request.session.get('gym_id')):
        return redirect('login')
    ex_customer = models.Gym_Customer_Data.objects.get(customer_id=id)
    ex_customer.customer_image.delete()
    ex_customer.delete()
    if request.session.gym_designation == 'Admin' :    
        return redirect("Gym_Staff:administrator-homepage")
    elif request.session.gym_designation == 'Trainer' :   
        return redirect("Gym_Staff:trainer-homepage")
    elif request.session.gym_designation == 'Instructor' :     
        return redirect("Gym_Staff:instructor-homepage")
    elif request.session.gym_designation == 'Dietician' :     
        return redirect("Gym_Staff:dietician-homepage")
