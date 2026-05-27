from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    return render(request,"home.html")

def loginu(request):
    if request.method == "POST":
        un = request.POST.get("username")
        ps = request.POST.get("password")
        try:
            user = User.objects.get(username=un)
        except User.DoesNotExist:
            return render(request,"loginu.html",{"error":"User Not Found...Please Try Again"})
        user = authenticate(request,username=un,password=ps)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            return render(request,"loginu.html",{"error":"Invalid Credentials..."})
    else:
        return render(request,"loginu.html")

def registeru(request):
    if request.method=="POST":
        un = request.POST.get("username")
        em = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        obj = User.objects.filter(username=un).exists()
        if obj :
            return render(request,'registeru.html',{'error':"User Already Exist...Please try again"})
        elif password!= cpassword:
            return render(request,'registeru.html',{'error':"Password and ConfirmPassword does not match"})
        else:
            obj = User(username=un,email=em,password=password)
            obj.save()
        return redirect("loginu")
    else:
        return render(request,"registeru.html")

def logoutu(request):
    logout(request)
    return redirect("loginu")
    

def forgot_password(request):
    return render(request,"forgotpass.html")
