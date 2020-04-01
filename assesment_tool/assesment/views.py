from django.shortcuts import render
from .models import Question, Output, Result
# Create your views here.

def home(request):
    context = {}
    return render(request, 'home.html', context)

def test(request, country, type, id):
    if type == 'question':
        context = {'type'       : type,
                   'question'   : Question.objects.get(question_id=id, country=country)}
                    
    elif type == 'output':
        current_output = Output.objects.get(output_id=id, country=country)
        context = {'type'       : type,
                   'output'     : current_output}
    
        result = Result(output=current_output, country=current_output.country)
        result.save()
    return render(request, 'test.html', context)
