# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import math
import json
import uuid
import os

from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import OvertimeRow, PrintOutTimeSheet, Roster, CalendarFile
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.views import generic
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .forms import UserForm, ProfileForm, OvertimeRowForm, RosterForm, OvertimeRowFormShortened, CreateNewUserForm, RosterIndForm, OvertimeRowFormSuperShortened, CustomPayCycleForm, DeleteForm
import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.core import serializers
from django.core import files
from django.core.files import File
from django.utils import timezone
from django.core.files.temp import NamedTemporaryFile


def Index(request):
    if request.user.is_authenticated:
        recent_roster = Roster.objects.filter(user = request.user, startDateTime__lte=datetime.datetime.now() + datetime.timedelta(days=1), startDateTime__gte=datetime.datetime.now() - datetime.timedelta(days=14)).order_by('endDateTime')
        recent_overtime = OvertimeRow.objects.filter(user = request.user, date__lte=datetime.date.today(), date__gte=datetime.date.today() - datetime.timedelta(days=14)).order_by('date')
        if recent_overtime.count() >= 1:
            filterOvertime = True
        else:
            filterOvertime = False
        if recent_roster.count() >= 1:
            filterRoster = True
        else:
            filterRoster = False
        recent_roster_and_overtime_View = []
        for i in range(14):
            single_day = []
            dateToTest = datetime.date.today() - datetime.timedelta(days=i)
            single_day.append(dateToTest)
            if filterRoster:
                day_roster = recent_roster.filter(startDateTime__year=dateToTest.year,startDateTime__month=dateToTest.month,startDateTime__day=dateToTest.day)

                if day_roster.count() >= 1:
                    single_day.append(day_roster)
                else:
                    single_day.append("")
            else:
                single_day.append("")
            overtime_array = []
            if filterOvertime:
                day_overtime = recent_overtime.filter(date=dateToTest)
                if day_overtime.count() >= 1:
                    dateOvertimeArray = []
                    for item in range(day_overtime.count()):
                        delete_form = DeleteForm(instance=day_overtime[item], prefix=day_overtime[item].pk)
                        dateOvertimeArray.append([day_overtime[item],delete_form])
                    overtime_array.append(dateOvertimeArray)
                    
                    form = OvertimeRowFormSuperShortened(prefix=dateToTest.strftime("%Y%m%d"), initial={'date':dateToTest})
                else:
                    overtime_array.append("")
                    form =""
            else:
                form=""
      
                
            overtime_array.append(form)
            single_day.append(overtime_array)

            recent_roster_and_overtime_View.append(single_day)
                    
        future_roster = Roster.objects.filter(user = request.user, endDateTime__gte=datetime.datetime.now()).order_by('endDateTime')[:7]
        recent_overtime_sheets = PrintOutTimeSheet.objects.filter(user = request.user).order_by('created_at')[:5]
    
        context = {
            'recent_roster' :recent_roster,
            'future_roster': future_roster,
            'recent_overtime_sheets': recent_overtime_sheets,
            "recent_roster_and_overtime_View":recent_roster_and_overtime_View,
        }
        return render(request, "overtimeRecorder/index.html", context)
    else:
        return render(request, "overtimeRecorder/homepage.html")

@login_required
def UserDetailsView(request, pk):
    return HttpResponse("you're viewing user %s" % pk)


def CreateNewUser(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/logout?next=' + reverse('overtime:createNewUser'))
    else:
        if request.method == 'POST':  
            user_form = CreateNewUserForm(request.POST)
            if user_form.is_valid():  
                obj = user_form.save(commit=False)
                obj.username = obj.email
                obj.save()
                profile_update = ProfileForm(request.POST, instance=obj.profile)
                profile_update.is_valid()
                profile_update.save()
                messages.success(request, 'Account created successfully')  
                return HttpResponseRedirect(reverse('overtime:login')) 
            else:
            
                return HttpResponseRedirect(reverse('overtime:index')) 
        
        else:  
            A_date_array=[]
            B_date_array=[]
            A_counter = datetime.date(2022, 1, 2)
            B_counter = datetime.date(2022, 1, 9)
            while A_counter < datetime.date.today() - datetime.timedelta(days=30):
                A_counter += datetime.timedelta(days=14)
            while B_counter < datetime.date.today() - datetime.timedelta(days=30):
                B_counter += datetime.timedelta(days=14)

            while len(A_date_array) < 5:
                A_date_array.append(A_counter)
                A_counter += datetime.timedelta(days=14)
            while len(B_date_array) < 5:
                B_date_array.append(B_counter)
                B_counter += datetime.timedelta(days=14)

            user_form = CreateNewUserForm()
            profile_form = ProfileForm()
            context = {  
                'user_form': user_form,
                'profile_form': profile_form,
                "A_date_array": A_date_array,
                "B_date_array": B_date_array
            }  
            return render(request, 'overtimeRecorder/register.html', context)  

@login_required
def EditUser(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('overtime:index'))
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)
    A_date_array=[]
    B_date_array=[]
    A_counter = datetime.date(2022, 1, 2)
    B_counter = datetime.date(2022, 1, 9)
    while A_counter < datetime.date.today() - datetime.timedelta(days=30):
        A_counter += datetime.timedelta(days=14)
    while B_counter < datetime.date.today() - datetime.timedelta(days=30):
        B_counter += datetime.timedelta(days=14)

    while len(A_date_array) < 5:
        A_date_array.append(A_counter)
        A_counter += datetime.timedelta(days=14)
    while len(B_date_array) < 5:
        B_date_array.append(B_counter)
        B_counter += datetime.timedelta(days=14)


    return render(request, 'overtimeRecorder/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        "A_date_array": A_date_array,
        "B_date_array": B_date_array
    })
    
@login_required
def detailOvertimeRowView(request, pk):
    row = get_object_or_404(OvertimeRow,pk=pk)
    if request.method == "POST":
        row_form = OvertimeRowForm(request.POST, instance=row)
        if row_form.is_valid():
            row_form.save()
            messages.success(request, "Overtime information successfully updated!")
            return HttpResponseRedirect(reverse('overtime:index'))
        else:
            messages.error(request, ('Please correct the error below.'))
            form = OvertimeRowForm(instance=row)
            return render(request, "overtimeRecorder/detailView.html", {"row":row, "form": form})
    else:
        form = OvertimeRowForm(instance=row)
        return render(request, "overtimeRecorder/detailView.html", {"row":row, "form": form})

@login_required
def printOptions(request):
    if request.method == "POST":
        row_form = CustomPayCycleForm(request.POST)
        if row_form.is_valid():
            rows = OvertimeRow.objects.filter(
                Q(user=request.user),Q(date__lte=row_form.cleaned_data['finishDate']), Q(date__gte=row_form.cleaned_data['startDate'])
            )
            printout = PrintOutTimeSheet(user=request.user, startDate=row_form.cleaned_data['startDate'], endingDate=row_form.cleaned_data['finishDate'] )
            printout.save()
            for row in rows:
                printout.linkedOvertimeRows.add(row)
            return HttpResponseRedirect(reverse('overtime:printView', args=(printout.id,)))
        else:
            messages.error(request, ('Please correct the error below.'))
            form = CustomPayCycleForm(instance=row_form)
            return render(request, "overtimeRecorder/overtimePrintOptions.html", { "form": form})
    else:
        form = CustomPayCycleForm()
        recent_overtime_sheets = PrintOutTimeSheet.objects.filter(user = request.user).order_by('created_at')[:5]
        return render(request, "overtimeRecorder/overtimePrintOptions.html", {
            "form":form,
            "recent_overtime_sheets":recent_overtime_sheets,
        })

@login_required
def createMostRecentPayCyclePrintout(request):
    rows = OvertimeRow.objects.filter(
        Q(user=request.user),Q(date__lte=request.user.profile.nearestPayCycle()), Q(date__gt=request.user.profile.nearestPayCycle()-datetime.timedelta(days=14))
        )
    #Add list above to new Printout
    if rows.count() <1:
        messages.error(request, ('No overtime data during this timeperiod'))
        return HttpResponseRedirect(reverse('overtime:printViewOptions'))
    else:
        printout = PrintOutTimeSheet(user=request.user, startDate=rows.order_by("date")[0].date, endingDate=rows.order_by("-date")[0].date )
        printout.save()
        for row in rows:
            printout.linkedOvertimeRows.add(row)
    return HttpResponseRedirect(reverse('overtime:printView', args=(printout.id,)))

@login_required
def createCustomPayCyclePrintout(request):
    if request.method == "POST":
        row_form = CustomPayCycleForm(request.POST)
        if row_form.is_valid():
            rows = OvertimeRow.objects.filter(
                Q(user=request.user),Q(date__lte=row_form.finishDate), Q(date__gte=row_form.startDate)
            )
            printout = PrintOutTimeSheet(user=request.user, startDate=row_form.startDate, endingDate=row_form.finishDate )
            printout.save()
            for row in rows:
                printout.linkedOvertimeRows.add(row)
            return HttpResponseRedirect(reverse('overtime:printView', args=(row_form.id,)))
        else:
            messages.error(request, ('Please correct the error below.'))
            form = CustomPayCycleForm(instance=row_form)
            return render(request, "overtimeRecorder/overtimePrintOptions.html", { "form": form})
    else:
        customDates = CustomPayCycleForm(request.POST)
        return render(request, "overtimeRecorder/overtimePrintOptions.html", {"form": customDates})
    

@login_required
def printView(request, pk):
    printout = get_object_or_404(PrintOutTimeSheet,pk=pk)
    rows = printout.linkedOvertimeRows.all()
    name = rows[0].user.first_name + " " + rows[0].user.last_name
    e_number = rows[0].user.profile.employeeNumber
    print_date = datetime.date.today()
    department = rows[0].user.profile.department
    classification = rows[0].user.profile.get_classification_display
    pay_fortnight = rows[0].user.profile.nearestPayCycle()
    overtime_printout = []

    total_hours_total = 0
    numberOfPages = int(math.ceil(len(rows)/12))
    for _ in range(numberOfPages):
        overtime_printout_temp = []
        for _ in range(12):
            overtime_printout_temp.append([" "] *10)
        overtime_printout.append(overtime_printout_temp)
    numberRows = len(rows)
    z = 0
    for y in range(numberOfPages):
        for x in range(0, min(numberRows - y*12, 12)):
            overtime_printout[y][x][0] = rows[z].date

            overtime_printout[y][x][1] = rows[z].date.strftime("%a")
            # ABOVE NEEDS FIXING---------------------------------
            overtime_printout[y][x][2] = rows[z].reason
            if rows[x].patientURN == None:
                    overtime_printout[y][x][3] = ""
            else:
                overtime_printout[y][x][3] = rows[z].patientURN
            overtime_printout[y][x][4] = rows[z].startTime
            overtime_printout[y][x][5] = rows[z].finishTime
            if rows[x].higherDutiesYN == None:
                overtime_printout[y][x][6] = "N"
            else:
                overtime_printout[y][x][6] = rows[z].higherDutiesYN
            overtime_printout[y][x][7] = rows[z].total_hours
            total_hours_total += rows[z].secondsForTotal()
            #ABOVE NEEDS FIXING------------------------------------
            if rows[x].preApproval == None:
                overtime_printout[y][x][8] = ""
            else:
                overtime_printout[y][x][8] = rows[z].preApproval
            z+= 1
    
    


    hours, remainder = divmod(total_hours_total, 3600)
    minutes, seconds = divmod(remainder, 60)
    stringFortnightlyTotal = ""
    if hours != 0:
        stringFortnightlyTotal += '{:02}h'.format(int(hours))
    if minutes != 0:
        stringFortnightlyTotal += ' {:02}m'.format(int(minutes))


    return render(request, "overtimeRecorder/printout.html", {
        "overtime_printout": overtime_printout,
        "name":name,
        "Number": e_number, 
        "date": print_date,
        "Department": department,
        "Classification": classification,
        "PayFortnight":pay_fortnight,
        "stringFortnightlyTotal":stringFortnightlyTotal,
        "numberOfPages":numberOfPages,
        })

@login_required
def changeDetails(request, pk):
    row = get_object_or_404(OvertimeRow,pk=pk)
    row.patientURN = request.POST["patientURN"]
    row.save()
    return HttpResponseRedirect(reverse('overtime:requestRow', args=(row.id,)))

@login_required
def inputRoster(request):
    if request.method == "POST":
        form = RosterForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['rosterField']
            lines = content.split("\n")
            # process the form data
            # Set up variables
            minDate = datetime.date(2100, 1, 1)
            maxDate = datetime.date(1900, 1, 1)
            RePattern2 = "^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)+ (.*)\/(.*)\/(.*) - (.*)"
            RePatternTimes = "^(Oncall \()*(\d+):(\d+) - (\d+):(\d+)"
            startLine = 0
            saveThisItem = True
            startDatetime = False
            arrayToSave = []
            for line in range(len(lines)):
                match = re.search(RePattern2, lines[line])
                if lines[line] == "Roster" or lines[line] == "":
                    continue
                elif match:
                    # save the previous one
                    if startDatetime and saveThisItem:

                        arrayToSave.append([startDatetime, endDatetime,jobToSave, roleToSave, onCall])
                        
                        
                    
                    startLine = line
                    RosterDate = datetime.date(int(match.group(4)), int(match.group(3)), int(match.group(2)))
                    saveThisItem = True
                    # Set min and max dates
                    if RosterDate < minDate:
                        minDate = RosterDate
                    elif RosterDate > maxDate:
                        maxDate = RosterDate
                else:
                    if line - startLine == 1:
                        times = re.search(RePatternTimes, lines[line])
                        if times:
                            onCall = times.group(1) is not None

                            startTime = datetime.time(int(times.group(2)), int(times.group(3)))
                            endTime = datetime.time(int(times.group(4)), int(times.group(5)))
                            if endTime < startTime:
                                startDatetime = timezone.make_aware(datetime.datetime.combine(RosterDate, startTime))
                                endDatetime = timezone.make_aware(datetime.datetime.combine(RosterDate + datetime.timedelta(1), endTime))
                            else:
                                startDatetime = timezone.make_aware(datetime.datetime.combine(RosterDate, startTime))
                                endDatetime = timezone.make_aware(datetime.datetime.combine(RosterDate, endTime))
                        else:
                            saveThisItem = False
                    if line - startLine == 3:
                        jobToSave = lines[line]
                    if line - startLine == 5:
                        roleToSave = lines[line]
            if startDatetime and saveThisItem:

                        arrayToSave.append([startDatetime, endDatetime,jobToSave, roleToSave, onCall])

            
            # Delete between dates
            if request.user:
                rowsToDelete = Roster.objects.filter(Q(user=request.user))
                for row in rowsToDelete:
                    if row.startDate >= minDate and row.startDate <=maxDate:
                        row.delete()
            
            for row in arrayToSave:
                rosterToSave = Roster(user=request.user, startDateTime=row[0], endDateTime=row[1], job=row[2].strip(), role=row[3].strip(), oncallTF=row[4])

                rosterToSave.save()

            return HttpResponseRedirect(reverse('overtime:index'))
    if request.method == "GET":
        form = RosterForm()
        return render(request, "overtimeRecorder/roster.html", {
            "rosterForm": form
        })

@login_required
def inputOvertime(request, date=datetime.date.today().strftime("%d/%m/%Y"), time=datetime.datetime.now().strftime("%H:%M"), AfterNotBefore=True):
    if request.method=="POST":
        row_form = OvertimeRowFormShortened(request.POST)
        if row_form.is_valid():


            obj = row_form.save(commit=False)
            obj.user=request.user
            obj.save()
            messages.success(request, "Overtime information successfully updated!")
            return HttpResponseRedirect(reverse('overtime:index'))
        else:
            messages.error(request, ('Please correct the error below.'))
            form = OvertimeRowFormShortened(request.POST)
            return render(request, "overtimeRecorder/inputovertime.html", {"overtimeForm": form})
    else:
        if AfterNotBefore:
            stime = time
            etime = ""
        else:
            stime = ""
            etime = time
        form = OvertimeRowFormShortened(initial={'date':date.replace("-","/"), "startTime":stime, "finishTime":etime})
        return render(request, "overtimeRecorder/inputovertime.html", {"overtimeForm": form, "bOra":AfterNotBefore})

@login_required
def inputOvertimeJustDate(request, date):
    if request.method=="POST":
        row_form = OvertimeRowFormShortened(request.POST)
        if row_form.is_valid():

            obj = row_form.save(commit=False)
            obj.user=request.user
            obj.save()
            messages.success(request, "Overtime information successfully updated!")
            return HttpResponseRedirect(reverse('overtime:index'))
        else:
            messages.error(request, ('Please correct the error below.'))
            form = OvertimeRowFormShortened(request.POST)
            return render(request, "overtimeRecorder/inputovertime.html", {"overtimeForm": form})
    else:
        form = OvertimeRowFormShortened(initial={'date':date.replace("-","/")})
        return render(request, "overtimeRecorder/inputovertime.html", {"overtimeForm": form, "bOra":True})


@login_required
def editIndividualRosterItem(request, pk):
    roster = get_object_or_404(Roster,pk=pk)
    if request.method=="POST":
        if roster.user != request.user:
            return HttpResponseRedirect(reverse('overtime:index'))
        else:
            rosterIndForm = RosterIndForm(request.POST, instance=roster)
            if rosterIndForm.is_valid():
                rosterIndForm.save()
            return HttpResponseRedirect(reverse('overtime:index'))
            
    else:
        if roster.user != request.user:
            return HttpResponseRedirect(reverse('overtime:index'))
        else:
            rosterIndForm = RosterIndForm(instance=roster)
            return render(request,"overtimeRecorder/specificRosterEdit.html", {"rosterIndForm":rosterIndForm})


@login_required
def submitAjaxOvertimeForm(request):
    if request.method =="POST":
        json_data_wrapper = json.loads(request.body)
        json_data= json_data_wrapper['post_data']


        dateForForm=datetime.datetime.strptime(json_data[5][1], "%Y-%m-%d").date()
        rosterObj = Roster.objects.filter(startDateTime__year=dateForForm.year,startDateTime__month=dateForForm.month, startDateTime__day=dateForForm.day )
        instance = []
        if rosterObj.count() ==1:
            if json_data[3][1]:
                obj = OvertimeRow(user=request.user, date=dateForForm, reason=json_data[1][1], patientURN=json_data[2][1], startTime=json_data[3][1], finishTime=timezone.localtime(rosterObj[0].startDateTime))
                obj.save()
                instance.append(obj.pk)
            if json_data[4][1]:
                obj = OvertimeRow(user=request.user, date=dateForForm, reason=json_data[1][1], patientURN=json_data[2][1], startTime=timezone.localtime(rosterObj[0].endDateTime), finishTime=json_data[4][1])
                obj.save()
                instance.append(obj.pk)
        if rosterObj.count() >1:
            if json_data[3][1]:
                obj = OvertimeRow(user=request.user, date=dateForForm, reason=json_data[1][1], patientURN=json_data[2][1], startTime=json_data[3][1], finishTime=timezone.localtime(rosterObj[0].startDateTime))
                obj.save()
                instance.append(obj.pk)
            if json_data[4][1]:
                obj = OvertimeRow(user=request.user, date=dateForForm, reason=json_data[1][1], patientURN=json_data[2][1], startTime=timezone.localtime(rosterObj[0].endDateTime), finishTime=json_data[4][1])
                obj.save()
                instance.append(obj.pk)
        json_array = []
        recent_overtime =OvertimeRow.objects.filter(id__in=instance)
        for row in recent_overtime:
            json_array.append({'date':row.date.strftime("%Y%m%d"),'startTime':row.startTime.strftime("%I:%M %p"),'finishTime':row.finishTime.strftime("%I:%M %p"), 'reason':row.get_reason_display(), 'patientURN':row.patientURN})
        converted = json.dumps(json_array)
        return JsonResponse(converted, safe=False)
    else:
        return HttpResponseRedirect(reverse('overtime:index'))

@login_required
def submitAjaxOvertimeFormDelete(request):
    if request.method =="POST":
        json_data_wrapper = json.loads(request.body)
        json_data= json_data_wrapper['post_data']
        pkForDelete = json_data[1][0].replace("-date","")
        row_to_delete = OvertimeRow.objects.get(pk=pkForDelete)
        if row_to_delete.user == request.user:
            id_to_delete = row_to_delete.id
            row_to_delete.delete()
            json_array = {"id":id_to_delete}
            converted = json.dumps(json_array)
        else:
            converted = False
        return JsonResponse(converted, safe=False)
    else:
        return HttpResponseRedirect(reverse('overtime:index'))


@login_required
def createCalendar(request):
    if request.method=="POST":
        itemsToPutInCalendar = Roster.objects.filter(user = request.user, endDateTime__gte=datetime.datetime.now()).order_by('endDateTime')[:7]
        textForCalendarFunction = []
        for item in itemsToPutInCalendar:
            textForCalendarFunction.append([item.job, item.startDateTime, item.endDateTime, "This event was created using the overtime tracker website"])
        calendarText = createCalendarText(textForCalendarFunction)
        calendar_temp_file = NamedTemporaryFile()
        calendar_temp_file.write(calendarText.encode())
        file_name = re.sub(r'[^\w\d-]','_',str(request.user)) + ".ics"
        calendar_temp_file.flush()
        temp_file = files.File(calendar_temp_file, name=file_name)

        calendar = CalendarFile(user=request.user, file=temp_file)
        calendar.save()
        return_text = calendar.file.url
    else:
        return_text = "failed"



    return JsonResponse(json.dumps(return_text), safe=False)




def createCalendarText(list_of_data):
    # for each item you should do in following order
    # Summary
    # START DATETIME
    # END DATETIME
    # Description
    calendar_start_text = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AndrewC Overtime//Calendar 1.0//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH"""
    calendar_content=[]
    for item in list_of_data:
        build_up_item = "BEGIN:VEVENT\n"
        build_up_item+= "SUMMARY:" + str(item[0]) + "\n"
        build_up_item+= "UID:" + str(uuid.uuid4()) + "\n"
        build_up_item+= "SEQUENCE:0\n"
        build_up_item+= "STATUS:CONFIRMED\nTRANSP:OPAQUE\n"
        build_up_item+= "DTSTART:" + item[1].strftime("%Y%m%dT%H%M%SZ") + "\n"
        build_up_item+= "DTEND:" +item[2].strftime("%Y%m%dT%H%M%SZ") + "\n"
        build_up_item+= "DTSTAMP:" + datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")+ "\n"
        build_up_item+= "LOCATIONS:Melbourne Health\n"
        build_up_item+= "DESCRIPTION:" + item[3] + "\n"
        build_up_item+= "END:VEVENT"
        calendar_content.append(build_up_item)
    calendar_end_text = "\nEND:VCALENDAR"

    calendar_text = calendar_start_text + "\n" + "\n".join(calendar_content) + calendar_end_text
    return calendar_text