from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import openai
import json
import os
from dotenv import load_dotenv
from essays.models import Essay
from .models import Feedback, SpellingError
from django.contrib.auth.decorators import login_required
from django.conf import settings 

load_dotenv()

PROMPTS_FILE_PATH = settings.PROMPTS_FILE_PATH

DEFAULT_PROMPTS = {
    "evaluation_prompt": "Evaluate the following essay and provide feedback on the quality, spelling errors, relevance to the title, and score out of 10:\n\n{essay_text}",
    "description_prompt": "Provides structured feedback for the essay",
    "spelling_errors_count_prompt": "Number of spelling mistakes in the essay",
    "spelling_error_word_prompt": "The misspelled word",
    "spelling_error_start_index_prompt": "Start index of the word",
    "spelling_error_end_index_prompt": "End index of the word",
    "content_relevance_prompt": "Is the essay content related to the title?",
    "essay_score_prompt": "Score out of 10 for the essay"
}

def load_prompts():
    try:
        with open(PROMPTS_FILE_PATH, 'r') as f:
            custom_prompts = json.load(f)
            # Use custom prompts and fall back to default ones if not provided
            prompts = {**DEFAULT_PROMPTS, **custom_prompts}
    except (FileNotFoundError, json.JSONDecodeError):
        # If JSON file doesn't exist or is corrupted, use default prompts
        prompts = DEFAULT_PROMPTS
    return prompts

def evaluate_essay_openAI_API(essay_text):
    openai.api_key = os.getenv('OPENAI_API_SECRET_KEY')

    prompts = load_prompts()

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompts["evaluation_prompt"].format(essay_text=essay_text)}
        ],
        functions=[
            {
                "name": "evaluate_essay",
                "description": prompts["description_prompt"],
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spelling_errors_count": {
                            "type": "integer",
                            "description": prompts["spelling_errors_count_prompt"]
                        },
                        "spelling_error": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "word": {
                                        "type": "string",
                                        "description": prompts["spelling_error_word_prompt"]
                                    },
                                    "start_index": {
                                        "type": "integer",
                                        "description": prompts["spelling_error_start_index_prompt"]
                                    },
                                    "end_index": {
                                        "type": "integer",
                                        "description": prompts["spelling_error_end_index_prompt"]
                                    }
                                }
                            }
                        },
                        "content_relevance": {
                            "type": "boolean",
                            "description": prompts["content_relevance_prompt"]
                        },
                        "essay_score": {
                            "type": "integer",
                            "description": prompts["essay_score_prompt"]
                        }
                    },
                    "required": ["spelling_errors_count", "spelling_error", "content_relevance", "essay_score"]
                }
            }
        ],
        function_call={"name": "evaluate_essay"},
        max_tokens=1000
    )

    feedback_json = response.choices[0].message['function_call']['arguments']
    feedback_dict = json.loads(feedback_json)

    return feedback_dict


def create_spelling_error(feedback, feedback_json):
    spelling_error = feedback_json.get('spelling_error', [])
    for error in spelling_error:
        SpellingError.objects.create(
            word=error['word'],
            start=error['start_index'],
            end=error['end_index'] - 1,
            feedback=feedback 
        )

@login_required(login_url='account_login')
def create_feedback(request, essay_id):
     # Retrieve the essay using the provided essay_id
    essay = get_object_or_404(Essay, id=essay_id)
    essay_text = essay.body
    
    # Use OpenAI API to evaluate the essay
    feedback_json = evaluate_essay_openAI_API(essay_text)
    # Extract relevant information from the feedback_json
    spelling_errors_count = feedback_json.get('spelling_errors_count', 0)
    content_relevance = feedback_json.get('content_relevance', False)  # Default to 'no' if not provided
    score = feedback_json.get('essay_score', 0)

    # Create or update Feedback instance
    feedback, created = Feedback.objects.update_or_create(
        essay=essay,
        defaults={
            'spelling_errors_count': spelling_errors_count,
            'content_relevance': content_relevance,
            'score': score
        }
    )
    create_spelling_error(feedback, feedback_json)
    return redirect(reverse("feedback", kwargs={"feedback_id": feedback.id}))

@login_required(login_url='account_login')
def feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    context = {
        'essay':feedback.essay,
        'spelling_errors_count': feedback.spelling_errors_count,
        'spelling_error': feedback.spelling_errors.all(),
        'content_relevance': feedback.content_relevance,
        'score': feedback.score
    }

    return render(request, 'feedback/essay_feedback.html', context)


