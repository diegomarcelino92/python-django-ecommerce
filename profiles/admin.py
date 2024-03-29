
from django.contrib import admin

from profiles.models import Profile, ProfileAddress


@admin.register(ProfileAddress)
class ProfileAddressAdmin(admin.ModelAdmin):
    model = ProfileAddress
    list_display = ('profile', 'number', 'neighborhood', 'code', 'city', 'state')
    search_fields = ('profile', 'number', 'neighborhood', 'code', 'city', 'state')


class ProfileAddressInline(admin.TabularInline):
    model = ProfileAddress
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'phone')
    search_fields = ('user', 'phone')
    inlines = [ProfileAddressInline]
