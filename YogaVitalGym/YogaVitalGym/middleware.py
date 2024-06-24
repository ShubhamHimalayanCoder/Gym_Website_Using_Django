from django.shortcuts import redirect

class CustomerRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/customer/') and 'customer_id' not in request.session:
            return redirect('customer_login')
        return self.get_response(request)

class StaffRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/staff/') and 'staff_id' not in request.session:
            return redirect('staff_login')
        return self.get_response(request)
