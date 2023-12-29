from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



from .forms import SignUpForm, ProfileFormUpdate

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})

class Login(LoginView):
    template_name = 'users/login.html'
    next_page = '/'

@login_required(login_url='/')
def ProfileInfo(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})


def Logout(request):
    logout(request)
    return redirect('/')



@login_required(login_url='/')
def ProfileUpdate(request):
    if request.method == 'POST':
        form = ProfileFormUpdate(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('ProfileInfo')
    else:
        form = ProfileFormUpdate(instance=request.user.profile)

    return render(request, 'users/update.html', context={'forms': form})





