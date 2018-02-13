from django.shortcuts import render
from django.http import HttpResponse
from forms import PageForm,CategoryForm,UserProfileForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

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

    # Get query text for search function
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the result list!
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context_dict)



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
                page.first_visit = timezone.now()
                page.last_visit = timezone.now()
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def save(self, *args, **kwargs):
    if slugify(self.name):
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data= request.POST)
        profile_form = UserProfileForm(data = requst.POST)

        if user_form_is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered =True
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'rango/register.html',{'user_form':user_form,'profile_form': profile_form,
                                                 'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password =password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResonse("Your Rango account is disable")
        else:
            print("Invalid login details: {0},{1}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'rango/login.http',{})


def some_view(request):
    if not request.user.is_authenticated():
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")

def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



