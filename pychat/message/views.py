from django.shortcuts import render
from .models import dm, message
from .forms import MessageForm
def home(request):
    dms = []
    for i in dm.objects.all():
        if request.user in i.list_of_people.all():
            dms.append(i)
    return render(request, 'message/home.html', {'dms':dms})    

def dm_detail(request,pk):
    
    dm_x = dm.objects.get(id=pk)
    messages = message.objects.all().filter(chat=dm_x)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message.objects.create(chat=dm_x, from_user=request.user, text=form.cleaned_data['text'])     
    else:
        form = MessageForm()
    dms = []
    for i in dm.objects.all():
        if request.user in i.list_of_people.all():
            dms.append(i)
    return render(request, 'message/dm.html', {'message':messages, 'form':form,'dms':dms})    
    
