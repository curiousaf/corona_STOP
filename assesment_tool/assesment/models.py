from django.db import models
from django_countries.fields import CountryField


# Create your models here.

class Question(models.Model):
    question_id = models.IntegerField()
    country = CountryField(blank_label='(select country)')
    text = models.CharField(max_length=1000)
    yes = models.CharField(max_length=50)
    no = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class Output(models.Model):
    output_id = models.IntegerField()
    country = CountryField(blank_label='(select country)')
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text

class Result(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    output = models.ForeignKey(Output, on_delete=models.CASCADE)
    country = CountryField()

    def __str__(self):
        return self.output.text
    