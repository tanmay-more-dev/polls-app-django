from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
from .forms import QuestionForm, QuestionModelForm
from django.contrib import messages

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:10]

class DetailsView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/details.html", { "question": question, "error_message": "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def add_form(request):
    if request.method == "POST":
        form = QuestionModelForm(request.POST)
        if form.is_valid():
            ques = Question(question_text = form.cleaned_data['question_text'], pub_date = timezone.now())
            ques.save()
            # form.save()
            Choice(question=ques, choice_text = form.cleaned_data['choice_one'], votes=0).save()
            Choice(question=ques, choice_text = form.cleaned_data['choice_two'], votes=0).save()
            return HttpResponseRedirect(reverse("polls:index"))
        else:
            return HttpResponseRedirect(reverse("polls:index"))
    else:
        form = QuestionModelForm()
        return render(request, "polls/add_question.html", {"form": form})