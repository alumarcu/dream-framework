from django.conf.urls import patterns, url
from dream.engine.soccer.views import DebugView

urlpatterns = patterns('',
    url(r'^debug/match/(?P<match_id>[0-9]+)/$', DebugView.as_view())
)