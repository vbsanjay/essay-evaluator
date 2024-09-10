# Essay Evaluation Web Application

This Django web application allows users to submit essays for evaluation and receive detailed feedback using the OpenAI API. 

## Website Link
https://essay-evaluator-delta.vercel.app/

## Features

- **Authentication:** Users can log in using Google SSO (Single Sign-On).
- **Essay Submission:** Submit essays with a title and a body text of up to 500 words.
- **Feedback:** 
  - Uses OpenAI API to evaluate the quality of essays.
  - Provides feedback including:
    - Count of spelling errors.
    - List of incorrectly spelled words with index positions.
    - Relevance of the essay content to the title (yes/no).
    - Overall essay score out of 10.
- **Admin Panel:** Allows admins to edit evaluation prompts.
- **History:** (Optional) View a history of submitted essays, including title, body, feedback, and submission date.
- **User Interface:** Basic and user-friendly, focusing on Django skills rather than complex front-end design.
- **Code Quality:** Adheres to Django best practices and utilizes appropriate Django features (models, views, templates, forms, etc.).
- **Deployment:** Deployed on Vercel.

## Technical Details

The application leverages Django's robust framework for backend development and integrates the OpenAI API for advanced essay evaluation. The latest GPT-4 Mini model, which provides structured dictionary responses, is used to deliver accurate feedback. This update has improved data processing efficiency and achieved a perfect 100% in JSON schema compliance, significantly enhancing performance compared to previous models.

## Images

### Evaluator: Evaluate your Essay here
![Home page](https://github.com/user-attachments/assets/838ed743-9ed2-4300-af40-f93b214fd9ae)

### Feedback: Feedback on your essay is seen after submission
![Feedback](https://github.com/user-attachments/assets/095e6e66-5248-486c-87ff-d2fae956b959)

### History: Track all your history of submissions in the Feedbacks section
![Feedback History](https://github.com/user-attachments/assets/f3349baa-3f6f-46cc-858a-98dd64c69604)

### Admin Panel: A panel available only to users with admin access
![Admin Panel](https://github.com/user-attachments/assets/3f15217c-2506-48d2-b0e1-f56bb2bcf18f)


