from django.shortcuts import render


def account(request):
    return render(request, 'user/user_account.html')
