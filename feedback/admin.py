import django.contrib.admin

import feedback.models


class AttachmentsInline(django.contrib.admin.TabularInline):
    model = feedback.models.Attachment


@django.contrib.admin.register(feedback.models.FeedBack)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.FeedBack.text.field.name,
        feedback.models.FeedBack.created_on.field.name,
    )
    readonly_fields = (
        feedback.models.FeedBack.created_on.field.name,
    )
    inlines = (
        AttachmentsInline,
    )
