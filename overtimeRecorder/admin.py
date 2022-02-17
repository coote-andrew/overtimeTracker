# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cgi import print_environ

from django.contrib import admin

# Register your models here.
from .models import OvertimeRow, Profile, PrintOutTimeSheet, Roster, CalendarFile
admin.site.register(OvertimeRow)
admin.site.register(Profile)
admin.site.register(PrintOutTimeSheet)
admin.site.register(Roster)
admin.site.register(CalendarFile)