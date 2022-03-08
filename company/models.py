from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Deferrable, UniqueConstraint
# Create your models here.


class CompanyS(models.Model):
    id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=500, default="")
    CIK_Number = models.CharField(max_length=50, default="")
    Ticket_Number = models.CharField(max_length=50, default="")

    def __str__(self) -> str:
        return str(self.Name)


Form_Type = [
    ('Type1', '10k'),
    ('Type2', '10q'),
    ('Type3', '8k'),
]


class Forms(models.Model):
    EDGAR_Link = models.URLField()
    Form_Type = models.CharField(
        max_length=5, choices=Form_Type, default="Type1")
    CompanyS = models.ForeignKey(CompanyS, on_delete=models.CASCADE)


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
    Metric_Type = models.CharField(
        max_length=5, choices=Metric_type, default="Type1")
    Value = models.FloatField(default=0.0)
    Source_Link = models.URLField()
    Year = models.IntegerField(('year'), validators=[MinValueValidator(
        2015), max_value_current_year], default=current_year)
    Quarter = models.CharField(max_length=1, choices=Quarter_Type, default=1)
    CompanyS = models.ForeignKey(CompanyS, on_delete=models.CASCADE)
    # TODO: How will we ensure unique combo of Metric_Type, year, quarter, and company. Task -- Akanksha
    # TODO: Change all the models so that their admin show their names. Task -- Divya

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["Metric_Type", "Source_Link", "Year", "Quarter", "CompanyS"], name='unique_value')
        ]


class Performance(models.Model):
    Growth = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    Profitability = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    Investibility = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    CompanyS = models.ForeignKey(CompanyS, on_delete=models.CASCADE)
