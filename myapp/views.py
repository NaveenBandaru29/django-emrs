from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contact,Profile,Song
from keras.models import load_model
# from time import sleep
from keras.preprocessing.image import img_to_array
# from keras.preprocessing import image
import cv2
import numpy as np
from scipy import stats


# Create your views here.
def Index(request):
    if request.user.is_authenticated:
         return redirect("home")
    return render(request,"index.html")

def About(request):
    return render(request,"index.html")

def ContactUs(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email1")
        phone = request.POST.get("phonenumber")
        desc = request.POST.get("description")

        if name == "":
                messages.warning(request,"Username is empty")
                return redirect("index")
        elif email == "":
                messages.warning(request,"Email is empty")
                return redirect("index")
        elif phone == "":
                messages.warning(request,"Phone number is empty")
                return redirect("index")
        elif desc == "":
                messages.warning(request,"Description is empty")
                return redirect("index")



        myquery = Contact(name=name,email=email,phonenumber=phone,description=desc)
        myquery.save()
        messages.info(request,("Thanks for contacting us"))
        return render(request,"index.html")
    return render(request,"index.html")


@login_required(login_url="login")
def Home(request):
    return render(request,"home.html")


def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print("User :",user)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request,("Invalid Username or Password"))
    return render(request,"login.html")



def SignUp(request):
    if request.method=="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        if pass1!=pass2:
            messages.info(request,"Passwords does not match")
            return redirect("signup")
        
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Username is already taken")
                return redirect("signup")
        except Exception as identifier:
            pass

        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email is already taken")
                return redirect("signup")
        except Exception as identifier:
            pass


        newUser= User.objects.create_user(username=username,email=email,password=pass1)
        newUser.save()
        messages.success(request,"User is created successfully! Please Login")
        return redirect("login")

    return render(request,"signup.html")



@login_required(login_url="login")
def Logout(request):
    logout(request)
    messages.success(request,"Log Out Success!!")
    return redirect("login")


@login_required(login_url="login")
def profile(request):
    if request.method == "POST":
        my_profile = request.user.profile
        name = request.POST.get("name")
        language = request.POST.get("language")
        artist = request.POST.get("artist")
        musician = request.POST.get("musician")
        my_profile.artist = artist
        my_profile.language = language
        my_profile.musician = musician
        my_profile.save()
        messages.success(request,"Profile updated successfully!!")


    context = {}
    name = str(request.user).title()
    user =  User.objects.filter(username=request.user).values()[0]
    pro = Profile.objects.filter(username=request.user).values()
    if pro:
         pro = pro[0]
    else:
         pro = Profile.objects.create(username = request.user)
    context = {
        "name":name,
        "user":user,
        "pro":pro,
    }

    return render(request,"profile.html",context)



def run(request):
    in_or_out = "login"
    face_classifier = cv2.CascadeClassifier(r'C:\Users\Bandaru Naveen\OneDrive\Documents\\4th Year PROJECT\Emotion_Detection_CNN-main\haarcascade_frontalface_default.xml')
    classifier =load_model(r'C:\Users\Bandaru Naveen\OneDrive\Documents\\4th Year PROJECT\Emotion_Detection_CNN-main\model.h5')

    emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']
    labelsList = []
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    i=0
    while i<10:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)

                prediction = classifier.predict(roi)[0]
                label=emotion_labels[prediction.argmax()]
                labelsList.append(label)
                label_position = (x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            else:
                cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imshow('Emotion Detector',frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        i+=1

    cap.release()
    cv2.destroyAllWindows()

    if request.user.is_authenticated:
        in_or_out = "logout"
        pro = Profile.objects.filter(username=request.user).values()[0]
        # print(pro)
        language = pro["language"]
        artist = pro["artist"]
        musician = pro["musician"]
        # print(musician,artist,language)

        if label=="" or  label=="Neutral":
            label = "Neutral"
            song = Song.objects.filter(emotion = "Happy",language = language,artist = artist,musician =musician)
        else:
            label = stats.mode(labelsList)[0][0]
            if label == "Happy":
                song = Song.objects.filter(emotion = label,language = language,artist = artist,musician =musician)
            else:
                song = Song.objects.filter(emotion = label,language = language,artist = artist,musician =musician) | Song.objects.filter(emotion = 'Happy',language = language,artist = artist,musician =musician)
    else:
        in_or_out = "login"
        if label=="" or  label=="Neutral":
            label = "Neutral"
            song = Song.objects.filter(emotion = "Happy")

            print()
            print()
            print(song)

        else:
            label = stats.mode(labelsList)[0][0]
            if label == "Happy":
                song = Song.objects.filter(emotion = label)


                print()
                print()
                print(song)
            else:
                song = Song.objects.filter(emotion = label) | Song.objects.filter(emotion = 'Happy')

                print()
                print()
                print(song)
                
             

    return render(request,"run.html",{"songs":song,"emotion":label,"iio":in_or_out})


def playSongs(request):
    song = Song.objects.all()
    return render(request,"play.html",{"songs":song})


def onlyHappy(request):
     label = "Happy"
     song = Song.objects.filter(emotion = label)
     return render(request,"run.html",{"songs":song,"emotion":label})

def onlySad(request):
     label = "Sad"
     song = Song.objects.filter(emotion = label)
     return render(request,"run.html",{"songs":song,"emotion":label})