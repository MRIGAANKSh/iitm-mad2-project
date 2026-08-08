from app import create_app

from app.celery_app import celery

from app.tasks.export_tasks import (
    export_student_applications
)
from app.tasks.reminder_tasks import (
    send_deadline_reminders
)
from app.tasks.report_tasks import (
    generate_monthly_report
)

app = create_app()


class FlaskTask(celery.Task):

    def __call__(self, *args, **kwargs):

        with app.app_context():

            return self.run(
                *args,
                **kwargs
            )


celery.Task = FlaskTask