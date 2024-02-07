from openpyxl.styles import NamedStyle, Font, PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import xlsxwriter
import pandas as pd

def estandarizar_fechas(df, formatos):
    for columna in df.columns:
            for formato in formatos:
                try:
                    temp = pd.to_datetime(df[columna], format=formato, errors='raise')
                    df[columna] = temp.dt.strftime('%d/%m/%Y')
                    break 
                except (ValueError, TypeError):
                    continue

def get_custom_header_format(workbook):
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#001689',  # Color de fondo RGB(0, 22, 137)
        'font_color': 'white',   # Color de la letra
        'border': 1
    })
    return header_format    

def convert_columns_to_numeric(dataframe):
    for column in dataframe.columns:
        if dataframe[column].apply(lambda x: x.replace('.', '', 1).isdigit() if isinstance(x, str) else True).all():
            dataframe[column] = pd.to_numeric(dataframe[column], errors='ignore')
    return dataframe

def get_custom_number_format(workbook):
    positive_number_format = workbook.add_format({'num_format': '#,##0', 'align': 'right'})
    negative_number_format = workbook.add_format({'num_format': '#,##0', 'font_color': 'red', 'align': 'right'})
    return positive_number_format, negative_number_format

def apply_number_formats(workbook, worksheet, dataframe):
    positive_number_format, negative_number_format = get_custom_number_format(workbook)
    for col_idx, col in enumerate(dataframe.columns):
        if pd.api.types.is_numeric_dtype(dataframe[col]):
            for row_idx, value in enumerate(dataframe[col], start=1):
                if pd.notnull(value):  # Aseguramos que no se trate de un NaN
                    cell_format = negative_number_format if value < 0 else positive_number_format
                    worksheet.write_number(row_idx, col_idx, value, cell_format)

def adjust_column_widths(workbook, worksheet, dataframe):
    for col_idx, column in enumerate(dataframe):
        max_col_width = max(
            dataframe[column].astype(str).apply(len).max(), 
            len(str(column)) 
        ) + 2 
        worksheet.set_column(col_idx, col_idx, max_col_width)

def find_first_numeric_column(dataframe):
    for column in dataframe.columns:
        if pd.api.types.is_numeric_dtype(dataframe[column]):
            return column
    return None

def sort_dataframe_by_first_numeric_column(dataframe):
    first_numeric_column = find_first_numeric_column(dataframe)
    if first_numeric_column:
        dataframe.sort_values(by=first_numeric_column, ascending=True, inplace=True)
    return dataframe