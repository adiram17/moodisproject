from django import forms
from .decorators import is_checked_today
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactForm, PatientCheckForm, PatientForm, PatientViewForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, PatientMoodResponse, PatientMoodEpisode, Profile, Question, ResponseOption
from datetime import datetime

def about(request):
    return render(request, 'pages/about.html', {})

def contact(request):
    form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})

def test(request):
    #messages.success(request, "Ini adalah message info")
    return render(request, 'pages/test.html', {})

#TODO add email activation
def signup(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'], password = request.POST['password1'])
                profile = user.profile
                profile.full_name = request.POST['full_name'] 
                profile.email = request.POST['email'] 
                profile.phone = request.POST['phone'] 
                profile.gender = request.POST['gender'] 
                profile.age = request.POST['age']
                profile.save()

                #auto add registered user as patient, self registered user as patient when sign up
                patient = Patient(
                    created_by=profile,
                    full_name=profile.full_name,
                    gender=profile.gender,
                    age=profile.age,
                    is_self = True
                )
                patient.save()
                
                messages.success(request, "User berhasil dibuat. Silakan login dengan akun terdaftar.")
                return redirect('home')
            except Exception as e:
                messages.error(request, "Terjadi kesalahan. "+str(e))
                return render(request, "pages/signup.html", {'form':form})
        else:
            messages.error(request, "Terjadi kesalahan")
            return render(request, "pages/signup.html", {'form':form})
    else:
        form = UserCreationForm
        return render(request,'pages/signup.html', {'form':form})


@login_required
def home(request):
    return render(request, 'pages/home.html', {})

@login_required
def patientEdit(request):
    patient_id = request.GET['patient_id']
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        patient.full_name = request.POST['full_name']
        patient.gender = request.POST['gender']
        patient.age = request.POST['age']
        try:
            patient.save()
            if (patient.is_self):
                profile = Profile.objects.get(id=request.user.profile.id)
                profile.full_name = patient.full_name 
                profile.gender = patient.gender 
                profile.age = patient.age 
                profile.save()
            messages.success(request, "Informasi profil berhasil diperbaharui")
            return redirect('precheck')
        except Exception as e:
            print("Terjadi kesalahan. "+str(e))
            messages.error(request, "Terjadi kesalahan. "+str(e))
            return redirect('patient_edit?patient_id='+str(patient_id))
    else:
        form = PatientForm(
            initial={
                'full_name':patient.full_name,
                'gender':patient.gender,
                'age':patient.age,
            }
        )
        return render(request, 'pages/patient_edit.html', {'patient_id':patient_id,'form': form})

@login_required
def patientAdd(request):
    form = PatientForm()
    if request.method == 'POST':
        patient=Patient()
        patient.full_name = request.POST['full_name']
        patient.gender = request.POST['gender']
        patient.age = request.POST['age']
        patient.created_by = request.user.profile
        patient.is_self = False
        try:
            patient.save()
            messages.success(request, "User berhasil ditambah")
            return redirect('precheck')
        except Exception as e:
            print("Terjadi kesalahan. "+str(e))
            messages.error(request, "Terjadi kesalahan. "+str(e))
            return redirect('precheck')
    else:
        return render(request, 'pages/patient_add.html', {'form': form})


@login_required
def precheck(request):
    patient_self=Patient.objects.get(created_by=request.user.profile, is_self=True)
    patient_others=Patient.objects.filter(created_by=request.user.profile, is_self=False)
    return render(request, 'pages/precheck.html', {'patient_self':patient_self, 'patient_others':patient_others})

@login_required
def check(request):
    patient_id=request.GET['patient_id']
    patient = Patient.objects.get(id=patient_id)
    questions = Question.objects.filter(question_type='Questionaire 1').order_by('question_number')
    if request.method == 'POST':
        
        date = request.POST['date']

        #pre generate patient mood episode
        patient_mood_episode=PatientMoodEpisode(
            date = date,
            patient=patient,
            episode="MANIA",
            )
        patient_mood_episode.save()
        
        #save answer
        for question in questions:
            answer_score = request.POST['option'+str(question.question_number)] 
            patient_mood_response =PatientMoodResponse(
                patient_mood_episode=patient_mood_episode,
                question=question,
                patient = patient,
                answer_score= answer_score,
            )
            patient_mood_response.save()
        
        #TODO add fuzzy process to update episode result based on patient answers
        patient_mood_episode.episode="MANIA"

        patient_mood_episode_id = patient_mood_episode.id
        messages.success(request, "Submit kuesioner berhasil")
        return redirect('/postcheck/?patient_id='+str(patient_id)+'&patient_mood_episode_id='+str(patient_mood_episode_id))
    else:
        form = PatientCheckForm(
            initial={
                'full_name':patient.full_name,
                'gender':patient.gender,
                'age':patient.age,
                'date': datetime.now().date()
            }
        )
        response_options=None
        for question in questions:
            response_option_temp=ResponseOption.objects.filter(question=question.id) 
            if (response_options==None):
                response_options=response_option_temp #initiate
            else:
                response_options = response_options|response_option_temp 
        return render(request, 'pages/check.html', {'form':form, 'questions':questions, 'response_options':response_options})

@login_required
def postcheck(request):
    patient_id=request.GET['patient_id']
    patient_mood_episode_id=request.GET['patient_mood_episode_id']
    patient_mood_episode = PatientMoodEpisode.objects.get(id=patient_mood_episode_id)
    return render(request, 'pages/postcheck.html', {'patient_id':patient_id, 'patient_mood_episode':patient_mood_episode})

@login_required
def patientDetail(request):
    patient_id= request.GET['patient_id']
    patient=Patient.objects.get(id=patient_id)
    form = PatientViewForm(
        initial={
                'full_name':patient.full_name,
                'gender':patient.gender,
                'age':patient.age,
            }
    )
    patient_mood_episodes = PatientMoodEpisode.objects.filter(patient=patient)
    return render(request, 'pages/patient_detail.html', {'patient_id':patient_id, 'form':form, 'patient_mood_episodes':patient_mood_episodes})

@login_required
def patientDelete(request, patient_id):
    patient=Patient.objects.get(id=patient_id)
    try:
        if (patient!=None):
            patient.delete()
            messages.success(request, "Data berhasil dihapus")
    except Exception as e:
        messages.error(request, "Terjadi kesalahan. Data gagal dihapus. "+str(e))
    return redirect('precheck')

@login_required
def patientMoodEpisodeDetail(request):
    patient_mood_episode_id= request.GET['patient_mood_episode_id']
    patient_mood_episode=PatientMoodEpisode.objects.get(id=patient_mood_episode_id)
    patient_mood_responses = PatientMoodResponse.objects.filter(patient_mood_episode=patient_mood_episode)
    return render(request, 'pages/patient_mood_episode_detail.html', {'patient_mood_episode':patient_mood_episode, 'patient_mood_responses':patient_mood_responses})

@login_required
def patientMoodEpisodeDelete(request, id):
    patient_mood_episode = PatientMoodEpisode.objects.get(id=id)
    patient_id = patient_mood_episode.patient.id
    if (patient_mood_episode!=None):
        patient_mood_episode.delete()
        messages.success(request, "Data berhasil dihapus")
    else:
        messages.error(request, "Terjadi kesalahan. Data gagal dihapus")
    return redirect('/patient_detail/?patient_id='+str(patient_id))
    