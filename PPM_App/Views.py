from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from PPM_App.Models import Poll, Response, Choice
from PPM_App.Serializers import PollSerializer, ResponseSerializer

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse


from PPM_App.Forms import PollForm, ChoiceFormSet

class PollCreateView(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

class ResponseCreateView(generics.CreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]

class PollResultsView(generics.RetrieveAPIView):
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
    return render(request, 'create_poll.html', {'form': form, 'formset': formset})

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