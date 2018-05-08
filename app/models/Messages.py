from django.db import models
from django.utils import timezone
from uuid import uuid4
from taggit.managers import TaggableManager
from django.utils.html import escape, mark_safe


class Message(models.Model):
    # toda mensagem contem dois identificadores únicos, um auto-incremental
    msg_id = models.AutoField(primary_key=True)
    msg_uuid = models.UUIDField(default=uuid4,unique=True)

    PROJECT_TYPE = (
        ('EM', 'EDUQMAIS'),
        ('PM', 'POUPEMAIS'),
    )
    library = models.CharField(max_length=10, choices=PROJECT_TYPE, verbose_name="Biblioteca")

    # limite maximo de 160 caracteres
    content = models.TextField(max_length=160, help_text="Máximo 160 caracteres", verbose_name="Mensagem")

    created_date = models.DateTimeField(default=timezone.now, verbose_name="Criado em")

    altered_date = models.DateTimeField(blank=True, null=True, verbose_name="Alterado em ")

    MSG_LANG = (
        ('pt-br', 'Português'),
        ('es', 'Espanho'),
        ('fr', 'Francês'),
    )
    lang = models.CharField(blank=True, max_length=10, choices=MSG_LANG, default='pt-br', verbose_name="Idioma")

    tags = TaggableManager(verbose_name="Tags")

    color = models.CharField(max_length=7, default='#007bff')

    MSG_TYPE = (
            ('IN', 'Introdução'),
            ('FA', 'Fato'),
            ('AT', 'Atividade'),
            ('IT', 'Interação'),
            ('RE', 'Reforço'),
            ('XX', 'Outro')
    )
    category = models.CharField(max_length=10, choices=MSG_TYPE, default='FA', verbose_name="Tipo")

    MSG_FORMAT = (
            ('R', 'Regular'),
            ('S', 'SIM'),
            ('N', 'NÃO'),
            ('O', 'Outro'),
    )
    msg_format = models.CharField(max_length=10, choices=MSG_FORMAT, default='R', verbose_name="Formato da Mensagem")

    class Meta:
        permissions = (("can_write_msg", "Can write messages"),)
        app_label = 'lm'
        verbose_name = 'MENSAGEM'
        verbose_name_plural = 'MENSAGENS'

    # funções utilizada no HTML
    def get_msgtype_badge(self):
        name = escape(self.category)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

    def get_msglen(self):
        _len = len(self.content)
        html = '<span class="badge badge-secondary badge-pill">%s</span>' % (_len)
        return mark_safe(html)

    def __str__(self):
        return '(' + self.msg_format + ') '+ self.category + ':   ' + self.content
