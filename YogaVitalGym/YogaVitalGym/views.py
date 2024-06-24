from django.shortcuts import render,redirect,HttpResponse
from Gym_Customers import models as model_1
from Gym_Staff import models as model_2
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError

def homepage(request):
    return render(request,'homepage.html')

def about_us(request):
    return render(request,'about.html')

def gym(request):
    return render(request, 'gym.html')

def yoga(request):
    return render(request, 'yoga.html')

def diet_plan(request):
    return render(request, 'diet-plan.html')

def gallery(request):
    return render(request,'gallery.html')

def blog(request):
    return render(request,'blog.html')

def contact_us(request):
    return render(request,'contact-us.html')

def login(request):
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        if model_1.Gym_Customer_Data.objects.filter(customer_email = email).exists():
            user = 'Customer'
        elif model_2.Gym_Staff_Data.objects.filter(staff_user_email = email).exists():
            user = 'YogaVitalGym'
        if all([email, password, user]):
            if user == 'Customer':
                check_email = model_1.Gym_Customer_Data.objects.filter(customer_email = email).exists()
                if check_email:
                    customer = model_1.Gym_Customer_Data.objects.get(customer_email = email)
                    check_pass = check_password(password, customer.customer_password)
                    if check_pass:
                        request.session['customer_id'] = customer.customer_id
                        request.session['customer_name'] = customer.customer_name
                        request.session['customer_services'] = customer.customer_services
                        request.session['user'] = user
                        return redirect('Gym_Customers:customer-homepage')
                    else:
                        error = {
                            'error' : 'not-matched'
                        }
                else:
                    error = {
                        'error' : 'not-matched'
                    }
            elif user == 'YogaVitalGym':
                check_email = model_2.Gym_Staff_Data.objects.filter(staff_user_email = email).exists()
                if check_email:
                    gym_user = model_2.Gym_Staff_Data.objects.get(staff_user_email = email)
                    check_pass = check_password(password,gym_user.staff_user_password)
                    if check_pass:
                        request.session['gym_id'] = gym_user.staff_user_id
                        request.session['gym_name'] = gym_user.staff_user_name
                        request.session['gym_designation'] = gym_user.staff_user_designation
                        request.session['user'] = user
                        if gym_user.staff_user_designation == 'Admin':
                            return redirect('Gym_Staff:administrator-homepage')
                        elif gym_user.staff_user_designation == 'Trainer':
                            return redirect('Gym_Staff:trainer-homepage')
                        elif gym_user.staff_user_designation == 'Instructor':
                            return redirect('Gym_Staff:instructor-homepage')
                        elif gym_user.staff_user_designation == 'Dietician':
                            return redirect('Gym_Staff:dietician-homepage')
                        else:
                            error = {
                                'error' : 'no-user'
                            }
                    else:
                        error = {
                            'error' : 'not-matched'
                        }
                else:
                    error = {
                        'error' : 'not-matched'
                    }
            elif user == 'None':
                error = {
                    'error' : 'no-user'
                }
            return render(request, 'login.html', context=error)

    return render(request,'login.html')


def logout(request):
    if request.session['user'] == 'Customer':
        request.session.pop('customer_id')
        request.session.pop('customer_name')
        request.session.pop('customer_services')
        request.session.pop('user')
        return redirect('login')
    elif request.session['user'] == 'YogaVitalGym':
        request.session.pop('gym_id')
        request.session.pop('gym_name')
        request.session.pop('gym_designation')
        request.session.pop('user')
        return redirect('login')