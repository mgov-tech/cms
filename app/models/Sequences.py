from django.db import models
from uuid import uuid4
from django.utils import timezone
from django.utils.html import escape, mark_safe
from .Messages import Message
from .Clients import Client


class SequenceGroups(models.Model):
    """Classe apenas para permitir adicionar grupos de faixa etária"""
    age_group = models.CharField(max_length=50)

    class Meta:
        app_label = 'app'
        verbose_name = 'Grupos de idade'
        verbose_name_plural = 'Grupos de idade'

    def __str__(self):
        return '   ' + self.age_group


class SequenceTheme(models.Model):
    """Classe apenas para permitir adicionar listas de temas"""
    theme = models.CharField(max_length=50)

    class Meta:
        app_label = 'app'
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'

    def __str__(self):
        return '   ' + self.theme


class SequenceSubTheme(models.Model):
    """Classe apenas para permitir adicionar listas de subtemas"""
    sub_theme = models.CharField(max_length=50)

    class Meta:
        app_label = 'app'
        verbose_name = 'Subtema'
        verbose_name_plural = 'Subtemas'

    def __str__(self):
        return '   ' + self.sub_theme


class Sequence(models.Model):
    seq_id = models.AutoField(primary_key=True)

    seq_uuid = models.UUIDField(default=uuid4, unique=True)

    theme = models.ForeignKey(SequenceTheme, on_delete=models.CASCADE, verbose_name="Tema", related_name="themes")

    subtheme = models.ForeignKey(SequenceSubTheme, null=True, blank=True, on_delete=models.CASCADE, verbose_name="SubTema", related_name="subthemes")

    desc = models.CharField(max_length=50, blank=True, verbose_name="Observação/Descrição")

    gp = models.ManyToManyField(SequenceGroups, blank=True, verbose_name="Grupo de Idade", related_name="age_groups")

    messages = models.ManyToManyField(Message, blank=True, verbose_name="Sequência", related_name="messages")

    # - * - * -
    is_verified = models.BooleanField(blank=True, default=False, help_text="Conferido?", verbose_name="Verificado")
    validator_review = models.TextField(blank=True, max_length=300, default='')

    PROJECT_TYPE = (
        ('EM', 'EDUQMAIS'),
        ('PM', 'POUPEMAIS'),
    )
    library = models.CharField(max_length=10, blank=True, choices=PROJECT_TYPE, verbose_name="Biblioteca")

    class Meta:
        app_label = 'app'
        verbose_name = 'SEQUÊNCIA'
        verbose_name_plural = 'SEQUÊNCIAS'

    def __str__(self):
        return '#' + str(self.seq_id) + ' - ' + self.desc

    def get_fact(self):
        try:
            c = self.messages.filter(category='FA')[0].content
        except:
            return ""


        html = '%s <span class="badge badge-secondary badge-pill">%s</span>' % (c, len(c))
        return mark_safe(html)

    def get_activity(self):
        try:
            c = self.messages.filter(category='AT')[0].content
        except:
            return ""

        html = '%s <span class="badge badge-secondary badge-pill">%s</span>' % (c, len(c))
        return mark_safe(html)

    def get_interaction(self):
        try:
            c = self.messages.filter(category='IT')[0].content
        except:
            return ""

        html = '%s <span class="badge badge-secondary badge-pill">%s</span>' % (c, len(c))
        return mark_safe(html)

    def get_reinforcement(self):
        html = ''
        try:
            c = self.messages.filter(category='RE')
            for i, msg in enumerate(c):
                answer = ''
                if msg.msg_format == 'S':
                    answer = 'SIM'
                if msg.msg_format == 'N':
                    answer = 'NÃO'
                if msg.msg_format == 'O':
                    answer = 'OUTRO'

                if i >= 1:
                    html += '<hr>'

                html += '''<span class="badge badge-warning badge-pill">%s</span> 
                           %s 
                           <span class="badge badge-secondary badge-pill">%s</span>
                        ''' % (answer, msg.content, len(msg.content))
        except:
            return ""

        return mark_safe(html)


'''
    def show_fact(self):
        text = self.fact.content
        return text
    show_fact.short_description = 'FATO'

    def show_activity(self):
        text = self.activity.content
        return text
    show_activity.short_description = 'ATIVIDADE'

    def show_interaction(self):
        text = self.interaction.content
        return text
    show_interaction.short_description = 'INTERAÇÃO'

    def show_reinforcement(self):
        text = self.reinforcement.content
        return text
    show_reinforcement.short_description = 'REFORÇO'
'''



#class Validator(models.Model):
#    val_id = models.AutoField(primary_key=True)


class SequenceReview(models.Model):
    sequencereview_id = models.AutoField(primary_key=True)

    seq_uuid = models.UUIDField(default=uuid4, unique=True)

    what_sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name="sequences_of")

    is_fact_checked = models.BooleanField(blank=False, verbose_name="Precisa de revisão?")
    reviews_fact = models.TextField(blank=True, max_length=300, default='')

    is_activity_checked = models.BooleanField(default=False, blank=False, verbose_name="Precisa de revisão?")
    reviews_activity = models.TextField(blank=True, max_length=300, default='')

    is_interaction_checked = models.BooleanField(default=False, blank=False, verbose_name="Precisa de revisão?")
    reviews_interaction = models.TextField(blank=True, max_length=300, default='')

    is_reinforcements_checked = models.BooleanField(default=False, blank=False, verbose_name="Precisa de revisão?")
    reviews_reinforcements = models.TextField(blank=True, max_length=300, default='')

    created_date = models.DateTimeField(default=timezone.now, verbose_name="Criado em")

    altered_date = models.DateTimeField(blank=True, null=True, verbose_name="Alterado em ")

    def __str__(self):
        return '' + str(self.sequencereview_id)

