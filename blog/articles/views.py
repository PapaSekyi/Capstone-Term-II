from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse

from . import models 


from django.contrib.auth import logout

from . forms import LoginForm,USerRegistration,ArticleRegistrationForm,GenreForm

from django.contrib.auth import authenticate, login

from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator


# Create your views here.


def custom_logout(request):
    logout(request)
    return redirect(reverse('logout_done'))

def logout_done(request):
    return render(request,'logout.html')

def articles(request):
    article=models.article.objects.all()
    paginator=Paginator(article,1)
    page=request.GET.get('page')
    try:
        article=paginator.page(page)
    except PageNotAnInteger:
        article=paginator.page(1) 
    except EmptyPage:
        article =paginator.page(paginator.num_pages) 

    context={
        'article':article,
        'page':page,
    }
    return render(request,'articles.html',context=context) 

def article_detail(request,slug):
    article=get_object_or_404(models.article,slug=slug)
    return render(request,'article_detail.html',context={'article':article})

def user_login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user=authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                return redirect(reverse('articles:arti'))
            else:
                return HttpResponse("Invalid Credentials") 
    else:
        form= LoginForm()

        return render(request,'login.html')
    

    
def register(request):
    if request.POST:
        user_form=USerRegistration(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False) # not saving the form in the database as of now as we have to check the two passwords.
            new_user.set_password(user_form.cleaned_data['password'])# we are setting the user password.
            new_user.save()
            username=user_form.cleaned_data['username']
            return render(request,'registration_done.html',{'username':username})
        else:
            raise user_form.errors # NOT_valid form is not working as of now for the username and 

    else:
        user_form=USerRegistration()
        return render(request,'registration.html',{'uform':user_form})

from django.utils.text import slugify
import uuid

def add_article(request):
    if request.POST:
        article_form = ArticleRegistrationForm(request.POST)

        if article_form.is_valid():
            article=article_form.save(commit=False)
            article.author=request.user
            unique_id = uuid.uuid4().hex[:10].upper() # Generate a 10-character uppercase UUID
            slug = slugify(unique_id)
            article.slug=slug 
            article.save()
            return redirect(reverse('articles:arti'))
        else:
            return HttpResponse("Some error in the Saving of the Form")
    else:
        article_form=ArticleRegistrationForm()
        return render(request,'article_add.html',{'article_form':article_form}) 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView,DeleteView

class UpdateArticleMixin(LoginRequiredMixin, UpdateView):
    model = models.article
    form_class = ArticleRegistrationForm
    template_name = 'article_update.html'
    
    def get_success_url(self):
        slug=self.object.slug
        return reverse('articles:article_detail',kwargs={'slug':slug})
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class DeleteArticleMixin(LoginRequiredMixin, DeleteView):
    model = models.article
    success_url = reverse_lazy('articles:arti')
    template_name = 'article_delete.html'

    def get_success_url(self):
        return self.success_url
    

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .prediction_model import predict_next_word,train_model

@csrf_exempt
def predict_next_words(request):
    if request.method == 'POST':
        sentence = request.POST.get('sentence')
        words = sentence.split()[-4:]
        genre = request.session.get('genre', None)
        size = request.session.get('size', None)

        predictions = predict_next_word(input_text=words, genre=genre,size=size) 
        return JsonResponse({'predictions': predictions})
    

def get_genre(request):
    if request.POST:
        form = GenreForm(request.POST)
        genre=request.POST.get('genre')
        abc=train_model(genre)
        request.session['genre']=genre
        size=abc 
        request.session['size']=size
        return redirect(reverse('articles:add_article'))
    else:
        form=GenreForm()
        return render(request,'get_genre.html',{'form':form})
    





    


