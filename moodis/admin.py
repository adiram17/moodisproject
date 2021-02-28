from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import PatientMoodResponse, Profile, Question, ResponseOption, PatientMoodEpisode

# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'user'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


#Register Question Admin
class ResponseOptionInline(admin.TabularInline):
    model = ResponseOption
    extra = 0
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ResponseOptionInline,
    ]
    list_display = [ 'prompt', 'question_type' , 'question_section', 'question_number']
    ordering =['question_type','question_section','question_number']

admin.site.register(Question, QuestionAdmin)

#Register Episode Admin
class PatientMoodResponseOptionInline(admin.TabularInline):
    def has_change_permission(self, request, obj=None):
        return False
        
    model = PatientMoodResponse
    extra = 0
    
class PatientMoodEpisodeAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    inlines = [
        PatientMoodResponseOptionInline,
    ]
    def created_by(str, obj):
        return obj.patient.created_by.full_name
    
    def full_name(str, obj):
        return obj.patient.full_name
    
    list_display = [ 'full_name', 'created_by', 'date' , 'episode']

admin.site.register(PatientMoodEpisode, PatientMoodEpisodeAdmin)