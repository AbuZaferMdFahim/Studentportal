from django.shortcuts import redirect, render
from . models import Notes, Homework
from . forms import *
from django.contrib import messages 
from django.views import generic
from youtubesearchpython import VideosSearch

# Create your views here.

def home(request):
    return render(request,'dashboard/home.html')

# Notes
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

def update_note(request, pk=None):
    note = Notes.objects.get(id=pk)

    if request.method == "POST":
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f"Note updated successfully!")
            return redirect('notes')
    else:
        form = NotesForm(instance=note)

    return render(request, 'dashboard/update_note.html', {'form': form, 'note': note})


def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NotesdetailView(generic.DetailView):
    model = Notes

# homework     

def homework(request):
    if request.method== 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            homework = Homework(
                user=request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homework.save()
            messages.success(request, f"Homework added from {request.user.username} successfully!")
            return redirect('homework')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done=True
    else:
        homework_done=False 
    context={'homework':homework,'homework_done':homework_done, 'form':form}
    return render(request,'dashboard/homework.html',context)

def update_homework(request,pk=None):
    homework= Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')

def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

# Youtube
def youtube(request):
    if request.method == "POST":
        form = YoutubeForm(request.POST)
        # Check if 'text' key is present in request.POST
        if 'text' in request.POST:
            text = request.POST['text']
            video = VideosSearch(text, limit=10)
            result_list = []
            for i in video.result()['result']:
                result_dict = {
                    'input': text,
                    'title': i['title'],
                    'duration': i['duration'],
                    'thumbnails': i['thumbnails'][0]['url'],
                    'channel': i['channel']['name'],
                    'link': i['link'],
                    'views': i['viewCount']['short'],
                    'published': i['publishedTime'],    
                }
                desc = ''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc += j['text']
                result_dict['description'] = desc
                result_list.append(result_dict)
            context = {'form': form, 'results': result_list}
            return render(request, 'dashboard/youtube.html', context)
    else:
        form = YoutubeForm()
        context = {'form': form}
        return render(request, 'dashboard/youtube.html', context)
