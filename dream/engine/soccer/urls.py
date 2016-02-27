from django.conf.urls import patterns, url
from dream.engine.soccer.views import *

urlpatterns = patterns(
    '',
    url(r'^dev/simulator/$', SimulatorView.as_view(), name='dev-simulator'),
    url(r'^dev/simulator/api/$', SimulatorView.as_view(), name='dev-simulator-api'),
    url(r'^dev/team-creator/$', TeamCreatorView.as_view(), name='dev-team-creator'),
    url(r'^dev/team-creator/api/$', TeamCreatorView.as_view(), name='dev-team-creator-api')
)
