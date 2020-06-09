from django.contrib import admin
from .models import ScrapedData
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.utils.translation import ugettext_lazy

# Register your models here.
admin.site.site_header = ugettext_lazy('Catalyst Rss Worker Admin Panel')
admin.site.site_title = "Catalyst Rss Worker Admin Panel"
admin.site.index_title = "Welcome to Catalyst Rss Worker"

class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ("Title","Description","Date","url")
    list_filter = (
        ("Date",admin.DateFieldListFilter),
        ('Date', DateRangeFilter),
        )
    search_fields = ('Title',"Description","Date")

admin.site.register(ScrapedData,ScrapedDataAdmin)