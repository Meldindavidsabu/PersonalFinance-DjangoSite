from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)  # Corrected to 'user'
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # Corrected to 'user'
            note.save()
            return redirect('note_list')  # Corrected to 'note_list'
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)  # Corrected to 'user'
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)  # Corrected to 'user'
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')  # Corrected to 'note_list'
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})  # Changed 'edit_note.html' to 'note_form.html'

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)  # Corrected to 'user'
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')  # Corrected to 'note_list'
    return render(request, 'notes/delete_note.html', {'note': note})
