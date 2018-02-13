from django.shortcuts import render

from django.http import HttpResponse

from models import Category
def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    
    return render(request,'rango/index.html',context=context_dict)

def about(request):
    html = '<a href = "/index/">Home</a><br>'+ '<h1> Rango says about</h1>'

    return HttpResponse(html)

def show_category(request,category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    
    try:

        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)
        
 
        context_dict['pages'] = pages

        context_dict['category'] = category
     
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None


    context_dict['query'] = category.name

    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['query'] = query
    context_dict['result_list'] = result_list

    return render(request, 'rango/category.html', context_dict)
