from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from rest_framework import viewsets
from .serializers import NewsSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import requests

class NewsViewsSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    

# Create your views here.

def news_api(request):
    url="https://newsapi.org/v2/everything?q=tesla&from=2023-04-23&sortBy=publishedAt&apiKey=462359fb8553467a95bfef1e51acb8f1"
    response = requests.get(url)
    data = response.json()
    data = data['articles']
    send_data = {

        'newsData':data
    }
    return render(request, 'api.html', send_data)


def index(request):
    data={
        'categoryData': Category.objects.all(),
    }
    return render(request,'index.html', data)

def news(request):
    news_data=News.objects.all().values()
    news_data=list(news_data)
    return JsonResponse(news_data, safe=False)

    if request.method == 'POST':
        search=request.POST['search']
        find_data=News.objects.filter(title__icontains=search) | News.objects.filter(category__name__icontains=search)
        paginator = Paginator(find_data, 4) 
        page = request.GET.get('page')
        find_data = paginator.get_page(page)   

        data={
            'newsData':find_data,
            'title':'Search Result'
        }
        return render(request,'news.html',data)
    else:
        news_data=News.objects.all()
        paginator = Paginator(news_data, 3) 
        page = request.GET.get('page')
        news_data = paginator.get_page(page)    
    data={
        'newsData':news_data,
        'title':'All News'
    }
    return render(request,'news.html', data)

def contact(request):
    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']     
        send_mail("Subject: " + subject, message, email, ['indramgr007@gmail.com'], fail_silently=False)   
        messages.success(request, 'Your message has been sent successfully')
        back = request.META.get('HTTP_REFERER')
        return redirect(back)
    else:
        return render(request,'contact.html')


def news_details(request, slug):
    newsData = News.objects.get(slug=slug)
    category = newsData.category.id
    related_news = News.objects.filter(category=category).exclude(id=newsData.id)
    data = {
        'newsData': News.objects.get(slug=slug),
        'related_news': related_news,
    }
    return render(request, 'news_details.html', data)

def global_data(request):
    data = {
            'categoryData':Category.objects.all(),
    }
    return data


def category_news(request,slug):
    data = {
        'catData':Category.objects.get(slug=slug),
    } 
    return render(request, 'category_news.html', data)


def page(request, slug):
    data={
        'pageContent': Page.objects.get(slug=slug),
    }
    return render(request,'page.html', data)
    


