from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GENDER_CHOICES=[
       ('Male', 'Male'),
       ('Female', 'Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    def __unicode__(self):
        return self.full_name
    def __str__(self):
        return self.full_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Question(models.Model): 
    SELECTION = [
        ('Questionaire 1', 'Mood Questionaire'),
        ('Questionaire 2', 'Closing Questionaire'),
    ]
    question_type = models.CharField(max_length=100, choices=SELECTION)
    question_section = models.CharField(max_length=255)
    question_number = models.IntegerField(default=0)
    prompt = models.TextField(max_length=255) 
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    def __unicode__(self):
        return self.prompt
    def __str__(self):
        return self.prompt

class ResponseOption(models.Model): 
    text = models.CharField(max_length=255) 
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Response Option'
        verbose_name_plural = 'Response Options'
        
    def __unicode__(self):
        return str(self.score)+" "+self.text
    def __str__(self):
        return str(self.score)+" "+self.text

class UserMoodResult(models.Model): 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True,blank=True)
    accumulative_score = models.IntegerField(default=0)
    result_category= models.CharField(max_length=50)
    result_description = models.TextField(max_length=255)

    class Meta:
        verbose_name = 'User Mood Result'
        verbose_name_plural = 'User Mood Result'