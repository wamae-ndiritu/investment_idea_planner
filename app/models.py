from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('user must have an email address.')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    

class InvestmentIdea(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    content = models.TextField()
    price_range = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

class InvestmentPlan(models.Model):
    title = models.CharField(max_length=200)
    investment_idea = models.ForeignKey(InvestmentIdea, on_delete=models.CASCADE, related_name='investment_plans')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='investment_plans')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_notification_enabled = models.BooleanField(default=False)
    

    def default_pay_day():
        today = datetime.today()
        last_day_of_month = (today.replace(day=28) + timedelta(days=4)).day
        return last_day_of_month

    pay_day = models.IntegerField(default=default_pay_day)

    def __str__(self):
        return self.title
    
    def get_timeline(self):
        return f'{self.start_date} - {self.end_date}'
    
    def get_no_of_months(self):
        return (self.end_date.year - self.start_date.year) * 12 + self.end_date.month - self.start_date.month
    
    def get_monthly_savings(self):
        return self.target_amount / self.get_no_of_months()
    
    def total_savings(self):
        return sum([saving.amount for saving in self.savings.all()])
    
    def target_balance(self):
        return self.target_amount - self.total_savings()

class Saving(models.Model):
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='savings')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.investment_plan.title} - {self.amount}'

class Notification(models.Model):
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='notifications')
    subject = models.CharField(max_length=200)
    recepient = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.investment_plan.title} - {self.message}'




