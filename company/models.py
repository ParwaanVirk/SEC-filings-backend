from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Deferrable, UniqueConstraint
# Create your models here.


class CompanyS(models.Model):
    id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=500, default="")
    CIK_Number = models.CharField(max_length=50, default="", unique=True)
    Ticket_Number = models.CharField(max_length=50, default="")

    def __str__(self) -> str:
        return str(self.Name)


Form_Type = [
    ('10k', '10k'),
    ('10q', '10q'),
    ('8k', '8k'),
]


class Forms(models.Model):
    id = models.BigAutoField(primary_key=True)
    EDGAR_Link = models.URLField()
    Form_Type = models.CharField(
        max_length=3, choices=Form_Type, default="10k")
    CompanyS = models.ForeignKey(CompanyS, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.CompanyS + " || " + self.Form_Type)


Metric_type = [
    ('Type1', 'GrowthRate'),
    ('Type2', 'CAC'),
]
def current_year():
    return datetime.date.today().year
def max_value_current_year(value):
    return MaxValueValidator(current_year())
Quarter_Type = [
    ('1', '1st quarter'),
    ('2', '2nd quarter'),
    ('3', '3rd quarter'),
    ('4', '4th quarter'),
]

class Metrics(models.Model):
    id = models.BigAutoField(primary_key=True)
    Metric_Type = models.CharField(
        max_length=5, choices=Metric_type, default="Type1")
    Value = models.FloatField(default=0.0)
    Source_Link = models.URLField()
    Year = models.IntegerField(('year'), validators=[MinValueValidator(
        2015), max_value_current_year], default=current_year)
    Quarter = models.CharField(max_length=1, choices=Quarter_Type, default=1)
    CompanyS = models.ForeignKey(CompanyS, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["Metric_Type", "Source_Link", "Year", "Quarter", "CompanyS"], name='unique_value')
        ]


class Performance(models.Model):
    id = models.BigAutoField(primary_key=True)
    Growth = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    Profitability = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    Investibility = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    CompanyS = models.ForeignKey(CompanyS, on_delete=models.CASCADE)
