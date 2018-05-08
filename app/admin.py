from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(SequenceGroups)
admin.site.register(SequenceTheme)
admin.site.register(SequenceSubTheme)
admin.site.register(SequenceReview)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(ProjectReview)
admin.site.register(Message)
admin.site.register(Sequence)
admin.site.register(ProjectSequences)
