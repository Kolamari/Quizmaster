from django.shortcuts import redirect

# Views are handled in the quiz app
# This file is for any additional result-specific views

def results_redirect(request):
    """Redirect to quiz results."""
    return redirect('quiz_results')
