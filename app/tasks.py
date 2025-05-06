from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import InvestmentPlan


@shared_task
def send_investment_reminders():
    today = now().date()
    print(f"Today's date: {today}")
    print("Fetching investment plans with notification date today...")
    plans = InvestmentPlan.objects.filter(
        notification_date=today, is_notification_enabled=True)
    
    for plan in plans:
        print(f"Sending reminder for plan: {plan.title}")
        send_mail(
            subject=f'Reminder: Save for your plan - {plan.title}',
            message=f"Dear {plan.user.email},\n\nThis is your reminder to save for your investment plan: '{plan.title}'.",
            from_email='',
            recipient_list=[plan.user.email],
        )


@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Welcome!',
        'Thanks for signing up.',
        '',
        [user_email],
        fail_silently=False,
    )
