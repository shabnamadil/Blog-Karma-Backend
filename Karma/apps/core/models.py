from typing import Iterable
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe

from ckeditor_uploader.fields import RichTextUploadingField


class Base(models.Model):
    created_at=models.DateTimeField("Əlavə edilmə tarixi", default=timezone.now)
    updated_at=models.DateTimeField("Yenilənmə tarixi", auto_now=True)

    class Meta:
        abstract=True


class Singleton(Base):

    class Meta:
        abstract=True

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class ContactInformation(Singleton):
    location = models.CharField('Ünvan', max_length=200)
    number = models.CharField('Əlaqə nömrəsi', max_length=10)
    email = models.EmailField('Email', unique=True)
    linkedin = models.URLField(unique=True, null=True, blank=True)
    facebook = models.URLField(unique=True, null=True, blank=True)
    instagram = models.URLField(unique=True, null=True, blank=True)
    whatsapp = models.URLField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Əlaqə məlumatı'
        verbose_name_plural='Əlaqə məlumatı'

    def __str__(self) -> str:
        return 'Əlaqə məlumatı'
    

class AboutUs(Singleton):
    company_name = models.CharField('Müəssisənin adı',  max_length=100)
    content = RichTextUploadingField('Haqqımızda')

    class Meta:
        verbose_name = 'Haqqımızda'
        verbose_name_plural = 'Haqqımızda'  

    def __str__(self) -> str:
        return f'{self.company_name} haqqında məlumat'
    
    @property
    def truncated_content(self):
        max_words = 3
        words = self.content.split()
        truncated_words = words[:max_words]
        truncated_content = ' '.join(truncated_words)

        if len(words) > max_words:
            truncated_content += ' ...'  

        return mark_safe(truncated_content)
    

class ContactMessage(Base):
    message_by = models.CharField('Kimdən', max_length=200, null=True)
    subject = models.CharField('Mövzu', max_length=255)
    message = models.TextField('Mesaj', max_length=300)

    class Meta:
        verbose_name = 'Mesaj'
        verbose_name_plural = 'Mesajlar'

    def __str__(self) -> str:
        return f'{self.message_by} adlı şəxs sizə mesaj göndərib'
    
    @property
    def truncated_message(self):
        max_words = 3
        words = self.message.split()
        truncated_words = words[:max_words]
        truncated_content = ' '.join(truncated_words)

        if len(words) > max_words:
            truncated_content += ' ...'  

        return mark_safe(truncated_content)
