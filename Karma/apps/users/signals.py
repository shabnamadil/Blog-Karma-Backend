from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.files.storage import default_storage

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def notify_super_user(sender, instance, created, *args, **kwargs):
    if created:
        super_users = User.objects.filter(
            is_active=True, is_superuser=True
        )
        current_site = Site.objects.get_current()
        for super_user in super_users:
            subject = 'New User Registration on CyberSocOps!!!'
            message = render_to_string('account_register.html', {
                'super_user': super_user,
                'domain': current_site.domain,
                'new_user' : instance
            })
            super_user.email_user(subject, message)

@receiver(pre_save, sender=Profile)
def delete_old_profile_image(sender, instance, **kwargs):
    if not instance.pk:
        pass
    try:
        old_instance = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return
    old_image = old_instance.image
    if old_image and old_image != instance.image:
        default_storage.delete(old_image.name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.user_profile.save()