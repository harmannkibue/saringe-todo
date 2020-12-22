from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from pilkit.processors import ResizeToFill
from mylib.custom_fields import CustomPhoneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from oauth2_provider.models import Application, AccessToken
from oauthlib.common import generate_token
from datetime import timedelta
from saringe_todo.settings import SITE_URL
from mylib.customs import email_send
from mylib.images import scramble
from imagekit.models import ProcessedImageField


class User(AbstractUser):
    ROLES = (('A', 'Admin'),
             ('N', 'Normal'),
             )
    role = models.CharField(max_length=3, choices=ROLES, default='N', null=False, blank=False)
    profile_photo = ProcessedImageField(null=True, blank=True,
                                        upload_to=scramble,
                                        processors=[ResizeToFill(100, 50)],
                                        format='JPEG',
                                        options={'quality': 100})
    reset_code = models.IntegerField(null=True, blank=True)
    phone_number = CustomPhoneField(unique=True)
    time_code_created = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        unique_together = ('username', 'phone_number')

    def __str__(self):
        return self.username


@receiver(post_save, sender=User, dispatch_uid="my_unique_identifier")
def my_handler(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]
    if created:
        # print("The instance is", instance)
        user = instance
        token = generate_token()
        app = Application.objects.first()
        AccessToken.objects.create(user=user,
                                   application=app, expires=now() + timedelta(days=1),
                                   token=token)
        link = "%s/api/v1/users/verify-account?token=%s" % (SITE_URL, token)
        data = {"name": user.first_name, "verify_url": link}
        try:
            email_send("saringe Todo Account Verification", "new_user.html", data, [user.email])
        except Exception as e:
            print("Here in the except of email verification signal", e)
            pass

