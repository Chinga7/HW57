from django.db import models
from django.urls import reverse

from webapp.validate import not_only_numeric


# Create your models here.
class Project(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=300, null=False, blank=False, verbose_name='Title', validators=(not_only_numeric,))
    description = models.TextField(max_length=300, null=True, blank=True, verbose_name='Description')

    def get_absolute_url(self):
        return reverse('webapp:project_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.pk}. {self.title}'


class Issue(models.Model):
    summary = models.CharField(max_length=300, null=False, blank=False, verbose_name='Summary', validators=(not_only_numeric,))
    description = models.TextField(max_length=300, null=True, blank=True, verbose_name='Description')
    type = models.ManyToManyField('webapp.Type', related_name='issues', blank=True)
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, related_name='status', verbose_name='Status')
    project = models.ForeignKey('webapp.Project', on_delete=models.CASCADE, related_name='issues', verbose_name='projects')
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update At')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def get_absolute_url(self):
        return reverse('webapp:issue_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.pk}. {self.summary}'


class Status(models.Model):
    status_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Status')

    def __str__(self):
        return f'{self.status_name}'


class Type(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Type')

    def __str__(self):
        return f'{self.name}'