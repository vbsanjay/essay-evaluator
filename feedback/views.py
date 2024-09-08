from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import openai
import json
from decouple import config

from essays.models import Essay
from .models import Feedback, SpellingError


def evaluate_essay_openAI_API(essay_text):
    openai.api_key = config('OPENAI_API_SECRET_KEY')  # Replace with your actual API key
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",  # Choose the appropriate model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Evaluate the following essay and provide feedback on the quality, spelling errors, relevance to the title, and score out of 10:\n\n{essay_text}"}
        ],
        functions=[
            {
                "name": "evaluate_essay",
                "description": "Provides structured feedback for the essay",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spelling_errors_count": {"type": "integer", "description": "Number of spelling mistakes in the essay"},
                        "spelling_error": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "word": {"type": "string", "description": "The misspelled word"},
                                    "start_index": {"type": "integer", "description": "Start index of the word"},
                                    "end_index": {"type": "integer", "description": "End index of the word"}
                                }
                            }
                        },
                        "content_relevance": {"type": "boolean", "description": "Is the essay content related to the title?"},
                        "essay_score": {"type": "integer", "description": "Score out of 10 for the essay"}
                    },
                    "required": ["spelling_errors_count", "spelling_errors", "related_to_title", "essay_score"]
                }
            }
        ],
        function_call={"name": "evaluate_essay"},
        max_tokens=1000  # Adjust based on the response you need
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

# Create your views here.
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

# get feedback
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


