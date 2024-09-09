from django.shortcuts import render
from essays.models import Essay

# Create your views here.
def history(request):
    essays = Essay.objects.filter(user=request.user)
    context = {
        'essays':essays
    }
    return render(request, 'history/history.html', context)