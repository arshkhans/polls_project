from celery import shared_task
from .models import Question

from datetime import datetime, timedelta

@shared_task(name = "print_msg_main")
def print_message(message, *args, **kwargs):
    print(f"Celery is working!! Message is {message}")

@shared_task(name = "delete_record")
def delete():
    current_time = datetime.now().replace(microsecond=0)
    questions = Question.objects.filter(pub_date__lt=current_time - timedelta(days=1))
    print(questions)
