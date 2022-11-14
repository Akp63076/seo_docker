from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<user>/<filename>
    return 'uploads/user_{0}/{1}'.format(instance.email, filename)

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class upload(models.Model):
    STATUS_CHOICES = [
    ('In Queue', 'In Queue'),
    ('In Progress', 'In Progress'),
    ('Complete', 'Complete'),
    ('Email Sent','Email Sent')
]
    email = models.EmailField()
    file_name=models.CharField(max_length=252)
    file = models.FileField(upload_to=user_directory_path,validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user))
    status=models.CharField(max_length=15,choices=STATUS_CHOICES,default="In Queue")
    time_created=models.DateTimeField()
    time_complete=models.DateTimeField(null=True)
    total=models.IntegerField(null=True)
    current=models.IntegerField(null=True)
    result=models.FileField(null=True)
    result_mod=models.FileField(null=True)
    # file_name=file_name_fun
    def __str__(self):
        return self.file_name