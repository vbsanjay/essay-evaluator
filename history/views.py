from django.shortcuts import render
from essays.models import Essay
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='account_login')
def history(request):
    essays = Essay.objects.filter(user=request.user)
    context = {
        'essays':essays
    }
    return render(request, 'history/history.html', context)

@login_required(login_url='account_login')
def detailed_report(request, essay_id):
    essay = Essay.objects.get(id=essay_id)
    feedback = essay.feedback
    context = {
        'essay': essay,
        'feedback': feedback,
        'spelling_errors_count': feedback.spelling_errors_count,
        'spelling_error': feedback.spelling_errors.all(),
        'content_relevance': feedback.content_relevance,
        'score': feedback.score
    }

    print(essay.body)
    return render(request, 'history/detailed_report.html', context)