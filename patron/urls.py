from django.conf.urls import patterns, url
from patron import views

urlpatterns = patterns('',
	url(r'^login/$', views.login, name = 'login'),
	url(r'^logout/$', views.logout, name = 'logout'),
	url(r'^suggest_bids/$',views.suggest_bids, name = 'suggest_bids'),
	url(r'^signup/$', views.signup, name  = 'signup'),		
	url(r'^homepage/$', views.homepage, name = 'homepage'),
)
