from celery import Celery
from celery.schedules import crontab
from .reminder_tasks import send_quiz_reminder


# Initialize Celery
celery = Celery("tasks", broker="redis://localhost:6379/0")
celery.conf.broker_connection_retry_on_startup = True


celery.conf.beat_schedule = {
    'send-quiz-reminder-every-day': {
        'task': 'reminder_tasks.send_quiz_reminder',
        'schedule': crontab(hour=8, minute=0),  # Daily at 8 AM
    },
}
