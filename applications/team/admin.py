from django.contrib import admin

# Register your models here.
from applications.team.models import Team

admin.site.register(Team)