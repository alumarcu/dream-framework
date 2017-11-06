from django.conf.urls import url
from dream.site.views import SignupView

urlpatterns = [
    url(r'^signup/', SignupView.as_view(), name='signup')
]
