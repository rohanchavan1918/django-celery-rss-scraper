from django.shortcuts import render,redirect


# Create your views here.

# Redirect to Admin LOgin
def home(request):
    response = redirect('/admin/')
    return response