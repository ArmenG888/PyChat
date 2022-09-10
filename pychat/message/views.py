from re import I
from django.shortcuts import render
from .models import dm, message

def home(request):
    dms = []
    for i in dm.objects.all():
        if request.user in i.list_of_people.all():
            dms.append(i)
    return render(request, 'message/home.html', {'dms':dms})    

def dm_detail(request,pk):
    dm_x = dm.objects.get(id=pk)
    return render(request, 'message/dm.html', {'message':dm_x.messages})    
    
