from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .forms import EssayForm
# from django.urls import reverse

@login_required(login_url='account_login')
def submit_essay(request):
    form = EssayForm()
    if request.method == "POST":
        form = EssayForm(request.POST)
        if form.is_valid():
            essay = form.save(commit=False)
            essay.user = request.user 
            essay.save()
            return redirect(reverse("create_feedback", args=[essay.id]))

    context = {"form":form}
    return render(request, 'essays/submit_essay.html', context)