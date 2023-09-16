from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import UserRegisterForm


class CreateUser(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
