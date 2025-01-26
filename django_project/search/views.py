from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
#from .forms import AnnotationForm,VerseQuestionForm,VerseAnswerForm

# Create your views here.
def home(request):

    return render(request,"search/home.html")
