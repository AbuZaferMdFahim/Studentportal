from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    # note
    path('notes',views.notes,name='notes'),
    path('update_note/<int:pk>',views.update_note,name='update_note'),
    path('delete_note/<int:pk>',views.delete_note,name='delete_note'),
    path('notes_detail/<int:pk>',views.NotesdetailView.as_view(),name='notes_detail'),

    # homework
    path('homework',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.update_homework,name='update_homework'),
    path('delete_homework/<int:pk>',views.delete_homework,name='delete_homework'),

    # youtube
    path('youtube',views.youtube,name='youtube'),
    
    # todo
    path('todo',views.todo,name='todo'),
    path('update_todo/<int:pk>',views.update_todo,name='update_todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete_todo'),

    # books
    path('books',views.books,name='books'),

    # disctionary
    path('dictionary',views.dictionary,name='dictionary'),
    
    #wiki
    path('wiki',views.wiki,name='wiki'),
]
