from django.contrib import admin

from .models import Post, PostAttachment

admin.site.register(Post)
# admin.site.register(PostAttachment)
# from django import forms


# class PostForm(forms.ModelForm):
#     def __init__(self, *arg, **kwargs):
#         super(PostForm, self).__init__(*args, **kwargs)
#         self.fields['body'].help_text = 'New Help Text'

#     class Meta:
#         model Post

    

# TEXT = 'Text that we can include '

# #to choose what fields will be displayed in admin site (e.g. add posts)
# class PostAdmin(admin.ModelAdmin):
#     fields = ['body', 'attachments', 'created_by']


#Fieldsets with sectioning
# class PostAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Secion 1', {
#             'fields': ('body', 'attachments'),
#             'description': '%s' % TEXT,
#         }),
#         ('Secion 2', {
#             'fields': ('created_by', 'is_private'),
#             'classes': ('collapse',),
#         }),
#     )

# admin.site.register(Post, PostAttachment)


