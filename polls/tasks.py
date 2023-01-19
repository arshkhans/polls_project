from celery.schedules import crontab
from celery import shared_task
from django.utils import timezone

@shared_task()
def delete_old_foos():
    print("deleting")
    return "completed deleting foos at {}".format(timezone.now())