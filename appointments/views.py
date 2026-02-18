from django.http import HttpResponse
from django.shortcuts import render


# Ye test view aapke urls.py ke liye required hai
def test(request):
    return HttpResponse("Appointments app is working")
