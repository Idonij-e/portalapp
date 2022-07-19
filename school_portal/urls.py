from django.urls import path
from . import views, AdminViews
from portal_system import settings

urlpatterns = [
    path('login_to_dashboard', views.showLogin, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
    path('admin_home',AdminViews.admin_home,name="admin_home"),
    path('add_staff',AdminViews.add_staff,name="add_staff"),
    path('add_staff_save',AdminViews.add_staff_save,name="add_staff_save"),
    path('add_course/', AdminViews.add_course,name="add_course"),
    path('add_course_save', AdminViews.add_course_save,name="add_course_save"),
    path('add_student', AdminViews.add_student,name="add_student"),
    path('add_student_save', AdminViews.add_student_save,name="add_student_save"),
    path('add_subject', AdminViews.add_subject,name="add_subject"),
    path('add_subject_save', AdminViews.add_subject_save,name="add_subject_save"),
    path('manage_staff', AdminViews.manage_staff,name="manage_staff"),
    path('manage_student', AdminViews.manage_student,name="manage_student"),
    path('manage_course', AdminViews.manage_course,name="manage_course"),
    path('manage_subject', AdminViews.manage_subject,name="manage_subject"),
    path('edit_staff/<str:staff_id>', AdminViews.edit_staff,name="edit_staff"),
    path('edit_staff_save', AdminViews.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<str:student_id>', AdminViews.edit_student,name="edit_student"),
    path('edit_student_save', AdminViews.edit_student_save,name="edit_student_save"),
    path('edit_subject/<str:subject_id>', AdminViews.edit_subject,name="edit_subject"),
    path('edit_subject_save', AdminViews.edit_subject_save,name="edit_subject_save"),
    path('edit_course/<str:course_id>', AdminViews.edit_course,name="edit_course"),
    path('edit_course_save', AdminViews.edit_course_save,name="edit_course_save"),
    path('manage_session', AdminViews.manage_session,name="manage_session"),
    path('add_session_save', AdminViews.add_session_save,name="add_session_save"),
    #path('check_email_exist', HodViews.check_email_exist,name="check_email_exist"),
    #path('check_username_exist', HodViews.check_username_exist,name="check_username_exist"),
    
    path('admin_profile', AdminViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save,name="admin_profile_save"),
    path('admin_send_notification_staff', AdminViews.admin_send_notification_staff,name="admin_send_notification_staff"),
    path('admin_send_notification_student', AdminViews.admin_send_notification_student,name="admin_send_notification_student"),
    #path('send_student_notification', AdminViews.send_student_notification,name="send_student_notification"),
    #path('send_staff_notification', AdminViews.send_staff_notification,name="send_staff_notification"),

]