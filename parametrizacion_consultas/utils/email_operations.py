import smtplib
from email.message import EmailMessage
from io import BytesIO
import pandas as pd
from .excel_operations import estandarizar_fechas, get_custom_header_format, convert_columns_to_numeric, get_custom_number_format, apply_number_formats, adjust_column_widths, find_first_numeric_column, sort_dataframe_by_first_numeric_column
import xlsxwriter
from data.config import HTML_CONTENT

def send_dataframe_as_email(query_result_dict, smtp_user, smtp_password, smtp_server, smtp_port):
    for correo_destinatario, dataframes in query_result_dict.items():
        with BytesIO() as excel_file:
            with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                workbook = writer.book
                for df in dataframes:
                    df = convert_columns_to_numeric(df)
                    df = sort_dataframe_by_first_numeric_column(df)
                    first_numeric_column_name = find_first_numeric_column(df)
                    sheet_name = first_numeric_column_name if first_numeric_column_name else 'Sheet1'
                    header_format = get_custom_header_format(workbook)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    worksheet = writer.sheets[sheet_name]
                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                    adjust_column_widths(workbook, worksheet, df)
                    apply_number_formats(workbook, worksheet, df)
            msg = EmailMessage()
            msg['Subject'] = 'Dataset Adjunto'
            msg['From'] = smtp_user
            msg['To'] = correo_destinatario
            msg.set_content(HTML_CONTENT, subtype='html')
            msg.add_attachment(excel_file.getvalue(),
                               maintype='application',
                               subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                               filename='Patrimonios_Clientes.xlsx')
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(smtp_user, smtp_password)
                    server.send_message(msg)
                    print(f"Correo enviado exitosamente a {correo_destinatario}!")
            except Exception as e:
                print(f"Error al enviar el correo a {correo_destinatario}: {e}")