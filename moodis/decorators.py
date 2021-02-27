from .models import Profile, UserMoodResult
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime

#to check if user already check for today 
def is_checked_today(function):
    #wrapper for function check, if true return function else redirect to home
    def wrapper(request, *args, **kwargs):
        try:
            #check if user already check today
            #TODO add check logic
            ischecked = False
            user_profile = Profile.objects.get(user=request.user)
            user_mood_result = UserMoodResult.objects.filter(profile=user_profile, date=datetime.now().date()).first()
            if (user_mood_result!=None):
                ischecked=True
            if ischecked:
                return redirect("/postcheck") #if already check return to postcheck
            else:
                return function(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, "Internal Error: "+str(e))
            return redirect("/")
    return wrapper