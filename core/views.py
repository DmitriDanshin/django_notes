from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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
    if request.user.is_authenticated:
        notes_amount = Note.objects.filter(user=request.user).count()
    else:
        notes_amount = 0
    context = {
        "notes": notes_amount
    }
    return render(request, "core/index.html", context=context)


@login_required
def delete_note(request, note_id: int):
    note = get_object_or_404(Note, pk=note_id)
    if note.user != request.user:
        return redirect('notes')
    note.delete()
    return redirect('notes')


@login_required
def notes(request):
    user_notes = Note.objects.filter(user__id=request.user.id) or []
    context = {
        "notes": user_notes
    }
    return render(request, "core/notes.html", context=context)


@login_required
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


@login_required
def edit_note(request, note_id: int):
    note = get_object_or_404(Note, pk=note_id)
    if note.user != request.user:
        return redirect('notes')
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
