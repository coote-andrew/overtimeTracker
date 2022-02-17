# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ssl import OP_ENABLE_MIDDLEBOX_COMPAT

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employeeNumber = models.CharField("employee number", max_length=30, blank=True, null=True)
    JOB_CLASSIFICATIONS = (
        (1, "intern"),
        (2, "HMO"),
        (3, "Registrar"),
    )
    classification = models.IntegerField("job classification", choices=JOB_CLASSIFICATIONS, null=True, blank=True)
    department = models.CharField("Department", max_length=50, blank=True, null=True)
    PAY_CYCLE_OPTIONS = (
        (1, "A"),
        (2, "B"),
    )
    payCycle = models.IntegerField("payCycle fortnight option A or B", choices=PAY_CYCLE_OPTIONS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    okToShareRoster = models.BooleanField("Share roster with other users", default=False, help_text="Optional: tick this box to share your roster with other users of this website")
    okToShareOvertime = models.BooleanField("Share overtime with other users", default=False, help_text="Optional: tick this box to share your overtime requests with other users of this website")
    def nearestPayCycle(self):
        if self.payCycle == None:
            return ""
        elif self.payCycle == 1:
            fortnight = datetime.date(2022, 1, 2)
        else:
            fortnight = datetime.date(2022, 1, 9)

        while fortnight < datetime.date.today():
            fortnight += datetime.timedelta(days=14)
        return fortnight
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

    def __str__(self):
        return str(self.user)
        

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class OvertimeRow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField("Date of overtime", null=True)
    CLINICAL_REASONS = (
        (1, "Direct Patient Care or Theatre"),
        (2, "Ward Round or Delayed/Extended handover (note, does not need pt URN)"),
        (3, "Discharge Summaries or Patient Admin"),
        (4, "MDM preparation"),
    )
    reason = models.IntegerField("Reason for overtime", choices=CLINICAL_REASONS, blank=True, null=True)
    patientURN = models.CharField("Patient URN", max_length=20, blank=True, null=True)
    startTime = models.TimeField("Starting time", blank=True, null=True)
    finishTime = models.TimeField("Finish time", blank=True, null=True)
    higherDutiesYN = models.CharField("Higher duties performed (Y/N)", max_length=3, blank=True, null=True)
    preApproval = models.CharField("NUM/Senior Registrar/Consultant Pre-Approval (not-mandatory)", max_length=200, blank=True, null=True)
    personalComment = models.TextField("Personal Comment (won't be printed)", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def last_paycycle(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now
    
    def total_hours(self):
        time_to_show = datetime.datetime.combine(datetime.date.min, self.finishTime) - datetime.datetime.combine(datetime.date.min, self.startTime)
        hours, remainder = divmod(time_to_show.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        string_to_return = ""
        if hours != 0:
            string_to_return += '{:02}h'.format(int(hours))
        if minutes != 0:
            string_to_return += ' {:02}m'.format(int(minutes))
        return string_to_return
    
    def secondsForTotal(self):
        time_to_show = datetime.datetime.combine(datetime.date.min, self.finishTime) - datetime.datetime.combine(datetime.date.min, self.startTime)
        return time_to_show.seconds
    
    def __str__(self):
        return str(self.date.strftime("%d/%m/%Y") or '')+ " " + str(self.get_reason_display() or '') + " " + self.startTime.strftime("%H:%M:%S") + " - " + self.finishTime.strftime("%H:%M:%S")

class PrintOutTimeSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    startDate = models.DateField("starting date", null=True)
    endingDate = models.DateField("ending date", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    linkedOvertimeRows = models.ManyToManyField(OvertimeRow)
    


class Roster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startDateTime = models.DateTimeField("starting date and time", blank=True, null=True)
    endDateTime = models.DateTimeField("ending date and time", blank=True, null=True)
    role = models.CharField("role performed", max_length=300, blank=True, null=True)
    job = models.CharField("job at the time", max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    oncallTF = models.BooleanField("is this role on call?", default=0)
    def __str__(self):
        if self.oncallTF:
            str_oncall = " (on call)"
        else:
            str_oncall = ""
        return self.role + ": " + timezone.localtime(self.startDateTime).strftime("%d/%m/%Y %H:%M") + " - " + timezone.localtime(self.endDateTime).strftime("%H:%M") + str_oncall
    
    @property
    def startDate(self):
        return timezone.localdate(self.startDateTime)
    #  input_formats = [
    #     '%d/%m/%y',
    #     '%d/%m/%Y',
    # ]

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class CalendarFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)