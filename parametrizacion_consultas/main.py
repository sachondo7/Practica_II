from data.config import SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT
from data.mails import lista_correos, asesores_info
from data.queries import query_templates, query_universal
from utils.email_operations import send_dataframe_as_email
from utils.db_operations import create_and_format_dataframes, create_another_dataframe

def main():
    print("Hello, world!")

    query_result_dict = create_and_format_dataframes(query_templates, asesores_info)
    send_dataframe_as_email(query_result_dict, SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT)
    query_result_dict = create_another_dataframe(query_universal, lista_correos)
    send_dataframe_as_email(query_result_dict, SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT)


if __name__ == "__main__":
    main()