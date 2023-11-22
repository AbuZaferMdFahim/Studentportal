from django.shortcuts import redirect, render
from . models import Notes
from . forms import *
from django.contrib import messages 
# Create your views here.

def home(request):
    return render(request,'dashboard/home.html')

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, f"Notes added from {request.user.username} successfully!")
            return redirect('notes')  # Redirect to the same page
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')
