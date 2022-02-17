from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name="overtime"
urlpatterns = [
    #extension /tracker
    path('', views.Index, name='index'),
    path("user/<int:pk>/", views.UserDetailsView, name="userDetails"),
    path("newuser/", views.CreateNewUser, name="createNewUser"),
    path("updateuser/", views.EditUser, name="updateUser"),
    path("request/<int:pk>/", views.detailOvertimeRowView, name="requestRow"),
    path("print/", views.printOptions, name="printViewOptions"),
    path("print/<int:pk>/", views.printView, name="printView"),
    path("runprint/this_paycycle/", views.createMostRecentPayCyclePrintout, name="create_this_paycycle"),
    path("runprint/custom/", views.createCustomPayCyclePrintout, name="create_custom_paycycle"),
    path("changeDetails/<int:pk>/", views.changeDetails, name="changeDetails"),
    path("print/<int:pk>/", views.printView, name="printView"),
    path("roster/", views.inputRoster, name="rosterInput"),
    path("roster/<int:pk>", views.editIndividualRosterItem, name="editRosterItem"),
    path("inptovertime/", views.inputOvertime, name="overtimeReq"),
    path("inptovertime/<date>/", views.inputOvertimeJustDate, name="overtimeReqWDate"),
    path("inptovertime/<date>/<time>/", views.inputOvertime, name="overtimeReqWDateAndTime"),
    path("inptovertime/<date>/<time>/<int:AfterNotBefore>", views.inputOvertime, name="overtimeReqWDateAndTime"),
    path("accounts/", include('django.contrib.auth.urls')),
    path("post/ajax/overtime/", views.submitAjaxOvertimeForm, name="ajaxOvertime"),
    path("post/ajax/overtimeDelete/", views.submitAjaxOvertimeFormDelete, name="ajaxOvertimeDelete"),
    path("post/ajax/createCalendar", views.createCalendar, name="createCalendar"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


