from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from guardian.admin import GuardedModelAdmin

# Register your models here.
from lm.models import *

# - * - * - * -
# MENSAGEM
# - * - * - * -

'''
#MENSAGEM: atividade
class MessageActivityAdmin(admin.ModelAdmin):
    list_display = ('content', 'library','tag_list')

    fieldsets = (
         ('Vamos adicionar uma nova ATIVIDADE no banco de conteúdos', {
             'classes': ('',),
             'fields' : ('library','category','content','tags',
                         'created_date','lang','msg_uuid'),
             'description': '',
         }),)

    readonly_fields=('category','msg_uuid')

    actions_on_bottom = True

    actions_on_top = False

    date_hierarchy = 'altered_date'

    list_filter = ('library', )

    search_fields = ('content', )

    def get_queryset(self, request):
        return super(MessageActivityAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
'''



# - * - * - * -
# AUTOR
# - * - * - * -

#class AuthorAdmin(admin.ModelAdmin):
#    list_display = ('profile', 'first_name', 'last_name')
#    fields = ('_user', 'profile', ('first_name', 'last_name'))


# - * - * - * -
# SEQUENCIA
# - * - * - * -
'''
class SequenceAdmin(admin.ModelAdmin):
    #list_display =  ('theme','subtheme','gp','validator','display_facts','display_activities',
    #                 'display_interactions','display_reinforcements')
    list_display = ('seq_id','theme','subtheme','is_verified',
                    'show_fact','show_activity','show_interaction',
                    'show_reinforcement')
    #raw_id_fields = ['fact']
    fieldsets = (
     ('Sequências', {
         'classes': ('',),
         'fields' : ('library',('theme','subtheme'), ('fact','activity','interaction',
                     'reinforcement'),'desc','gp','seq_uuid'),
         'description': '',
     }),)
    readonly_fields=('seq_uuid',)
    list_filter = ('is_verified','theme','subtheme')
    search_fields = ('seq_id',
                     'theme__theme',
                     'subtheme__sub_theme',
                     'fact__content',
                     'activity__content',
                     'interaction__content',
                     'interaction__content' )
    actions = ['validate_sequence','unvalidate_sequence']

    def validate_sequence(self, request, queryset):
        queryset.update(is_verified=True)
    validate_sequence.short_description = "VALIDAR as sequências selecionadas"

    def unvalidate_sequence(self, request, queryset):
        queryset.update(is_verified=False)
    unvalidate_sequence.short_description = "INVALIDAR as sequências selecionadas"
'''


class SequencesInlineFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        return super(SequencesInlineFormSet, self).save_new(form, commit=commit)

    def save_existing(self, form, instance, commit=True):
        return form.save(commit=commit)


class SequencesInline(admin.TabularInline):
    model = Project.sequences.through
    formset = SequencesInlineFormSet
    verbose_name = 'Sequência'
    verbose_name_plural = 'Sequências'
    extra = 3
    mim_num = 1

    def __str__(self):
        return "teste"

# - * - * - * -
# PROJETO
# - * - * - * -


class ProjectAdmin(GuardedModelAdmin):
    list_display = ('project_name', 'client', 'library', 'is_project_approved')
    fieldsets = (
         ('Projeto', {
             'classes': ('wide',),
             'fields' : ('client', 'project_name','library','is_project_approved'),
             'description': '',
         }),)
    readonly_fields=('prj_uuid',)
    inlines = [SequencesInline, ]
    exclude = ('sequences',)

#-------------------------------------------------


class UserProfileCreationForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserProfileCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserProfileCreationForm
    list_display = ("username","is_creator","is_reviewer")
    fieldsets = (
        (None, {'fields': ('username', 'password', 'is_superuser', 'is_staff', 'is_active', 'is_creator','is_reviewer','groups','user_permissions')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'is_superuser', 'is_staff', 'is_active', 'is_creator','is_reviewer')}
            ),
        )

admin.site.register(UserProfile, CustomUserAdmin)

# default

admin.site.register(SequenceGroups)
admin.site.register(SequenceTheme)
admin.site.register(SequenceSubTheme)
admin.site.register(SequenceReview)
admin.site.register(Client)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectReview)
#admin.site.register(UserProfile, UserAdmin)
admin.site.register(Message)
admin.site.register(Sequence)
admin.site.register(ProjectSequences)


# personalized
#admin.site.register(MessageFact, MessageFactAdmin)
#admin.site.register(MessageInteraction, MessageInteractionAdmin)
#admin.site.register(MessageReinforcement, MessageReinforcementAdmin)
#admin.site.register(MessageActivity, MessageActivityAdmin)
#admin.site.register(Author, AuthorAdmin)
#admin.site.register(Sequence, SequenceAdmin)
