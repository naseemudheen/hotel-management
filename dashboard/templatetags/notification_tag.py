from django import template
from dashboard.models import Booking, Notification

register = template.Library()


@register.simple_tag
def get_num_unread_notifi():

    qs = Notification.objects.filter(is_readed = False).count()
    return qs