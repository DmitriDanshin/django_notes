from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from core.forms import SignUpForm, NoteForm
from core.models import Note


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('main')
    template_name = 'core/registration.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


def index(request):
    context = {
        "notes": Note.objects.count()
    }
    return render(request, "core/index.html", context=context)


def delete_note(request, note_id: int):
    if request.user.is_authenticated:
        note = Note.objects.get(pk=note_id)
        if note:
            note.delete()
    return HttpResponseRedirect('/notes')


def notes(request):
    if request.user.is_authenticated:
        user_notes = Note.objects.filter(user__id=request.user.id)
    else:
        user_notes = []
    context = {
        "notes": user_notes
    }
    return render(request, "core/notes.html", context=context)


def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user.id
            form.save()
            return redirect('notes')
    else:
        form = NoteForm()
    context = {
        'form': form
    }
    return render(request, 'core/create-note.html', context=context)


def edit_note(request, note_id: int):
    note = Note.objects.get(pk=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes')
    else:
        form = NoteForm(instance=note)

    context = {
        "form": form
    }
    return render(request, 'core/create-note.html', context=context)
