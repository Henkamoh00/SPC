from django.contrib import admin
from .models import *

# Register your models here.

class PostImageAdmin(admin.StackedInline):
    model = PostImage
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]
        
    list_display = ['title',
                    'content',
                    'dateTime',
                    'status',
                    ]

    list_display_links = ['title',
                        'content',
                        'dateTime',
                        ] 

    list_editable = ['status',]

    list_filter = ['status',
                'dateTime',
                ]

    search_fields = ['title',
                    'content',
                    ]



class CommentAdmin(admin.ModelAdmin):
    list_display = ['userID',
                    'postID',
                    'comment',
                    'updated',
                    'dateTime',
                    'status',
                    ]

    list_display_links = ['userID',
                        'postID',
                        'comment',
                        'dateTime',
                        ]

    list_editable = ['updated',
                    'status',]

    list_filter = ['status',
                    'updated',
                    'dateTime',
                    'userID',
                    'postID',
                    ]

    search_fields = ['userID',
                        'postID',
                        'comment',
                        ]



admin.site.register(Post, PostAdmin)
# admin.site.register(PostImage)
admin.site.register(Comment, CommentAdmin)