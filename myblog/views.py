from django.contrib.auth.forms import AuthenticationForm
from django.forms import BaseForm
from django import http
from django.shortcuts import render,redirect
from .models import Post,Category,Profile,Comment,Contactmessage
from django .views import View
from .forms import UserLoginform,UpdateProfileForm,UserregistrationForm,PostCreateForm,CommentForm,ChangePasswordForm,CategoryForm,UpdateEmailForm,ContactForm
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordResetView
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .context_processors import *
from .mixins import SuperUserRequiredMixin

# account registration email activation
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
#prevent error related force_text not found
from django.utils.encoding import force_str as force_text






class Homeview(ListView):

    queryset = Post.objects.all()
    template_name = 'myblog/home.html'
    ordering = ['-post_date']
    paginate_by = '2'



class ProfileAllview(LoginRequiredMixin,ListView):
    
    queryset = User.objects.all()
    template_name = 'myblog/show_all_profile.html'
    ordering = ['username']
    paginate_by = '6'

    login_url = "/login/"
    redirect_field_name = "redirect_to"
        
    

class Myfollowerview(LoginRequiredMixin,View):

    def get(self,request):

        followers = request.user.profile.follows.all().order_by('-user')
        count = followers.count()
       
        
       

        p = Paginator(followers,8)
        page = request.GET.get('page')
    
        try:
            followers = p.page(page)
        except PageNotAnInteger:
            followers = p.page(1)
        except EmptyPage:
            followers = p.page(p.num_pages)


        
        context={'followers':followers,'title':'followers','count':count}
        return render(self.request,'myblog/all_follower.html',context)
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    

class Myfollowview(LoginRequiredMixin,View):
    
    def get(self,request):
        
      
        followers = request.user.profile.followed_by.all().order_by('-user')
        count = followers.count()
        

        p = Paginator(followers,8)
        page = request.GET.get('page')
    
        try:
            followers = p.page(page)
        except PageNotAnInteger:
            followers = p.page(1)
        except EmptyPage:
            followers = p.page(p.num_pages)
        
        context={'followers':followers,'title':'follows','count':count}
        return render(self.request,'myblog/all_follower.html',context)
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"






class Postview(View):

    def get(self,request,pk):

        category = get_object_or_404(Category,pk=pk)
        posts = Post.objects.filter(category=category).order_by('-post_date')

        paginator = Paginator(posts, 1)
        page_number = request.GET.get("page")
        posts = paginator.get_page(page_number)

        context={'posts':posts}
        return render(request,'myblog/posts.html',context)
    


class Commentview(View):

    def get(self,request,pk):

        post = get_object_or_404(Post,pk=pk)
        
        comments = Comment.objects.filter(post=post).order_by('-comment_date')
        comments_number = comments.count()

        paginator = Paginator(comments, 8)
        page_number = request.GET.get("page")
        comments = paginator.get_page(page_number)

        context={'comments':comments,'comments_number':comments_number,'post':post}
        return render(request,'myblog/show_comments.html',context)
    
    def post(self,request,pk):

        if request.user.is_authenticated:

            post = get_object_or_404(Post,pk=pk)

            comment = self.request.POST.get('comment')
            if comment:
                
                comment_post, created =  Comment.objects.get_or_create(comment_text=comment,comment_user=request.user,post=post)
                messages.success(request,'You posted new comment')
                return redirect('show_comment',pk)
        else:
            return redirect('show_comment',pk)
    


class Editcommentview(LoginRequiredMixin,View):

    def get(self,request,pk):

        comment = get_object_or_404(Comment,pk=pk)

        if comment.comment_user == self.request.user:

            form = CommentForm(instance=comment)
            context = {'form':form}
            
            return render(self.request,'myblog/update_comment.html',context)
        
        else:
            messages.error(self.request,'Permission denied')
            return redirect('forbidden_access')

    def post(self,request,pk):
        
        comment = get_object_or_404(Comment,pk=pk)

        if comment.comment_user == self.request.user:
        
            form = CommentForm(self.request.POST,instance=comment)

            if form.is_valid():
                form.save()
                messages.success(self.request,'Comment updated')
                return redirect('show_comment',comment.post.pk)
            
            else:
                for error in  list(form.errors.values()):
                    messages.error(self.request,error)
                    return redirect(request.META.get('HTTP_REFERER'))
        
        else:
            messages.error(self.request,'Permission denied')
            return redirect('forbidden_access')
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class Deletecommentview(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):

    model = Comment

    template_name = 'myblog/confirm_delete.html'
    
    def get_success_message(self,cleaned_data):
            return('Comment deleted' )
    
    def get_success_url(self,**kwargs):

        return reverse_lazy('show_comment',kwargs={'pk': self.object.post.pk})
    
    def test_func(self):

        object = self.get_object()
        if object.comment_user == self.request.user:
            return True
        else:
            messages.error(self.request,'You have no permission')
            return False
            
    def handle_no_permission(self):
        return redirect('forbidden_access')    

    login_url = "/login/"
    redirect_field_name = "redirect_to"


class commentlikeview(LoginRequiredMixin,SuccessMessageMixin,View):
    
    def post(self,request,pk):
       
        comment = get_object_or_404(Comment,pk=pk)

        if comment.like.filter(id=request.user.id):
            comment.like.remove(request.user)
            messages.error(request,'You disliked the comment')

        else:
            comment.like.add(request.user)
            messages.success(request,'You liked the comment')


        return redirect(request.META.get('HTTP_REFERER'))
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ReplyCommentView(View):

    def post(self,request,pk):

        comment = get_object_or_404(Comment,pk=pk)
        
        reply_message = self.request.POST.get('reply_message')
        
        Comment.objects.create(comment_text=reply_message,comment_user = self.request.user, post = comment.post, reply = comment)
        comment.save()
        messages.success(self.request,'You Reply saved')
        return  redirect('show_comment', comment.post.pk)





class Postlikeview(LoginRequiredMixin,SuccessMessageMixin,View):
    
    def post(self,request,pk):
       
        post = get_object_or_404(Post,pk=pk)

        if post.like.filter(id=request.user.id):
            post.like.remove(request.user)
            messages.error(request,'You disliked the comment')

        else:
            post.like.add(request.user)
            messages.success(request,'You liked the comment')


        return redirect(request.META.get('HTTP_REFERER'))
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class AddCategoryView(SuperUserRequiredMixin,SuccessMessageMixin,CreateView):

    model = Category
    form_class = CategoryForm
    template_name = 'myblog/universal_form.html'

    
    def form_invalid(self,form):

            for error in list(form.errors.values()):
                messages.error(self.request,error) 

            return self.render_to_response(self.get_context_data(form=form))


    def get_success_message(self,cleaned_data):
            return('New category has been created' )
    

    def get_success_url(self):
      return reverse_lazy('home')
    
    def get_context_data(self, *args, **kwargs):
        context = super(AddCategoryView,self).get_context_data(*args, **kwargs)

        context['page_name'] = "add_category"
        return context
    
            
    def handle_no_permission(self):
        return redirect('forbidden_access')
    





class PostCreateview(LoginRequiredMixin,SuccessMessageMixin,CreateView):

    model = Post

    form_class = PostCreateForm
    template_name = 'myblog/universal_form.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def get_success_message(self,cleaned_data):
            return('New post has been created' )
    

    def get_success_url(self):
      return reverse_lazy('home')
    

    def get_context_data(self, *args, **kwargs):
        context = super(PostCreateview,self).get_context_data(*args, **kwargs)

        context['page_name'] = "create_post"
        return context
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"




class PostDetailview(DetailView):

    model = Post
    template_name = 'myblog/post_detail.html'

    def get_context_data(self,*args,**kwargs):
        context=super(PostDetailview,self).get_context_data(*args,**kwargs)

        post_detail = get_object_or_404(Post,pk=self.kwargs['pk'])

        context['post_detail'] = post_detail
        return context
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class PostEditview(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):

    model = Post

    form_class = PostCreateForm
    template_name = 'myblog/universal_form.html'
    
    def get_success_message(self,cleaned_data):
            return('Post updated' )
    
    def get_success_url(self):

        return reverse_lazy('home')
    
    def test_func(self):

        object = self.get_object()
        if object.author == self.request.user:
            return True
        else:
            messages.error(self.request,'You have no permission')
            return False
        
    def get_context_data(self, *args, **kwargs):
        context = super(PostEditview,self).get_context_data(*args, **kwargs)

        context['page_name'] = "edit_post"
        return context
            
    def handle_no_permission(self):
        return redirect('forbidden_access')    

    login_url = "/login/"
    redirect_field_name = "redirect_to"


class Deletepostview(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,DeleteView):

    model = Post
    template_name = 'myblog/confirm_delete.html'
    
    def get_success_message(self,cleaned_data):
            return('Post deleted' )
    
    def get_success_url(self):

        return reverse_lazy('home')
    
    def test_func(self):

        object = self.get_object()
        if object.author == self.request.user:
            return True
        else:
            messages.error(self.request,'You have no permission')
            return False
            
    def handle_no_permission(self):
        return redirect('forbidden_access')  


    login_url = "/login/"
    redirect_field_name = "redirect_to"


class Myloginview(SuccessMessageMixin,LoginView):

    template_name = 'myblog/login.html'
    form_class = UserLoginform
    redirect_authenticated_user = True

   
    def get_success_message(self,cleaned_data):
        return(f'{self.request.user} logged in successfully' )


    def form_invalid(self,form):
        messages.error(self.request,'Invalid Username or password')
        return self.render_to_response(self.get_context_data(form=form))
    

    def get_success_url(self):

        if self.request.user.is_superuser:
            try:
                self.request.user.profile
                return reverse('home')
            except:
                Profile.objects.create(user=self.request.user,pk=self.request.user.pk)
                messages.warning(self.request,'please fill your profile information')
                return reverse('edit_profile',kwargs={'pk':self.request.user.profile.pk})

        else:

            if self.request.user.profile.avatar and self.request.user.profile.bio:
                return reverse_lazy('home')
        
            else:
                messages.warning(self.request,'please fill your profile information')
                return reverse('edit_profile',kwargs={'pk':self.request.user.profile.pk})

   



class Mylogoutview(LogoutView):


    def get_success_message(self,cleaned_data):
        return(f'{self.request.user} logged out successfully' )
    
    def get_success_url(self):
      
      return reverse_lazy('login')


class ShowProfileView(LoginRequiredMixin,DetailView):
    
    model = Profile
    template_name = 'myblog/user_profile.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ShowProfileView,self).get_context_data(*args,**kwargs)

        user_profile = get_object_or_404(Profile,pk=self.kwargs['pk'])
        context['user_profile'] = user_profile
        return context
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class EditProfileView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):


    model = Profile

    form_class = UpdateProfileForm
    template_name = 'myblog/update_profile.html'
    
    def get_success_message(self,cleaned_data):
            return('Profile updated' )
    
    def get_success_url(self):

        return reverse_lazy('home')
    
    def test_func(self):

        object = self.get_object()
        if object.user == self.request.user:
            return True
        else:
            messages.error(self.request,'Permission denied')
            return False
        
            
    def handle_no_permission(self):
        return redirect('forbidden_access')    
    
 


    login_url = "/login/"
    redirect_field_name = "redirect_to"


class UpdateEmailView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):

    model = User
    template_name = 'myblog/universal_form.html'

    form_class = UpdateEmailForm

    def get_success_message(self, cleaned_data):

        return('Email address updated')
    
    def get_success_url(self,**kwargs):
        return reverse_lazy('edit_profile',kwargs={'pk': self.object.profile.pk})
    
    def test_func(self):
        object = self.get_object()
        if object.pk == self.request.user.pk:
            return True
        else:
            messages.error(self.request,'Permission denied')
            return False
        
    def get_context_data(self, *args, **kwargs):
        context = super(UpdateEmailView,self).get_context_data(*args, **kwargs)

        context['page_name'] = "edit_mail"
        return context
        

    def handle_no_permission(self):
        return redirect('forbidden_access')
    

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class MyuserSingnupview(SuccessMessageMixin,CreateView):

    form_class = UserregistrationForm
    template_name = 'myblog/user_reg.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        Profile.objects.create(user = user, pk=user.pk)
        

        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        try:
            user.email_user(subject=subject, message=message)

            messages.success(self.request,'To finish registration please check your mailbox including spam folder and follow instructions')
        except:
            messages.error(self.request,'Mail Server Connection problem, please turn to website admin')

        return super().form_valid(form)


    def form_invalid(self,form):

            for error in list(form.errors.values()):
                messages.error(self.request,error) 

            return self.render_to_response(self.get_context_data(form=form))
     

    def get_success_url(self):

        return reverse_lazy('login')
    


def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your registration finished now please login')
        return redirect('login')

    else:
        return render(request, 'activation_invalid.html')

    


class UserFollowview(LoginRequiredMixin,SuccessMessageMixin,View):
    
    def post(self,request,pk):
       
      
        profile = get_object_or_404(Profile,pk=pk)

        if profile.follows.filter(id=request.user.profile.id):
            profile.follows.remove(request.user.profile)
            messages.error(request,f'You now unfollowed {profile.user.username}')

        else:
            profile.follows.add(request.user.profile)
            messages.success(request,f'You now followed {profile.user.username}')
        

        return redirect(request.META.get('HTTP_REFERER'))
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class CustompasswordchangeView(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):

    form_class = ChangePasswordForm
    template_name = 'myblog/universal_form.html'

    
    def get_success_message(self, cleaned_data):
        return('Your password has been changed successfully')
    
   

    def get_success_url(self):
        return reverse_lazy('edit_profile',kwargs={'pk': self.request.user.profile.pk})
    
    def get_context_data(self, *args, **kwargs):
        context = super(CustompasswordchangeView,self).get_context_data(*args, **kwargs)

        context['page_name'] = "password_change"
        return context

  
    def form_invalid(self,form):

            for error in list(form.errors.values()):
                messages.error(self.request,error) 
            return self.render_to_response(self.get_context_data(form=form))
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):

    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'

    success_message = "we sent email for you with instructions to change your password." \
                      " if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    
    success_url = reverse_lazy('home')



class ContactMessageView(SuccessMessageMixin,CreateView):

    template_name = 'myblog/universal_form.html'
    form_class = ContactForm

    def get_success_message(self, cleaned_data):
        return ('Your message has been sent and stored')
    
    def get_success_url(self):

        return reverse_lazy('home')
    
    
    def form_invalid(self,form):

        for error in list(form.errors.values()):
            messages.error(self.request,error)   
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, *args, **kwargs):
        context = super(ContactMessageView,self).get_context_data(*args, **kwargs)

        context['page_name'] = "contact_message"
        return context
    
    
class ShowmessageView(SuperUserRequiredMixin,SuccessMessageMixin,ListView):

    model = Contactmessage
    template_name = 'myblog/show_messages.html'

    ordering = ['full_name']
    paginate_by = '5'
    

class forbidden_access(View):

    def get(self,request):

        return render(self.request,'myblog/forbidden_access.html')


class Aboutview(View):

    def get(self,request):

        return render(self.request,'myblog/about.html')
    

class Privacyview(View):

    def get(self,request):

        return render(self.request,'myblog/privacy.html')
    

class Termsview(View):

    def get(self,request):

        return render(self.request,'myblog/terms.html')







        



    


    


    
    

    







       

