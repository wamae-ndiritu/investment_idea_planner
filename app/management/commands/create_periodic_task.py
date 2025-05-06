from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create a periodic task for sending investment reminders daily'

    def handle(self, *args, **kwargs):
        # Create or get the schedule
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='*/5',
            hour='*',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )

        task_name = 'app.tasks.send_investment_reminders'
        task_label = 'Daily Investment Reminder 2'

        try:
            periodic_task = PeriodicTask.objects.get(name=task_label)
            # Update the existing task
            periodic_task.crontab = schedule
            periodic_task.task = task_name
            periodic_task.enabled = True
            periodic_task.save()
            self.stdout.write(self.style.SUCCESS(
                f'Updated existing periodic task: {task_label}'))
        except PeriodicTask.DoesNotExist:
            # Create new task
            PeriodicTask.objects.create(
                name=task_label,
                task=task_name,
                crontab=schedule,
                enabled=True,
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created new periodic task: {task_label}'))
