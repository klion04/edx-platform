"""
Course Goals Models
"""
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from eventtracking import tracker
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField


class CourseGoal(models.Model):  # pylint: disable=model-missing-unicode
    """
    Represents a course goal set by a user on the course home page.
    """
    user = models.ForeignKey(User)
    course_key = CourseKeyField(max_length=255, db_index=True, blank=True)
    goal_key = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ("user", "course_key")


@receiver(post_save, sender=CourseGoal, dispatch_uid="emit_course_goal_event")
def emit_course_goal_event(sender, instance, **kwargs):
    name = 'edx.course.goal.added' if kwargs.get('created', False) else 'edx.course.goal.updated'
    tracker.emit(
        name,
        {
            'goal_key': instance.goal_key,
        }
    )
