from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from sqlite3 import IntegrityError
from .models import Question, Choice, VoteUser
from django.utils import timezone
from django.contrib import messages
from django.db.models import F

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'anketler/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user_ip = get_client_ip(request)
    has_voted = VoteUser.objects.filter(question=question, ip_address=user_ip).exists()
    
    return render(request, 'anketler/detail.html', {
        'question': question,
        'has_voted': has_voted
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user_ip = get_client_ip(request)
    
    if VoteUser.objects.filter(question=question, ip_address=user_ip).exists():
        messages.error(request, 'Bu ankete daha önce oy kullandınız!')
        return HttpResponseRedirect(reverse('anketler:detail', args=(question.id,)))
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'anketler/detail.html', {
            'question': question,
            'error_message': "Bir seçenek seçmediniz.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        
        VoteUser.objects.create(question=question, ip_address=user_ip)
        
        messages.success(request, 'Oyunuz başarıyla kaydedildi!')
        return HttpResponseRedirect(reverse('anketler:detail', args=(question.id,)))

def about(request):
    return render(request, 'anketler/about.html')