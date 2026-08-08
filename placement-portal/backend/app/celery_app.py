from celery import Celery

from celery.schedules import crontab
celery = Celery(
    "placement_portal",

    broker="redis://localhost:6379/0",

    backend="redis://localhost:6379/0"
)


celery.conf.beat_schedule = {

    "daily-deadline-reminders": {

        "task":
            "app.tasks.reminder_tasks.send_deadline_reminders",

        "schedule": 60.0

    },

    "monthly-placement-report": {

    "task":
        "app.tasks.report_tasks.generate_monthly_report",

    "schedule": crontab(
        day_of_month=1,
        hour=9,
        minute=0
    )

}
}


celery.conf.update(

    task_serializer="json",

    accept_content=["json"],

    result_serializer="json",

    timezone="Asia/Kolkata",

    enable_utc=False

)