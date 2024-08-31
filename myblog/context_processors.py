from .models import Category,Profile,Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

def navbar_context(request):
 

    return {'Category_menu': Category.objects.all(),'Profiles':Profile.objects.all(),'post_count':Post.objects.count()}

def sidebar_context(request):
    if request.user.is_authenticated:

        myposts = Post.objects.filter(author=request.user).order_by('-post_date')
        
        p = Paginator(myposts,3)
        page = request.GET.get('page2')
    
        try:
            Myposts = p.page(page)
        except PageNotAnInteger:
            Myposts = p.page(1)
        except EmptyPage:
            Myposts = p.page(p.num_pages)


        return {'Myposts':Myposts}
    else:
        return {}
    


    
  
