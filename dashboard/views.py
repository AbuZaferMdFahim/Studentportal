from django.shortcuts import redirect, render
import requests, wikipedia
from . models import *
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
        form = DashboardForm(request.POST)
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
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/youtube.html', context)
    
def todo(request):
    if request.method== 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            todo = Todo(
                user=request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todo.save()
            messages.success(request, f"Todo added from {request.user.username} successfully!")
            return redirect('todo')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user = request.user)
    if len(todo) == 0:
        todo_done=True
    else:
        todo_done=False 
    context = {'todo':todo,'form':form, 'todo_done':todo_done}
    return render(request,'dashboard/todo.html',context)

def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        # Check if 'text' key is present in request.POST
        if 'text' in request.POST:
            text = request.POST['text']
            url = "https://www.googleapis.com/books/v1/volumes?q="+text
            r = requests.get(url)
            answer = r.json()
            result_list = []

            for item in answer.get('items', []):
                volume_info = item.get('volumeInfo', {})
                result_dict = {
                    'title': volume_info.get('title', ''),
                    'subtitle': volume_info.get('subtitle', ''),
                    'description': volume_info.get('description', ''),
                    'count': volume_info.get('pageCount', ''),
                    'categories': volume_info.get('categories', []),
                    'rating': volume_info.get('pageRating', ''),
                    'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                    'preview': volume_info.get('previewLink', ''),
                }
                result_list.append(result_dict)

            context = {'form': form, 'results': result_list}
            return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'dashboard/books.html', context)
    
def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        # Check if 'text' key is present in request.POST
        if 'text' in request.POST:
            text = request.POST['text']
            url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
            r = requests.get(url)
            answer = r.json()
            try:
                phonetics = answer[0]['phonetics'][0]['text']
                audio = answer[0]['phonetics'][0]['audio']
                definition = answer[0]['meanings'][0]['definitions'][0]['definition']
                example = answer[0]['meanings'][0]['definitions'][0]['example']
                synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
                context={'form':form,'input':text,'phonetics':phonetics,'audio':audio,'definition':definition,'example':example,'synonyms':synonyms}
            except:
                context={'form':form,'input':''}
            return render(request,'dashboard/dictionary.html',context)
    else:
        form = DashboardForm()
        context={'form':form}
    return render(request,'dashboard/dictionary.html',context)

def wiki(request):
    if request.method=='POST':
        text=request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context={'form':form, 'title':search.title,'link':search.url, 'details':search.summary}
        return render(request,'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
        context={'form':form}
    return render(request,'dashboard/wiki.html',context)