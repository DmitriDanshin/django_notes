from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('notes/', views.notes, name='notes'),
    path('notes/delete/<int:note_id>', views.delete_note, name='delete-note'),
    path('notes/edit/<int:note_id>', views.edit_note, name='edit-note'),
    path('notes/create', views.create_note, name='create-note'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registration', views.SignUpView.as_view(), name='registration'),
]
