from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from PPM_App.Models import Poll, Choice
from PPM_App.Serializers import PollSerializer

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from PPM_App.Forms import PollForm, ChoiceFormSet

class PollCreateView(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]


def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('Dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'Register.html', {'form': form})

def Dashboard(request):
    polls = Poll.objects.all()
    choices = Choice.objects.all()
    return render(request, 'Dashboard.html', {'polls': polls, 'choices': choices})

def Logout(request):
    logout(request)
    return redirect('Login')

def PollCreate(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        formset = ChoiceFormSet(request.POST, prefix='choices')
        if form.is_valid() and formset.is_valid():
            poll = form.save(commit=False)
            poll.user = request.user
            poll.save()

            for form in formset:
                if form.cleaned_data.get('text'):
                    choice = form.save(commit=False)
                    choice.poll = poll
                    choice.save()

            return redirect('Dashboard')
        else:
            print("Form is invalid")
            print("Form.errors: ", form.errors)
            print("Formset.errors: ", formset.errors)
    else:
        form = PollForm()
        formset = ChoiceFormSet(prefix='choices')
    return render(request, 'Create_poll.html', {'form': form, 'formset': formset})

def Delete_Poll(request, poll_id):
    if request.method == 'DELETE':
        poll = Poll.objects.get(id=poll_id)
        if request.user == poll.user:
            poll.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Non autorizzato'}, status=403)
    else:
        return JsonResponse({'success': False, 'error': 'Metodo non valido'}, status=405)

@login_required
@csrf_exempt
def vote(request, poll_id, choice_id):
    poll = Poll.objects.get(id=poll_id)
    choice = Choice.objects.get(id=choice_id)

    if request.user in poll.responded_users.all():
        return JsonResponse({'success': False, 'error': 'User has already voted'})

    choice.votes += 1
    choice.save()

    poll.responded_users.add(request.user)
    poll.save()

    return JsonResponse({'success': True})