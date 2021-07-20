from django.shortcuts import render
from .models import *
from .filters import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages



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
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login')
def profile(request, username):
    houses = request.user.profile.Houses.all()
    bookings = Booking.objects.filter(house__owner__user=request.user.id)
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
        'bookings':bookings
         }
    return render(request, 'core/profile.html', context)


def home(request):
    houses_r = House.objects.filter(action='Renting').order_by('-pk')[:100]
    houses_s = House.objects.filter(action='Selling').order_by('-pk')[:100]
    
    context = {
        
        'houses_r':houses_r,
        'houses_s':houses_s
    }
    return render(request, 'core/home.html',context)

def about(request):
    return render(request, 'core/about.html')



def house_details(request, pk):
    house = House.objects.get(pk = pk)
    if request.method == 'POST':
        form = BookingForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.house = house
            booking.save()
            messages.success(request, 'Your booking was successful! we will reach out to you very soon!!', extra_tags='alert')
            return redirect(request.path_info)
    else:
        form = BookingForm()
    context = {
        'house':house,
        'form':form
    }
    return render(request, 'core/house_detail.html', context)



def house_rent(request):
    houses = House.objects.filter(action='Renting').order_by('-pk')
    house_filter = HouseFilter(request.GET, queryset = houses)
    context={
        'houses':houses,
        'filter':house_filter,
    }
    return render(request, 'core/house-rent.html',context)

def house_sell(request):
    houses = House.objects.filter(action='Selling').order_by('-pk')
    house_filter = HouseFilter(request.GET, queryset = houses)
    context={
        'filter':house_filter,
        'houses':houses
    }
    return render(request, 'core/house_sell.html',context)

def search_house(request):
    if 'house' in request.GET and request.GET["house"]:
        search = request.GET.get("house")
        house = House.search_house(search)
        message = f"{search}"
        context = {"house":house, 'search':search}
        return render(request, 'core/result.html',context)
    else:
        message = "You haven't searched for any term"
        return render(request, 'core/result.html',{"message":message})


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
    return render(request, 'core/sell_form.html', context)

