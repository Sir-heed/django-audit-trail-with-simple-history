from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Poll, Choice


class PollHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "question"]
    history_list_display = ["history_type"]
    search_fields = ['question', 'modified_by__username']


admin.site.register(Poll, PollHistoryAdmin)
admin.site.register(Choice, SimpleHistoryAdmin)
