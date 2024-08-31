from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField


class Category(models.Model):

    name = models.CharField(max_length=250, null=True, blank=True)
    short_desc = models.CharField(max_length=250, null=True, blank=True)


    def __str__(self):

        return self.name
    
    class Meta:

        verbose_name_plural = "Categories"
    

class Post(models.Model):

    title = models.CharField(max_length=250, null=True, blank=True, unique=True)
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    body = HTMLField(max_length=3000,default="",blank=True)
    likes = models.ManyToManyField(User, related_name="post_blog", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/post_images')
    like = models.ManyToManyField(User, related_name="post_like", blank=True )

    def __str__(self):

        return f'{self.title}--by:  {self.author.username}'
    

class  Comment(models.Model):

    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200, blank=True, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name="comment_like", blank=True )
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comment_reply', null=True, blank=True)


    def __str__(self):

        return f'{self.comment_user}-{self.comment_date}'
    
    @property
    def get_reply(self):
        return Comment.objects.filter(reply=self).reverse()
    
    @property
    def is_reply(self):
        if self.reply is None:
            return True
        return False
    


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True )
    avatar = models.ImageField(null=True, blank=True, upload_to='images/profile_avatars')
    bio = models.TextField(max_length=300, null=True, blank=True)
    fb_link = models.CharField(max_length=100, null=True, blank=True)
    linkedin_link = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        
        return self.user.username
    
    def get_absolute_url(self):

        return reverse('home')
    
    @property
    def imageURL(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url


class Contactmessage(models.Model):

    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=800)
    message_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return  f'{self.full_name}--{self.subject}'
