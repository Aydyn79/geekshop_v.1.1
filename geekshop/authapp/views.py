from django.contrib import messages, auth
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView


from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, UserProfileEditForm
from authapp.models import ShopUser
from basketapp.models import Basket
from mainapp.mixin import BaseClassContextMixin, UserDispatchMixin

from authapp.forms import UserProfileEditForm


class LoginListView(LoginView,BaseClassContextMixin):
    template_name = 'authapp/login.html'
    form_class = ShopUserLoginForm
    title = 'GeekShop - Авторизация'

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return HttpResponseRedirect(reverse('main'))
    #     return HttpResponseRedirect(reverse('authapp:login'))

class RegisterListView(FormView,BaseClassContextMixin):
    model = ShopUser
    template_name = 'authapp/register.html'
    form_class = ShopUserRegisterForm
    title = 'GeekShop - Регистрация'
    success_url = reverse_lazy('auth:login')

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse('auth:verify',args=[user.email,user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email],fail_silently=True)

    @staticmethod
    def verify(self,email,activate_key):
        try:
            user = ShopUser.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expired():
                user.activation_key =''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self,user)
            return render(self,'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('main'))




class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    template_name = 'authapp/profile.html'
    form_class = ShopUserEditForm
    success_url = reverse_lazy('auth:profile')
    title = 'GeekShop - Профиль'

    def post(self, request, *args, **kwargs):
        form = ShopUserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return redirect(self.success_url)

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, "Вы успешно зарегистрировались")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, *args, **kwargs):
        return get_object_or_404(ShopUser, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context

class Logout(LogoutView):
    template_name = "mainapp/index.html"


'''
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm, ShopUserLoginForm

def login(request):
    print(request.POST)
    login_form = ShopUserLoginForm(data=request.POST)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request,user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))
    content = {
        'title': 'вход',
        'login_form':login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', content)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:products'))

def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return  HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    content = {
        'title': 'регистрация',
        'form': register_form
    }
    return render(request, 'authapp/register.html', content)

def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
    content = {
        'title': 'Редактирование',
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', content)
'''