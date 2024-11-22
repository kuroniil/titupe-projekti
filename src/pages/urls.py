from django.urls import path

from .views import homeView, notesView, registerView, newNoteView, logoutView, noteSearchView, publicNoteView, adminView, deleteView

urlpatterns = [
    path('', homeView, name='home'),
    path('notes', notesView, name='notes'),
    path('register', registerView, name='register'),
    path('newnote', newNoteView, name='newnote'),
    path('logout', logoutView, name='logout'),
    path('notesearch', noteSearchView, name='notesearch'),
    path('newpublicnote', publicNoteView, name='newpublicnote'),
    path('adminpage', adminView, name='admingpage'),
    path('delete/<int:id>', deleteView, name='delete')
]