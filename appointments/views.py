from django.shortcuts import render
from django.http import HttpResponse

# Ye test view aapke urls.py ke liye required hai
def test(request):
    return HttpResponse("Appointments app is working")
