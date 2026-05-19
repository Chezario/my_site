from django.contrib import admin
from .models import Printers, Room, Security, Broker, SecurityTransaction, UploadedFile


@admin.action(description="Переместить выбранные операции в архив")
def make_closed(modeladmin, request, queryset):
    queryset.update(is_on_dashboard=False)


class SecurityTransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_on_dashboard']
    # search_fields = ['security__name']
    list_filter = ['security', 'is_on_dashboard']
    actions = [make_closed]

    def get_changeform_initial_data(self, request):
        return {'user': request.user}




admin.site.register(Room)
admin.site.register(Printers)
admin.site.register(Security)
admin.site.register(Broker)
admin.site.register(SecurityTransaction, SecurityTransactionAdmin)
admin.site.register(UploadedFile)

