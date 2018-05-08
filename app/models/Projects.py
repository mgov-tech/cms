from django.db import models
from uuid import uuid4
from .Clients import Client
from .Sequences import Sequence
from .Profiles import UserProfile

from django.utils import timezone
from django.utils.html import escape, mark_safe


class Project(models.Model):
    prj_id = models.AutoField(primary_key=True)

    prj_uuid = models.UUIDField(default=uuid4, unique=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client")

    PROJECT_TYPE = (
        ('EM', 'EDUQMAIS'),
        ('PM', 'POUPEMAIS'),
    )
    library = models.CharField(max_length=10, blank=True, choices=PROJECT_TYPE, verbose_name="Biblioteca")

    color = models.CharField(max_length=7, default='#997bff')

    sequences = models.ManyToManyField(Sequence, blank=True, related_name="sequences", through='ProjectSequences')

    project_name = models.CharField(max_length=160)

    is_project_approved = models.BooleanField(blank=True, default=False, verbose_name="Aprovado?")

    class Meta:
        app_label = 'lm'
        verbose_name = 'PROJETO'
        verbose_name_plural = 'PROJETOS'
        permissions = (('can_review_project', 'Pode revisar projetos'),)

    def get_project_badge(self):
        library = escape(self.library)
        if library == 'EM':
            library = 'eduqmais'
        if library == 'PM':
            library = 'poupemais'
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">&nbsp;%s&nbsp</span>' % (color, library)
        return mark_safe(html)

    def sequences_count(self):
        return self.sequences.count()

    def __str__(self):
        return str(self.project_name)


class ProjectReview(models.Model):
    """
    Cada projetos pode receber reviews nas sequências, este modelo
    registra estas informações
    """

    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)

    projectreview_uuid = models.UUIDField(default=uuid4, unique=True)

    is_project_reviewed = models.BooleanField(blank=True, default=False, verbose_name="Revisado?")
    project_reviews = models.TextField(blank=True, max_length=300, verbose_name='Como esta sequência pode melhorar?')

    created_date = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    altered_date = models.DateTimeField(blank=True, null=True, verbose_name="Alterado em ")

    is_fact_flagged = models.BooleanField(blank=True, default=False, verbose_name="Fato")
    is_activity_flagged = models.BooleanField(blank=True, default=False, verbose_name="Atividade")
    is_interaction_flagged = models.BooleanField(blank=True, default=False, verbose_name="Interação")
    is_reinforcement_flagged = models.BooleanField(blank=True, default=False, verbose_name="Reforço")


    def __str__(self):
        return str(self.id) + ' ' + self.project_reviews + ' (' + self.user.username + ')'


class ProjectSequences(models.Model):
    """
    Conectando Projetos <> Sequencias (though) e armazenando informações pertinentes para este contexto
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="from_projectsequence")
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name="from_projectsequence")
    order = models.PositiveSmallIntegerField(unique=True)

    projectsequencereview_uuid = models.UUIDField(default=uuid4, unique=True)

    is_reviewed = models.BooleanField(blank=True, default=False, verbose_name="Revisado?")

    project_reviews = models.ManyToManyField(ProjectReview, blank=True, verbose_name='sss')

    created_date = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    altered_date = models.DateTimeField(blank=True, null=True, verbose_name="Alterado em ")


    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.project.project_name + ' <---> ' + self.sequence.desc + '  ' + str(self.order)