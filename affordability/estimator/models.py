from django.db import models

# Create your models here.
class AffordabilityInput(models.Model):
    income = models.FloatField()
    down_payment = models.FloatField()
    loan_term = models.IntegerField() # in years
    interest_rate = models.FloatField()

    def __str__(self):
        return f'Affordability Input: {self.income}, {self.down_payment}, {self.loan_term}, {self.interest_rate}'