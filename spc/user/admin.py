from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class MyUserAdmin(UserAdmin):
    list_display = ['username',
                    'email',
                    'first_name',
                    'last_name',
                    'is_active',
                    'is_staff',
                    ]

class ConcernAdmin(admin.ModelAdmin):
    list_display = ['userID',
                    'subject',
                    'email',
                    'fullName',
                    'dateTime',
                    'status',
                    ]

    list_display_links = ['userID',
                        'subject',
                        'email',
                        'fullName',
                        'dateTime',
                        ]

    list_editable = ['status',]

    list_filter = ['status',
                'dateTime',
                ]

    search_fields = ['userID',
                    'subject',
                    'email',
                    'fullName',
                    ]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'phoneNumber',
                    'gender',
                    'address',
                    'status',
                    ]

    list_display_links = ['user',
                        'phoneNumber',
                        'gender',
                        'address',
                        ]

    list_editable = ['status',]

    list_filter = ['status',
                'gender',
                ]

    search_fields = ['user',
                    'phoneNumber',
                    'gender',
                    'address',
                    ]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Concern, ConcernAdmin)