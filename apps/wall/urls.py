from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^wall$', views.wall),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^process_post$', views.process_post),
    url(r'^(?P<id>\d+)/comment$', views.comment_view),
    url(r'^(?P<id>\d+)/comment/process_comment$', views.process_comment),
    url(r'^(?P<post_id>\d+)/comment/(?P<comment_id>\d+)/delete$', views.delete_comment)
]
