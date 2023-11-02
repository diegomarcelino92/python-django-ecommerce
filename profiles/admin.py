
from django.contrib import admin

from profiles.models import Profile, ProfileAddress


class ProfileAddressInline(admin.TabularInline):
    model = ProfileAddress
    extra = 0


@admin.register(ProfileAddress)
class ProfileAddressAdmin(admin.ModelAdmin):
    model = ProfileAddress
    list_display = ('profile', 'number', 'neighborhood', 'code', 'city', 'state')
    search_fields = ('profile', 'number', 'neighborhood', 'code', 'city', 'state')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('email', 'phone')
    search_fields = ('email', 'phone')
    inlines = [ProfileAddressInline]
