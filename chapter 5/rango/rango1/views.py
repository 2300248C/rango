from django.shortcuts import render

from django.http import HttpResponse

def index(request):

    context_dict ={ 'boldmessage': "Crunchy, creamy,cookie,candy,cupcake!"}
    
    return render(request,'rango/index.html',context=context_dict)

def about(request):
    html = '<a href = "/index/">Home</a><br>'+ '<h1> Rango says about</h1>'

    return HttpResponse(html)
