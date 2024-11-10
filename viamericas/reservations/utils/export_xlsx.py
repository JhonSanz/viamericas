import openpyxl
from django.http import HttpResponse


def export_to_excel(*, filename, Queryset, headers, model_props):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = filename

    ws.append(headers)
    for query_item in Queryset:
        row = [getattr(query_item, model_prop) for model_prop in model_props]
        ws.append(row)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=books.xlsx"
    wb.save(response)
    return response
