import requests
import pandas as pd


def get_laporan_sales_by_item_detail(branch_id, company_id, start_date, start_time, end_date, end_time, cookies):
    # The interval in which the sales report will be retrieved
    print(f'{start_date} {start_time} - {end_date} {end_time}')

    data = {
        'radio-duration': 'all-day',
        'time-left': '00',
        'time-left': '00',
        'time-right': '00',
        'time-right': '00',
        'branch': str(branch_id),
        'arr_branch': str(branch_id),
        'arr_staff': '',
        'reportrange': f'{start_date} - {end_date}',
        'duration': f'{start_time} - {end_time}',
        'flagEachday': 'false',
        'column': '[{"name":"column[]","value":"item_name"},{"name":"column[]","value":"modifier"},{"name":"column[]","value":"category_name"},{"name":"column[]","value":"qty"},{"name":"column[]","value":"grosssales"},{"name":"column[]","value":"void"},{"name":"column[]","value":"voidamount"},{"name":"column[]","value":"discount"},{"name":"column[]","value":"discount_bill"},{"name":"column[]","value":"amount_redeem"},{"name":"column[]","value":"total"},{"name":"column[]","value":"service"},{"name":"column[]","value":"tax"},{"name":"column[]","value":"grandtotal"}]',
        'companyid': company_id,
        'company_type': '0',
    }

    response = requests.post(
        'https://backoffice.dretail.id/mpos-server/index.php/C_report_mt_salesitem/exportXls',
        cookies=cookies,
        data=data,
    )

    with open(f'laporan_sales_by_item_{branch_id}_detail.xlsx', 'wb') as f:
        f.write(response.content)

    return pd.read_excel(f'laporan_sales_by_item_{branch_id}_detail.xlsx', skiprows=7)
