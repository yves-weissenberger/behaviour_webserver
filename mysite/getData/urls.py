from django.conf.urls import url,  patterns, include
from django.contrib import admin

from . import views


admin.autodiscover()


urlpatterns = [
	url(r'^$',views.boxes,name='boxes'),
	url(r'^(?P<box_nr>[0-9]+)/$',views.box_info,name='box_info'),
	url(r'^(?P<box_nr>[0-9]+)/get_box_data/$',views.get_box_data,name='get_box_data'),
	url(r'^(?P<box_nr>[0-9]+)/set_mouse_ID/$', views.set_mouse_ID, name='set_mouse_ID'),
	url(r'^(?P<box_nr>[0-9]+)/write_mouse_ID/$', views.write_mouse_ID, name='write_mouse_ID'),
	url(r'^(?P<box_nr>[0-9]+)/set_mouse_task/$', views.set_mouse_task, name='set_mouse_task'),
	url(r'^(?P<box_nr>[0-9]+)/write_mouse_task/$', views.write_mouse_task, name='write_mouse_task'),
	url(r'^(?P<box_nr>[0-9]+)/get_PiData/$', views.get_PiData, name='get_PiData'),
	url(r'^(?P<box_nr>[0-9]+)/write_PiData/$', views.write_PiData, name='write_PiData'),
	url(r'^set_num_boxes/$', views.set_num_boxes, name='set_num_boxes'),
	url(r'^write_num_boxes/$', views.write_num_boxes, name='write_num_boxes'),
	url(r'^download_data/$', views.download_data, name='download_data'),
	url(r'^download_data/(?P<mouse_ID>[^/]{0,20})/$', views.list_mousewise, name='list_mousewise'),
	url(r'^download_data/(?P<mouse_ID>[^/]{0,20})/(?P<fileName>.*)/$', views.download_mousewise, name='download_mousewise'),

	url(r'^(?P<box_nr>[0-9]+)/(?P<isOnline>True|False|0|1)/upload_new_task/$', views.upload_new_task, name='upload_new_task'),

]
