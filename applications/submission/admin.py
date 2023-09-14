from django.contrib import admin

# Register your models here.
from applications.submission.models import Submission

admin.site.register(Submission)