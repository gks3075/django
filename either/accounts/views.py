from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)     # 모델 폼이라서 데이터만 받으면 됨
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:       # 이미 로그인이 되어있으면 
        return redirect('articles:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)    # 폼이어서 request와 데이터 둘다 받아야 함
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')    # login_required 쓸 때 next 받기 위해서 => html에서 action 비워두기
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('articles:index')


def delete(request):
    if request.user.is_authenticated:
        # 회원탈퇴 후 로그아웃
        request.user.delete()
        auth_logout(request)
    return redirect('articles:index')


def profile(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)

def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user) # instance를 안주면 새로 저장하면서 integrity 에러발생
        if form.is_valid():
            user = form.save()
            return redirect('accounts:profile', user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)