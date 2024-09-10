from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import PromptsEditForm
from django.core.files.storage import default_storage
import json
import os
from django.conf import settings

# Create your views here.
@login_required(login_url='account_login')
def profile(request):
    user = request.user
    context = {
        'user':user,
    }
    return render(request, "profiles/profile.html", context)

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def admin(request):
    PROMPTS_FILE_PATH = settings.PROMPTS_FILE_PATH
    if request.method == 'POST':
        form = PromptsEditForm(request.POST)
        if form.is_valid():
            # Extract prompts from form data
            prompts = {
                "evaluation_prompt": form.cleaned_data['evaluation_prompt'],
                "description_prompt": form.cleaned_data['description_prompt'],
                "spelling_errors_count_prompt": form.cleaned_data['spelling_errors_count_prompt'],
                "spelling_error_word_prompt": form.cleaned_data['spelling_error_word_prompt'],
                "spelling_error_start_index_prompt": form.cleaned_data['spelling_error_start_index_prompt'],
                "spelling_error_end_index_prompt": form.cleaned_data['spelling_error_end_index_prompt'],
                "content_relevance_prompt": form.cleaned_data['content_relevance_prompt'],
                "essay_score_prompt": form.cleaned_data['essay_score_prompt']
            }
            # Save prompts to JSON file
            with default_storage.open(PROMPTS_FILE_PATH, 'w') as json_file:
                json.dump(prompts, json_file, indent=4)
            return redirect('submit-essay')  # Redirect to avoid form resubmission
    else:
        # Load existing prompts
        try:
            with default_storage.open(PROMPTS_FILE_PATH, 'r') as json_file:
                prompts = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            prompts = {}

        # Initialize form with existing prompts
        form = PromptsEditForm(initial=prompts)

    return render(request, "profiles/admin.html", {'form': form})
