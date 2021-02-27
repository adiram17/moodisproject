from django import forms
from .decorators import is_checked_today
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactForm, ProfileForm, ProfileViewForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Question, ResponseOption, UserMoodResult
from datetime import datetime

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
                profile.birth_date = request.POST['birth_date']
                profile.save()
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

def about(request):
    return render(request, 'pages/about.html', {})

def contact(request):
    form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})

def test(request):
    #messages.success(request, "Ini adalah message info")
    return render(request, 'pages/test.html', {})

@login_required
def home(request):
    return render(request, 'pages/home.html', {})

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.profile.full_name = request.POST['full_name']
        user.profile.email = request.POST['email']
        user.profile.phone = request.POST['phone']
        user.profile.gender = request.POST['gender']
        user.profile.birth_date = request.POST['birth_date']
        try:
            user.save()
            messages.success(request, "Informasi profil berhasil diperbaharui")
            return redirect('detail')
        except Exception as e:
            print("Terjadi kesalahan. "+str(e))
            messages.error(request, "Terjadi kesalahan. "+str(e))
            return redirect('profile')
    else:
        form = ProfileForm(
            initial={
                'username':request.user.username,
                'full_name':request.user.profile.full_name,
                'email':request.user.email,
                'phone':request.user.profile.phone,
                'gender':request.user.profile.gender,
                'birth_date':request.user.profile.birth_date,
            }
        )
        return render(request, 'pages/profile.html', {'form': form})


@login_required
@is_checked_today
def precheck(request):
    return render(request, 'pages/precheck.html', {})

@login_required
@is_checked_today
def check(request):
    if request.method == 'POST':
        #TODO fuzzy logic here and save into user information detail
        score1 = request.POST['flexRadioDefault1'] 
        score2 = request.POST['flexRadioDefault2'] #dst
        print("Score 1:"+str(score1))
        print("Score 2:"+str(score2))
        user_profile= Profile.objects.get(user=request.user)
        user_mood_result=UserMoodResult(
            profile=user_profile,
            accumulative_score=25,
            result_category="BIPOLAR",
            result_description="80% Kecenderungan Bipolar"
            )
        user_mood_result.save()
        messages.success(request, "Submit questionaire berhasil")
        return redirect('postcheck')
    else:
        questions = Question.objects.filter(question_type='Questionaire 1').order_by('question_number')
        response_options=None
        for question in questions:
            response_option_temp=ResponseOption.objects.filter(question=question.id) 
            if (response_options==None):
                response_options=response_option_temp #initiate
            else:
                response_options = response_options|response_option_temp 
        return render(request, 'pages/check.html', {'questions':questions, 'response_options':response_options})

@login_required
def postcheck(request):
    user_profile = Profile.objects.get(user=request.user)
    user_mood_result = UserMoodResult.objects.filter(profile=user_profile, date=datetime.now().date()).first()
    return render(request, 'pages/postcheck.html', {'user_mood_result':user_mood_result})

@login_required
def detail(request):
    form = ProfileViewForm(
        initial={
                'full_name':request.user.profile.full_name,
                'email':request.user.email,
                'phone':request.user.profile.phone,
                'gender':request.user.profile.gender,
                'birth_date':request.user.profile.birth_date,
            }
    )
    user_profile = Profile.objects.get(user=request.user)
    user_mood_results = UserMoodResult.objects.filter(profile=user_profile)
    return render(request, 'pages/detail.html', {'form':form, 'user_mood_results':user_mood_results})


@login_required
def deleteUserMoodResult(request, id):
    user_profile = Profile.objects.get(user=request.user)
    user_mood_result = UserMoodResult.objects.filter(profile=user_profile, id=id).first()
    if (user_mood_result!=None):
        user_mood_result.delete()
        messages.success(request, "Data berhasil dihapus")
    else:
        messages.error(request, "Terjadi kesalahan. Data gagal dihapus")
    return redirect('detail')
    