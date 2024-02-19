import copy
from urllib import request

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.views import View

from profiles.forms import ProfileAddressForm, ProfileForm, UserForm
from profiles.models import Profile, ProfileAddress

User = get_user_model()


class ProfileCreate(View):
    template_name = 'profile_create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        user_form = None
        profile_form = None
        profile_address_form = None
        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        if self.request.user.is_authenticated:
            user = self.request.user
            profile = Profile.objects.filter(user=user).first()
            profile_address = ProfileAddress.objects.filter(profile=profile).first()

            user_form = UserForm(
                data=self.request.POST or None,
                user=self.request.user,
                instance=self.request.user)

            profile_form = ProfileForm(data=self.request.POST or None, instance=profile)
            profile_address_form = ProfileAddressForm(data=self.request.POST or None, instance=profile_address)
        else:
            user_form = UserForm(data=self.request.POST or None)
            profile_form = ProfileForm(data=self.request.POST or None)
            profile_address_form = ProfileAddressForm(data=self.request.POST or None)

        self.user_form = user_form
        self.profile_form = profile_form
        self.profile_address_form = profile_address_form
        self.context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile_address_form': profile_address_form
        }

        self.view = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.view

    def post(self, *args, **kwargs):
        user_form = self.user_form
        profile_form = self.profile_form
        profile_address_form = self.profile_address_form

        user = self.request.user
        data = user_form.cleaned_data
        password = data.get('password')

        if user_form.is_valid() and profile_form.is_valid() and profile_address_form.is_valid():
            if self.request.user.is_authenticated:
                user = User.objects.get(username=self.request.user.username)

                if password:
                    user.set_password(password)
                data.pop('password')

                user.__dict__.update(data)

                profile = Profile.objects.filter(user=user).first()
                profile.user = user

                profile_address = ProfileAddress.objects.filter(profile=profile).first()
                if not profile_address:
                    profile_address = profile_address_form.save(commit=False)
                profile_address.profile = profile

                user.save()
                profile.save()
                profile_address.save()
                messages.success(request, 'Cadastro atualizado com sucesso')

            else:
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data.get('password'))

                profile = profile_form.save(commit=False)
                profile.user = user

                profile_address = profile_address_form.save(commit=False)
                profile_address.profile = profile

                user.save()
                profile.save()
                profile_address.save()
                messages.success(self.request, 'Cadastro criado com sucesso')

        if password:
            auth = authenticate(self.request, username=user, password=password)

            if auth:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()
        messages.success(self.request, 'Cadastro criado com sucesso')
        redirect('profiles:create')
        return self.view


class ProfileLogin(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request, 'Usuário ou senha inválidos')
            return redirect('profiles:create')

        user = authenticate(self.request, username=username, password=password)

        if user:
            messages.success(self.request, 'Você fez login com sucesso')
            login(self.request, user=user)
            return redirect('products:list')
        else:
            messages.error(self.request, 'Usuário ou senha inválidos')
            return redirect('profiles:create')


class ProfileLogout(View):
    def get(self, *args, **kwargs):
        logout(request=self.request)
        return redirect('products:list')
