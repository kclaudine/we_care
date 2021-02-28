from django.shortcuts import render
from .models import *
from .filters import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='login')
def profile(request, username):
    houses = request.user.profile.houses.all()
    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = UpdateUserProfileForm(instance=request.user.profile)

    context = {
        'prof_form': prof_form,
        'houses':houses,
         }
    return render(request, 'profile.html', context)


def home(request):
    houses = House.objects.all()
    house_filter = HouseFilter(request.GET, queryset = houses)
    context = {
        'filter':house_filter,
        'houses':houses
    }
    return render(request, 'home.html',context)


def house_details(request, pk):
    house = House.objects.get(pk = pk)
    context = {
        'house':house
    }
    return render(request, 'house_detail.html', context)



def house_rent(request):
    houses = House.objects.filter(action='renting').order_by('-pk')
    context={
        'houses':houses
    }
    return render(request, 'house-rent.html',context)

def house_sell(request):
    houses = House.objects.filter(action='selling').order_by('-pk')
    context={
        'houses':houses
    }
    return render(request, 'house_sell.html',context)

def search_house(request):
    if 'house' in request.GET and request.GET["house"]:
        search = request.GET.get("house")
        house = House.search_house(search)
        message = f"{search}"
        context = {"house":house, 'search':search}
        return render(request, 'result.html',context)
    else:
        message = "You haven't searched for any term"
        return render(request, 'result.html',{"message":message})

@login_required(login_url='login')
def new_house(request):
    if request.method == 'POST':
        form = SellForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user.profile
            house.save()
            return redirect('home')
    else:
        form = SellForm()
    context={
        'form':form
    }
    return render(request, 'sell_form.html', context)

