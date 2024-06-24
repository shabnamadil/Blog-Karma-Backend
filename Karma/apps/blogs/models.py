from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


from utils.manager import (
    PublishedBlogManager
)


User = get_user_model()


class Base(models.Model):

    class Status(models.TextChoices):
            DRAFT = 'DF', 'Draft'
            PUBLİSHED = 'PB', 'Published'
    
    created_at = models.DateTimeField('Əlavə edilmə tarixi', auto_now_add=True)
    updated_at = models.DateTimeField('Yenilənmə tarixi', auto_now=True)
    published_at = models.DateTimeField('Nəşr tarixi', default=timezone.now)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

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
    

class IPs(models.Model):
    view_ip = models.GenericIPAddressField('IP ünvanı', editable=False)

    class Meta:
        verbose_name = ('IP ünvanı')
        verbose_name_plural = ('IP ünvanları')

    def __str__(self) -> str:
        return self.view_ip


class Blog(Base):
    blog_title = models.CharField(('Məqalə başlığı'), max_length=150)
    # blog_content = RichTextUploadingField('Məqalə mətni')
    blog_image = models.ImageField('Cover foto', upload_to='blogs/')
    slug=models.SlugField(
                        ("Link adı"),
                        null=True, blank=True,
                        help_text="Bu qismi boş buraxın. Avtomatik doldurulacaq.",
                        max_length=500    
                    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    viewed_ips = models.ManyToManyField(IPs, related_name="blogs", verbose_name='Məqalənin görüntüləndiyi IP ünvanları', editable=False)
    objects = models.Manager()
    published = PublishedBlogManager()

    class Meta:
        verbose_name = ('Məqalə')
        verbose_name_plural = ('Məqalələr')
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])
        ]

