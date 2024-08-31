from django import forms
from .models import Profile,User,Post,Category,Comment,Contactmessage
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm



class UserLoginform(AuthenticationForm):

    def __init__(self,*args,**kwargs):
        super(UserLoginform,self).__init__(*args,**kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter username',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'
        } ))


    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

        }))




class UpdateProfileForm(forms.ModelForm):

    avatar=forms.ImageField(required=True)

    bio = forms.CharField(widget=forms.Textarea(attrs={

        'placeholder':'Enter profile bio',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'
    }),required=True)

    fb_link = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter facebook link',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'
        
        }),required=False)
    
    linkedin_link = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter linkedin link',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

        }),required=False)
    
    website = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter own website link',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

        }),required=False)   
    
    class Meta:
        model = Profile
        fields=('avatar','bio','fb_link','linkedin_link','website')


class UserregistrationForm(UserCreationForm):


    email = forms.CharField(widget=forms.EmailInput(attrs={

        'placeholder':'Enter email',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    username = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter Username',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={

        'placeholder':'Enter Password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={

        'placeholder':'Repeat password ',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    usable_password = None

    class Meta:

        model = User

        fields=('username','email','password1','password2')


class PostCreateForm(forms.ModelForm):


    title = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter title',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))
    subtitle = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter subtitle',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))
 

    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={

        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))


    class Meta:

        model = Post
        fields=('title','subtitle','body','category','image')


class CommentForm(forms.ModelForm):

    comment_text = forms.CharField(widget=forms.Textarea(attrs={

        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    class Meta:
        model = Comment
        fields=('comment_text',)


class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(widget = forms.PasswordInput(attrs={

        'placeholder':'Enter old password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    })) 

    new_password1 = forms.CharField(label='New password ',widget = forms.PasswordInput(attrs={

        'placeholder':'Enter old new password ',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    new_password2 = forms.CharField(label='Retype New Password',widget = forms.PasswordInput(attrs={

        'placeholder':'Repeat new password',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))


    class Meta:
        model = User

        fileds=('old_password','new_password1','new_password2')



class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category
        fields=('name','short_desc')


    name = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter Category name',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    short_desc = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter Short Description',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))


class UpdateEmailForm(forms.ModelForm):

    class Meta:
        model = User
        fields=('email',)

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Enter Email',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))   


class ContactForm(forms.ModelForm):

    class Meta:

        model = Contactmessage
        fields=('full_name','email','subject','message')


    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter your full name',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'


    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Enter your email address',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'

    }))

    subject = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter the subject',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'


    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':'Enter message',
        'class':'w-full rounded-md py-2.5 px-4 border text-sm outline-[#f84525]'


    }))