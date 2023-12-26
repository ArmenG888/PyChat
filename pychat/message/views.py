from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import dm, message, server
from .forms import MessageForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import random
import openai
from django.contrib.auth.models import User
  
openai.api_key = ""

def dms(user):
    dms = []
    for i in dm.objects.all():
        if user in i.list_of_people.all():
            dms.append(i)
    return dms

@login_required(login_url='/login/')
def home(request):
    return render(request, 'message/home.html', {'dms':dms(request.user)})    

def ajax(request, pk):
    request.user.profile.last_online = timezone.now()
    request.user.profile.save()
    dm_x = dm.objects.get(id=pk)
    messages = message.objects.all().filter(chat=dm_x)
    messages_x = {}
    for i in messages:
        
        messages_x[i.id] = [i.from_user.username, i.text, i.time.strftime("%m/%d/%Y") + " at " + i.time.strftime("%I:%M %p")]

    online = {}
    for i in dm_x.list_of_people.all():
        online[i.username] = i.profile.online()
    return JsonResponse({'online':online, 'messages':messages_x})


messages_gpt = []

@login_required(login_url='/login/')
def dm_detail(request,pk):
    
    dm_x = dm.objects.get(id=pk)
    messages = message.objects.all().filter(chat=dm_x)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            if dm_x.gpt != True:
                txt = form.cleaned_data['text']
                if txt.find("``") != -1:
                    math_equation = txt[txt.find("``"):]
                    math_equation = math_equation.replace("``", "$$")
                    math_equation = math_equation.replace("/", "\over")
                    math_equation = math_equation.replace("sqrt", "\sqrt")
                    math_equation = math_equation.replace("tan", "\tan")
                    math_equation = math_equation.replace("(", "{")
                    math_equation = math_equation.replace(")", "}")
                    math_equation = math_equation.replace("+-", "\pm")
                    math_equation = math_equation.replace("!=", "\\ne")
                    txt=math_equation
                    print(txt)
                elif txt.find("/random_number") != -1:
                    random_number = txt.replace("/random_number","")
                    random_numbers = random_number.split("(")[1].replace(")","").split(",")
                    random_number = random.randint(int(random_numbers[0]),int(random_numbers[1]))
                    txt += " --- " + str(random_number)
                elif txt.find("/yes_no()") != -1:
                    txt += " --- yes" if random.randint(1,2) == 2 else " --- no"
                message.objects.create(chat=dm_x, from_user=request.user, text=txt)     
            else:
                txt = form.cleaned_data['text']
                messages_gpt.append({"role": "user", "content": txt})

                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages_gpt
                )
                response = chat.choices[0].message.content
                usr = User.objects.get(username="gpt")
                message.objects.create(chat=dm_x, from_user=request.user, text=txt) 
                message.objects.create(chat=dm_x, from_user=usr, text=response)    
            
            return redirect('dm', pk)
    else:
        form = MessageForm()
    
    return render(request, 'message/dm.html', {'form':form,'dms':dm.objects.get(id=pk), 'dm':dms(request.user), 'messages':messages, 'servers':server.objects.all()})    
    
