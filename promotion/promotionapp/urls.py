from promotionapp import views
from django.urls import path, re_path

urlpatterns = [    
    path('', views.loginpage, name='home'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('promotions/', views.promotions, name='promotions'),
    path('authentication/', views.authentication, name='authentication'),
    path('promoterregistration/', views.promoterregistration, name='promoterregistration'),
    path('list_of_admins/', views.list_of_admins, name='list_of_admins'),
    path('list_of_promoters/', views.list_of_promoters, name='list_of_promoters'),
    path('end_user/', views.end_user, name='end_user'),
    path('list_of_users/', views.list_of_users, name='list_of_users'),
    path('approve_promoters/', views.approve_promoters, name='approve_promoters'),
    path('reject_promoters/', views.reject_promoters, name='reject_promoters'),
    path('update_promoters/<int:promoter_id>', views.update_promoters, name='update_promoters'),
    path('update_promoters_sql/<int:promoter_id>', views.update_promoters_sql, name='update_promoters_sql'),
    path('delete_promoter/<int:promoter_id>', views.delete_promoter, name='delete_promoter'),
    path('logoutpage/', views.logoutpage, name='logoutpage'),
    path('savepromotions/', views.savepromotions, name='savepromotions'),
    path('campaign/', views.campaign, name='campaign'),
    path('list_of_promotions/', views.list_of_promotions, name='list_of_promotions'),
    path('list_of_promotions_completed/', views.list_of_promotions_completed, name='list_of_promotions_completed'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('target_filters/', views.target_filters, name='target_filters'),
    path('editpromotions/<int:promoter_id>/', views.editpromotions, name='editpromotions'),
    path('after_promoter_login/', views.after_promoter_login, name='after_promoter_login'),


]