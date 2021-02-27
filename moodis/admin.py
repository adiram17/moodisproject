from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, Question, ResponseOption, UserMoodResult

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


class UserMoodResultAdmin(admin.ModelAdmin):
    def username(str, obj):
        return obj.profile.user.username
    def fullname(str, obj):
        return obj.profile.full_name
    search_fields = ['profile__user__username','profile__full_name','result_category']
    list_display = [ 'username', 'fullname', 'date' , 'accumulative_score', 'result_category', 'result_description']
admin.site.register(UserMoodResult, UserMoodResultAdmin)