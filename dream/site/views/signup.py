from django.views.generic import View
from django.shortcuts import render
from dream.site.forms import SignupForm
from dream.site.services import SignupService


class SignupView(View):

    TEMPLATE_PATH = 'signup.html'

    def get(self, request):
        form = SignupForm()

        context = {'signup_form': form}

        return render(request, self.TEMPLATE_PATH, context)

    def post(self, request):
        payload = request.POST
        form = SignupForm(payload)

        if form.is_valid():
            service = SignupService()
            service.create_account(service.process(payload))

        context = {'signup_form': form}

        return render(request, self.TEMPLATE_PATH, context)
