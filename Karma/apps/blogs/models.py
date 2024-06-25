from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField

from utils.manager import (
    PublishedBlogManager,
    PublishedBlogCommentManager
)


User = get_user_model()


class Base(models.Model):

    class Status(models.TextChoices):
            DRAFT = 'DF', 'Draft'
            PUBLİSHED = 'PB', 'Published'
    
    created_at = models.DateTimeField(
        'Əlavə edilmə tarixi', 
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Yenilənmə tarixi', 
        auto_now=True
    )
    published_at = models.DateTimeField(
        'Nəşr tarixi', 
        default=timezone.now
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PUBLİSHED
    )

    class Meta:
        abstract=True

    @property
    def created_date(self):
        local_created_time = timezone.localtime(self.created_at)
        return local_created_time.strftime('%d/%m/%Y, %H:%M')
    
    @property
    def updated_date(self):
        local_updated_time = timezone.localtime(self.updated_at)
        return local_updated_time.strftime('%d/%m/%Y, %H:%M')
    
    @property
    def published_date(self):
        local_published_time = timezone.localtime(self.published_at)
        return local_published_time.strftime('%d/%m/%Y, %H:%M')
    

class IP(models.Model):
    view_ip = models.GenericIPAddressField('IP ünvanı', editable=False)

    class Meta:
        verbose_name = ('IP ünvanı')
        verbose_name_plural = ('IP ünvanları')

    def __str__(self) -> str:
        return self.view_ip
    

class Category(models.Model):
    category_name = models.CharField(('Kateqoriya adı'), max_length=150)

    class Meta:
        verbose_name = ('Kateqoriya')
        verbose_name_plural = ('Kateqoriyalar')

    def __str__(self) -> str:
        return self.category_name


class Blog(Base):
    blog_title = models.CharField(('Məqalə başlığı'), max_length=100)
    blog_content = RichTextUploadingField('Məqalə mətni')
    blog_image = models.ImageField('Cover foto', upload_to='blogs/')
    liked_count = models.IntegerField(default=0)
    category = models.ManyToManyField(
        Category, 
        related_name='blogs', 
        verbose_name='Kateqoriya'
    )
    slug=models.SlugField(
        ("Link adı"),
        null=True, blank=True,
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        max_length=500    
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='blogs',
        verbose_name='Müəllif'
    )
    viewed_ips = models.ManyToManyField(
        IP, related_name="blogs", 
        verbose_name='Məqalənin görüntüləndiyi IP ünvanları',
        editable=False
    )
    objects = models.Manager()
    published = PublishedBlogManager()

    class Meta:
        verbose_name = ('Məqalə')
        verbose_name_plural = ('Məqalələr')
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])
        ]
        
    @property
    def view_count(self):
        return self.viewed_ips.count() if self.viewed_ips else 0
    
    def __str__(self) -> str:
        return self.blog_title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.blog_title)
        super().save(*args, **kwargs)
    

class Comment(Base):
    comment_text = models.TextField('Bloq rəyi', max_length=250)
    comment_slug = models.SlugField(
        ("Link adı"),
        null=True, blank=True,
        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
        max_length=500
    )  
    blog = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE, 
        related_name='blog_comments'
    )
    comment_author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_comments',
        verbose_name='Rəy müəllifi'
    )
    objects = models.Manager()
    published = PublishedBlogCommentManager()

    class Meta:
          verbose_name = ('Bloq rəyi')
          verbose_name_plural = ('Bloq rəyləri')
          ordering = ['-published_at']
          indexes = [
            models.Index(fields=['-published_at'])
        ]
            
    @property
    def truncated_comment(self):
        max_words = 3
        words = self.comment_text.split()
        truncated_words = words[:max_words]
        truncated_content = ' '.join(truncated_words)

        if len(words) > max_words:
            truncated_content += ' ...'  

        return truncated_content

    def __str__(self) -> str:
        return self.truncated_comment

