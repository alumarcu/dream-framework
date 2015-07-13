from django.conf.urls import patterns, url
from dream.engine.soccer.views import DebugView

urlpatterns = patterns(
    '',
    url(r'^debug/simulator/$', DebugView.as_view())
)
