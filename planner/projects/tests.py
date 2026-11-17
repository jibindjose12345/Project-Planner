from django.http import Http404
from django.test import SimpleTestCase
from unittest.mock import patch

from rest_framework.test import APIRequestFactory

from .views import TaskCreateWithAI


class TaskCreateWithAITests(SimpleTestCase):

    @patch('projects.views.get_object_or_404', side_effect=Http404)
    def test_missing_assigned_project_returns_not_found(self, get_object):
        request = APIRequestFactory().post('/create-tasks-ai/missing-uuid/')

        response = TaskCreateWithAI.as_view()(request, uuid='missing-uuid')

        self.assertEqual(response.status_code, 404)
        get_object.assert_called_once()
