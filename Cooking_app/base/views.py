from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_signup(request):
    return render(request, 'login_signup.html')