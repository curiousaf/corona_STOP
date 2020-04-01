from django.contrib import admin
from .models import Question, Output, Result

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)


# Register your models here.

# admin.site.register(Question)
#admin.site.register(Output)

@admin.register(Output)
@admin.register(Result)
@admin.register(Question)
class EntityAdmin(admin.ModelAdmin):
    list_filter = (('country', ChoiceDropdownFilter),)
    