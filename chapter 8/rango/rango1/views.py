from django.shortcuts import render
from django.http import HttpResponse
from forms import PageForm,CategoryForm

from models import Category,Page
def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    
    return render(request,'rango/index.html',context=context_dict)

def about(request):
    html = "<a href =" +  "{% url 'index' %}"">Home</a><br>"+ '<h1> Rango says about</h1>'

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

    return render(request, 'rango/category.html', context=context_dict)



def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():

            category = form.save(commit=True)
            print(category, category.slug)

            return index(request)
        else:
           
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})



def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                # probably better to use a redirect here.
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}

    return render(request, 'rango/add_page.html',context=context_dict)


