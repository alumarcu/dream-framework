from django.conf.urls import patterns, url
from dream.engine.soccer.views import SimulatorView

urlpatterns = patterns(
    '',
    url(r'^dev/simulator/$', SimulatorView.as_view(), name='dev-simulator'),
    url(r'^dev/simulator/api/$', SimulatorView.as_view(), name='dev-simulator-api')
)
