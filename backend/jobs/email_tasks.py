from celery import Celery
from backend.utils.email import send_email
from app import create_app
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
celery = Celery("tasks", broker="redis://localhost:6379/0")
celery.conf.broker_connection_retry_on_startup = True



def init_celery(app):
    celery.conf.update(app.config)
    celery.Task = AppContextTask
    return celery

class AppContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with create_app().app_context():
            return self.run(*args, **kwargs)

@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def send_welcome_email(self, user_email):
    try:
        subject = "Welcome to the Quiz Platform!"
        body = "Thank you for signing up. Start taking quizzes today!"
        send_email(user_email, subject, body)
        logger.info(f"Welcome email successfully sent to {user_email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user_email}: {e}")
        raise self.retry(exc=e)
