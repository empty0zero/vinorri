from django.contrib import admin
from .models import guest
from django.http import HttpResponse
from openpyxl import Workbook

def download_for_excel(modeladmin, request, queryset):
    
    # Экспорт выбранных объектов модели в Excel.
    
    # Создаем книгу Excel и лист
    wb = Workbook()
    ws = wb.active
    ws.title = "Export"

    # Заголовки столбцов
    headers = ['First Name', 'Last Name', 'Consent', 'Alcohol']
    ws.append(headers)

    # Заполняем строки данными
    for obj in queryset:
        # Массив alcohol преобразуем в строку через запятую
        alcohol_str = ", ".join(obj.alcohol)
        ws.append([obj.first_name, obj.last_name, obj.consent, alcohol_str])

    # Создаем HTTP-ответ с Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="export.xlsx"'

    # Сохраняем книгу в ответ
    wb.save(response)
    return response

download_for_excel.short_description = "Скачать выбранные объекты в Excel"


@admin.register(guest)
class GuestAdminPage(admin.ModelAdmin):
    
    # Админ-панель модели гостей
    
    list_display = ('first_name', 'last_name', 'consent', 'alcohol')
    actions = [download_for_excel]
    list_filter = (
        ('consent', admin.BooleanFieldListFilter),
    )