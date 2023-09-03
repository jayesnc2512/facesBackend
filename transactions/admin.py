import datetime
from django.contrib import admin
from django import forms

from .models import Transaction
from users.models import Participation
from django.http.response import HttpResponse
from django.template.defaultfilters import slugify
import csv


class TransactionForm(forms.ModelForm):
  class Meta:
    model = Transaction
    fields = '__all__'
  
  participations = forms.ModelMultipleChoiceField(queryset=Participation.objects.all())

  def __init__(self, *args, **kwargs):
    super(TransactionForm, self).__init__(*args, **kwargs)
    if self.instance:
      self.fields['participations'].initial = self.instance.participations.all()

  #   def save(self, *args, **kwargs):
  #     # FIXME: 'commit' argument is not handled
  #     # TODO: Wrap reassignments into transaction
  #     # NOTE: Previously assigned Foos are silently reset
  #     instance = super(TransactionForm, self).save(commit=False)
  #     self.fields['participations'].initial.update(transaction=None)
  #     self.cleaned_data['participations'].update(transaction=instance)
  #     return instance

class DateFilterList(admin.SimpleListFilter):

  title = 'Day'
  parameter_name = 'timestamp'

  def lookups(self, request, model_admin):
    return (
      ('D1', 'Today'),
      ('D2', 'Yesterday'),
      ('D3', 'Day before Yesterday'),
    )

  def queryset(self, request, queryset):
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    day_before_yesterday = today - datetime.timedelta(days=2)

    if self.value() == 'D1':
        return queryset.filter(timestamp__gte=f"{today.year}-{today.month}-{today.day}")
    if self.value() == 'D2':
      return queryset.filter(timestamp__gte=f"{yesterday.year}-{yesterday.month}-{yesterday.day}", timestamp__lt=f"{today.year}-{today.month}-{today.day}")
    if self.value() == 'D2':
      return queryset.filter(timestamp__gte=f"{day_before_yesterday.year}-{day_before_yesterday.month}-{day_before_yesterday.day}", timestamp__lt=f"{yesterday.year}-{yesterday.month}-{yesterday.day}")


@admin.register(Transaction)
class EventAdmin(admin.ModelAdmin):
  list_display = ['transaction_id', 'upi_transaction_id', 'timestamp', 'event_amount', 'total_amount']
  list_filter = ('is_paid','is_verified')

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
  
  # ordering = ['-timestamp']
