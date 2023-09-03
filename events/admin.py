from django.contrib import admin
from django.db import models
from django.db.models import F
from martor.models import MartorField
from martor.admin import AdminMartorWidget
# from django_markdown.models import MarkdownField
# from django_markdown.widgets import AdminMarkdownWidget
from django.http.response import HttpResponse
from django.template.defaultfilters import slugify
import csv

from .models import Event

class SeatsFilterList(admin.SimpleListFilter):

    title = 'Seats'
    parameter_name = 'seats'

    def lookups(self, request, model_admin):
        return (
            ('FULL', 'Seats Full'),
            ('VACENT', 'Seats Vacant'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'FULL':
            return queryset.filter(seats=F('max_seats'))
        if self.value() == 'VACANT':
            return queryset.filter(seats__lte=F('max_seats'))

#For downloading csv of events

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  list_display = ['event_code', 'day', 'start', 'end', 'title']
  list_filter = ('is_featured',)

  actions = ['export_as_csv']

  @admin.action(description="Download Csv")
  def export_as_csv(self, request, queryset):
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)
    fields= None
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    for obj in queryset:
      row = []
      for field in headers:
          if field in headers:
              val = getattr(obj, field)
              if callable(val):
                  val = val()
              row.append(val)

      writer.writerow(row)
    # Return CSV file to browser as download
    return response
class EventAdmin(admin.ModelAdmin):
  list_filter = ('day', 'category', 'is_featured', SeatsFilterList, 'is_fcrit_only')
  search_fields = ('event_code', 'title', 'description', )
  formfield_overrides = {MartorField: {'widget': AdminMartorWidget}}
