from django.urls import path

from . import views
urlpatterns = [

    path('projects/',views.ProjectListCreateView.as_view()),
    path('projects/<str:uuid>/',views.ProjectsRetrieveUpdateDestroyView.as_view()),
    path('assigned-projects/',views.AssignedProjectListCreateView.as_view()),
    path('assigned-projects/<str:uuid>/',views.AssignedProjectsRetrieveUpdateDestroyView.as_view()),
    path('tasks/',views.TaskListCreateView.as_view()),
    path('tasks/<str:uuid>/',views.TaskRetrieveUpdateDestroyView.as_view()),
    path('create-tasks-ai/<str:uuid>/',views.TaskCreateWithAI.as_view()),
    
]