from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ユーザーをログインさせる
            login(request, user)
            return redirect('upload_file')  # ログイン後にリダイレクトするURLを指定
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
