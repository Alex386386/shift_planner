from django.contrib import admin

from .models import Worker, Month, Day


class WorkerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class MonthAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'month_number']
    list_filter = ['year']
    search_fields = ['year', 'month_number']


class DayInline(admin.TabularInline):
    model = Day.workers.through
    extra = 1


class DayAdmin(admin.ModelAdmin):
    list_display = ['id', 'day_number', 'month', 'workers_required']
    list_filter = ['month']
    inlines = [DayInline]
    exclude = ('workers',)


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Month, MonthAdmin)
admin.site.register(Day, DayAdmin)
