from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User



# Create your models here.

class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug=slugify(self.name)
        return super(Tag,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200,blank=True)
    image = models.ImageField(null=True,blank=True,upload_to='images/')
    tags = models.ManyToManyField(Tag,blank=Tag,related_name='post')
    view_count = models.IntegerField(null=Tag,blank=Tag,default=0)
    is_featured = models.BooleanField(default=False)
    



class Comments(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    website = models.CharField(max_length=200)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,blank=True,related_name='replies')
    


    



