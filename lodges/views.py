from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AgentPersonalInfoForm, AgentPropertiesForm #, BookedLodgeForm, PaymentForm,
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .models import LodgeProperties, Lodge, NewPayment, Pop_searched, Profile, AgentPersonalInfo, Contact #, Payment,
from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.paginator import Paginator#, zEmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from datetime import datetime

from .models import User
from notifications.signals import notify

current_user_name = []
def index(request):
    searched_list = []
    searched = Pop_searched.objects.all()
    for s in searched:
        search = str(s.searched)
        searched_list.append(search.lower())
        # print(str(s.searched))
    print(set(searched_list))
    if len(searched_list) > 0:
        first = Lodge.objects.filter(name__contains=searched_list[0])
        if len(searched_list) > 1:
            second = Lodge.objects.filter(name__contains=searched_list[1])

    context = {
        'lodges': Lodge.objects.all()[:4],
        # 'results': results,
        'searched_list': searched_list,
        'first': first,
        'second': second
        }
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method=='POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        subject  = request.POST['subject']
        message = request.POST['message']
        date = datetime.now()
        contact = Contact.objects.create(full_name=full_name, email=email, subject=subject, message=message, date = date)
        messages.success(request,'Message has been sent successfully')
        return HttpResponseRedirect('/')
    else:
        return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email') 
            messages.success(request, f'Account for {username} has been created!')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)

def deposit(request):
    lodge = Lodge.objects.all()
    email = request.user.email
    context = {
        'lodges': lodge, 
        'email': email,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, 'confirm_payment.html', context)

def ini_pay(request, id):
    try:
        lodge = LodgeProperties()
        lodge_id = get_object_or_404(LodgeProperties, id=id)
        user = User.objects.get(username=request.user)
        lodge_name = lodge_id
        email = request.user.email
        amount = lodge_id.lodge.price
        payment = NewPayment.objects.create(user=user, lodge_name=lodge_name, email=email, amount=amount)
        # if request.method == 'POST':
        #     user = User.objects.get(username=request.user)
        #     lodge_name = request.POST['name']
        #     email = request.POST['email']
        #     amount = request.POST['price']
            
        #     print(lodge_id.id)

        #     payment = NewPayment.objects.create(user=user, lodge_name=lodge_name, email=email, amount=amount)
        return render(request, 'confirm_payment.html', {'lodge_id':lodge_id, 'lodge':lodge })
            #return redirect('confirm_payment', id)
    except Exception as e:
        print(e)
        #return HttpResponse("Account has been created for this user proceed to properties upload by typing this ")
        return render(request, 'agenterrorpage.html')

def lodgeview(request, id):
    try:
        lodge = LodgeProperties
        lodge_id = get_object_or_404(lodge, id=id)
        users = User.objects.all()
        print(request.user)
        user = User.objects.get(username=request.user)

        return render(request, 'lodge_detail.html', 
                    {'users': users, 'user': user, 'lodge':lodge, 'lodge_id':lodge_id})
    except Exception as e:
        print(e)
        return HttpResponse("Something is wrong at the moment.")

class LodgeDetailView(DetailView):
    model = LodgeProperties
    template_name = 'lodge_detail.html'
    #ordering = ['-date-poste']

class ConfPayment(DetailView):
    model = LodgeProperties
    template_name = 'confirm_payment.html'



def listing(request):
    lodges = Lodge.objects.all().order_by("name")
    paginator = Paginator(lodges, per_page=6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "lodges":lodges}
    return render(request, "list.html", context)

def listing_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 2)
    startswith = request.GET.get("startswith", "")
    keywords = Lodge.objects.filter(
        name__startswith=startswith
    )
    paginator = Paginator(keywords, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"name": kw.name} for kw in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)

def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        results = Lodge.objects.filter(name__contains=searched)
        lodges = Lodge.objects.all()

        user = User.objects.get(username=request.user)
        Pop_searched.objects.create(user=user, searched=searched)
        return render(request, 'list.html', {'searched':searched, 'results':results, 'lodges':lodges})
    else:
        return render(request, 'list.html',)

def filter(request):
    if request.method == "POST":
        minimum = request.POST.get('minimum')
        maximum = request.POST.get('maximum')
        lodges = Lodge.objects.all()
        price_query = []
        for i in lodges:
            if i.price >= int(minimum) and i.price <= int(maximum):
                #print(i.price)
                price_query.append(i)
        return render(request, 'list.html', {'price_query': price_query})
    else:
        return render(request, 'list.html',)
    

def bookings(request, id):
    try:
        lodge = LodgeProperties
        lodge_id = get_object_or_404(lodge, id=id)
        users = User.objects.all()
        print(request.user)
        user = User.objects.get(username=request.user)
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y %H:%M:%S")

        return render(request, 'lodge_booking.html', 
                    {'users': users, 'date_str':date_str, 'user': user, 'lodge':lodge, 'lodge_id':lodge_id})
    except Exception as e:
        print(e)
        return HttpResponse("Please login from admin site for sending messages.")

def message(request):
    try:
        if request.method == 'POST':
            #sender = User.objects.get(username=request.user)
            sender = User.objects.get(username=request.user)
            receiver = User.objects.get(id=request.POST.get('user_id'))
            notify.send(sender, recipient=receiver, verb='Message', description=request.POST.get('message'))
            return redirect('index')
        else:
            return HttpResponse("Invalid request")
    except Exception as e:
        print(e)
        #return HttpResponse("Account has been created for this user proceed to properties upload by typing this ")
        return render(request, 'agenterrorpage.html')


def agentPersonalInfo(request):
    try:
        if request.method == 'POST':
            form = AgentPersonalInfoForm(request.POST)
            
            if form.is_valid():
                agent = form.save(commit=False)
                agent.user = request.user
                agent.save()
                agent_fname = form.cleaned_data.get('agent_fname')
                messages.success(request, f' {agent_fname} request has been submitted')

                return redirect('agentProperties')
        else:
            form = AgentPersonalInfoForm()
        return render(request, 'agentpersonalinfo.html', {'form': form})
    except Exception as e:
        print(e)
        return render(request, 'agenterrorpage.html')


def agentProperties(request):
    try:
        if request.method == 'POST':
            form = AgentPropertiesForm(request.POST, request.FILES)
            
            if form.is_valid():
                form.save()
                messages.success(request, f' request to upload properties has been submitted')

                return HttpResponse("Your response has been submitted successfully. The admin will contact you in two days time")
        else:
            form = AgentPropertiesForm()
        return render(request, 'agentproperties.html', {'form': form})
    except Exception as e:
        print(e)
        return render(request, 'propertyerrorpage.html')
