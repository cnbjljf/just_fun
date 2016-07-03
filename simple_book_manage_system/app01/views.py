from django.shortcuts import render
from django.shortcuts import redirect
from app01 import models

# Create your views here.

def index(request):
    return render(request,'books_manage.html')

def test(request):
    return render(request,'test.html')


def Author(request):
    if request.method == "POST":
        first_name = request.POST['surname']
        last_name = request.POST['last_name']
        email = request.POST['email']
        models.author.objects.create(first_name=first_name,last_name=last_name,email=email)
    author_info = models.author.objects.all()
    return render(request,'author.html',{"author_info":author_info})


def Publisher(request):
    if request.method == 'POST':
        print(request.POST)
        country=request.POST['country']
        pub_name=request.POST['pub_name']
        city = request.POST['city']
        province = request.POST['province']
        address = request.POST['address']
        website = request.POST['website']
        if country and pub_name and city and province and address and website:
            models.publisher.objects.create(name=pub_name,address=address,city=city,state_province=province\
                                            ,country=country,website=website)
    publisher_info = models.publisher.objects.all()
    return render(request,'publisher.html',{'publisher_info':publisher_info})



def Book(request):
    if request.method == "POST":
        print(request.POST)
        date=request.POST['date']
        book_name=request.POST['book_name']
        #还差点功能，时间紧迫，暂未完成，20150513今晚补上余下的功能
    book_info = models.book.objects.all()
    author_list = models.author.objects.all()
    publisher_list = models.publisher.objects.all()
    return render(request,'book.html',{'book_info': book_info,"pulisher_list":publisher_list,\
                                       'author_list':author_list})