from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import dm, message
from .forms import MessageForm
from django.utils import timezone
def dms(user):
    dms = []
    for i in dm.objects.all():
        if user in i.list_of_people.all():
            dms.append(i)
    return dms
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

def dm_detail(request,pk):
    
    dm_x = dm.objects.get(id=pk)
    messages = message.objects.all().filter(chat=dm_x)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message.objects.create(chat=dm_x, from_user=request.user, text=form.cleaned_data['text'])     
            return redirect('dm', pk)
    else:
        form = MessageForm()
    
    return render(request, 'message/dm.html', {'form':form,'dms':dm.objects.get(id=pk), 'dm':dms(request.user), 'messages':messages})    
    
