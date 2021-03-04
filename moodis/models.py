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
    phone = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(default=0)
    
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

class Patient(models.Model):
    GENDER_CHOICES=[
       ('Male', 'Male'),
       ('Female', 'Female')
    ]
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    age = models.IntegerField(default=0)
    is_self = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.full_name
    def __str__(self):
        return self.full_name


class Question(models.Model): 
    SELECTION = [
        ('Questionaire 1', 'Mood Questionaire'),
        ('Questionaire 2', 'Closing Questionaire'),
    ]
    question_code = models.CharField(max_length=10)
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


class PatientResponse(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_score = models.IntegerField(default=0)
    class Meta:
        abstract = True

class PatientMoodEpisode(models.Model): 
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(blank=True)
    episode_score = models.FloatField()
    episode_category = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Patient Mood Episode'
        verbose_name_plural = 'Patient Mood Episode'

#extend from patient response
class PatientMoodResponse(PatientResponse):
    patient_mood_episode = models.ForeignKey(PatientMoodEpisode, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Patient Mood Response'
        verbose_name_plural = 'Patient Mood Responses'
