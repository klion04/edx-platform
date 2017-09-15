""" Course Goals API """
from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from edx_rest_framework_extensions.authentication import JwtAuthentication
from opaque_keys.edx.keys import CourseKey
from openedx.core.lib.api.permissions import IsStaffOrOwner
from rest_framework import permissions, serializers, viewsets
from rest_framework.authentication import SessionAuthentication

from .api import CourseGoalOption
from .models import CourseGoal


User = get_user_model()


class CourseGoalSerializer(serializers.ModelSerializer):
    """
    Serializes CourseGoal models.
    """
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = CourseGoal
        fields = ('user', 'course_key', 'goal_key')

    def validate_goal_key(self, value):
        """
        Ensure that the goal_key is valid.
        """
        if value not in CourseGoalOption.get_course_goal_keys():
            raise serializers.ValidationError(
                'Provided goal key, {goal_key}, is not a course key (options= {goal_options}).'.format(
                    goal_key=value,
                    goal_options=[option.value for option in CourseGoalOption],
                )
            )
        return value

    def validate_course_key(self, value):
        """
        Ensure that the course_key is valid.
        """
        course_key = CourseKey.from_string(value)
        if not course_key:
            raise serializers.ValidationError('Provided course_id does not map to a course.')
        return course_key


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
        GET /course_goal/api/v0/course_goal?course_key={course_key1}&username={username}
        POST /course_goal/api/v0/course_goal?course_key={course_key1}&goal={goal}&username={username}
            Request data: {"course_key": <course-key>, "goal_key": "unsure", "username": "testUser"}

    """
    authentication_classes = (JwtAuthentication, SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsStaffOrOwner,)
    queryset = CourseGoal.objects.all()
    serializer_class = CourseGoalSerializer

    def post(self, request, *args, **kwargs):
        """
        Attempt to create course goal.
        """
        if not request.data:
            raise Http404

        course_id = request.data.get('course_key')
        if not course_id:
            raise Http404('Must provide a course_id')

        goal_key = request.data.get('goal_key')
        if not goal_key:
            raise Http404('Must provide a goal_key')

        # username = User.objects.get() if request.data.get('username') else

        api.add_course_goal(request.user, course_id, goal_key)

        return JsonResponse({
            'success': True,
        })
