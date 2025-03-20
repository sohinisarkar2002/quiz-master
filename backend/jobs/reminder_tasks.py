from celery import Celery
from backend.utils.email import send_email
from backend.database import db
from backend.models import UserQuizAttempt, User
from app import create_app
from datetime import datetime, timedelta
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

@celery.task(base=AppContextTask)
def send_quiz_reminder():
    reminder_time = datetime.utcnow() - timedelta(days=7)
    
    # Efficient batch processing to improve performance
    users_to_remind = (
        db.session.query(User.email)
        .join(UserQuizAttempt, User.id == UserQuizAttempt.user_id)
        .filter(UserQuizAttempt.score == 0, UserQuizAttempt.quiz_id.isnot(None))
        .limit(100)  # Batch size for improved efficiency
        .all()
    )

    for user_email, in users_to_remind:
        try:
            subject = "Reminder: Take Your Quiz!"
            body = "You have unfinished quizzes. Come back and complete them!"
            send_email(user_email, subject, body)
            logger.info(f"Reminder successfully sent to {user_email}")
        except Exception as e:
            logger.error(f"Failed to send reminder to {user_email}: {e}")
