from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='account_login')
def profile(request):
    user = request.user
    context = {
        'user':user,
    }
    return render(request, "profiles/profile.html", context)
