""" Course Goal Views """
import json

from django.utils.translation import ugettext as _
from openedx.core.djangolib.markup import Text, HTML

import api


""" Course Goals API """
from django.http import Http404, HttpResponse
from opaque_keys.edx.keys import CourseKey
from rest_framework import serializers, viewsets
from util.json_request import JsonResponse

from .models import CourseGoal

class CourseGoalSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes CourseGoal models.
    """
    class Meta:
        model = CourseGoal
        fields = ('user', 'course_key', 'goal')


class CourseGoalViewSet(viewsets.ModelViewSet):
    """
    API calls to create and retrieve a course goal.

    **Use Case**
        * Create a new goal for a user.

            Http400 is returned if the format of the request is not correct,
            the course_id or goal is invalid or cannot be found.

        * Retrieve goal for a user and a particular course.

            Http400 is returned if the format of the request is not correct,
            or the course_id is invalid or cannot be found.

    **Example Requests**
        GET /course_goal/api/v0/course_goal?course_key={course_key1}
        POST /course_goal/api/v0/course_goal?course_key={course_key1}&goal={goal}
            Request data: {"course_key": <course-key>, "goal": "unsure"}
            
    Returns an HttpResponse Object with a success message html stub.

    """
    queryset = CourseGoal.objects.all()
    serializer_class = CourseGoalSerializer

    def post(self, request, *args, **kwargs):
        """
        Attempt to create course goal.
        """
        if not request.data:
            raise Http404

        course_id = request.data.get('course_id')
        if not course_id:
            raise Http404('Must provide a course_id')

        goal_key = request.data.get('goal_key')
        if not goal_key:
            raise Http404('Must provide a goal_key')

        api.add_course_goal(request.user, course_id, goal_key)

        # Add a success message
        # TODO: LEARNER-2522: 9/2017: Address success messages later.
        message = ''
        if str(goal_key) == api.CourseGoalOption.UNSURE.value:
            message = Text(_('No problem, you can add a goal at any point on the sidebar.'))
        elif str(goal_key) == api.CourseGoalOption.CERTIFY.value:
            message = Text(_("That's great! You can upgrade to verified status in the sidebar."))
        elif str(goal_key) == api.CourseGoalOption.COMPLETE.value:
            message = Text(_("That's great! If you decide to upgrade to go for a certified status,"
                             " you can upgrade to a verified status in the sidebar."))
        elif str(goal_key) == api.CourseGoalOption.EXPLORE.value:
            message = Text(_('Sounds great - We hope you enjoy the course!'))

        # Add a dismissible icon to allow user to hide the success message
        response = HTML('{message}<span tabindex="0" class="icon fa fa-times dismiss"></span>').format(message=message)

        return HttpResponse(
            json.dumps({
                'html': response
            }),
            content_type="application/json",
        )
