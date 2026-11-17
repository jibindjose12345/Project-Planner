from django.shortcuts import get_object_or_404, render

# Create your views here.

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from .models import Project,AssignedProject

from .serializers import ProjectSerializer,TaskSerializer

from .models import AssignedProject,Task

from .serializers import AssignedProjectSerializer

from rest_framework.views import APIView

from rest_framework.response import Response

from planner.utils import generate_tasks

from django.db import transaction

from planner.paginations import CustomPagination

class ProjectListCreateView(ListCreateAPIView):

    pagination_class = CustomPagination

    queryset = Project.objects.filter(active_status = True)

    serializer_class = ProjectSerializer


class ProjectsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = Project.objects.filter(active_status = True)
    
    serializer_class = ProjectSerializer

    def perform_destroy(self, instance):

        instance.active_status = False

        instance.save()

class AssignedProjectListCreateView(ListCreateAPIView):

    pagination_class = CustomPagination

    queryset = AssignedProject.objects.filter(active_status = True).select_related('project','coordinator').prefetch_related('developers')

    serializer_class = AssignedProjectSerializer


class AssignedProjectsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = AssignedProject.objects.filter(active_status = True).select_related('project','coordinator').prefetch_related('developers')

    serializer_class = AssignedProjectSerializer

    def perform_destroy(self, instance):

        instance.active_status = False

        instance.save()



class TaskListCreateView(ListCreateAPIView):

    pagination_class = CustomPagination

    def get_queryset(self):
        uuid = self.request.query_params.get('project')

        if uuid:
            assigned_project = AssignedProject.objects.get(uuid=uuid,active_status=True)

            return assigned_project.assigned_tasks.filter(active_status=True).select_related('assigned_project', 'assigned_to')

        return Task.objects.none()

    serializer_class = TaskSerializer


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = Task.objects.filter(active_status=True).select_related('assigned_project', 'assigned_to')

    serializer_class = TaskSerializer

    def perform_destroy(self, instance):

        instance.active_status = False

        instance.save()

class TaskCreateWithAI(APIView):

    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        assigned_project = get_object_or_404(
            AssignedProject,
            uuid=uuid,
            active_status=True,
        )

        try:

            result = generate_tasks(assigned_project)

        except ValueError as e:

            return Response({'msg': str(e)}, status=400)

        tasks = [Task(title=task.title,
                    description=task.description,
                    assigned_project=assigned_project,
                    assigned_to_id= task.developer_id,
                    priority = task.priority) for task in result.tasks]

        with transaction.atomic():

            Task.objects.bulk_create(tasks)

            data = {'msg':'Tasks assigned successfully'}

            return Response(data,status=200)