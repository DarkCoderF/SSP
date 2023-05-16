from django.shortcuts import render,redirect

def posts(request):
    return redirect('articles:list')