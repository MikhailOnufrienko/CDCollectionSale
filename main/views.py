from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist, RequestContext
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature

from .models import BuyerUser, Artist, Item
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utilities import signer


class RegisterUserView(CreateView):
    model = BuyerUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(BuyerUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class CDLoginView(LoginView):
    template_name = 'main/login.html'
    next_page = 'main:profile'


class CDLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


def index(request):
    return render(request, 'main/index.html')


def band_view(request, pk):
    artist = Artist.objects.get(pk=pk)
    return render(request, 'main/band.html', context={'artist': artist})


def album_view(request, pk):
    album = Item.objects.get(pk=pk)
    return render(request, 'main/item.html', context={'album': album})


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = BuyerUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь успешно удалён.')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = BuyerUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Вы успешно изменили свои данные.'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Вы успешно изменили свой пароль.'


@login_required
def cart(request):
    return render(request, 'main/cart.html')


def other_pages(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
