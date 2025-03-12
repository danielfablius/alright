# If you DO have the WhatsApp Desktop app installed
from alright import WhatsApp
from operator import itemgetter
from collections import defaultdict
import argparse
import datetime
import locale
import json
import pandas as pd
import requests
import time

from branch import Branch


parser = argparse.ArgumentParser()
parser.add_argument('targets', nargs=3, type=int, help='Target items for all branches, each for DAGO, NARIPAN, and SERANG respectively.')
parser.add_argument('interval', nargs='?', type=int, help='The interval in which the update should occur.', default=0)
parser.add_argument('-s', '--skip-initial', action='store_true', help='Whether the update should trigger immediately or wait for the next interval.')
args = parser.parse_args()

locale.setlocale(locale.LC_TIME, 'id_ID.utf8')

whatsapp_group_koordinasi_bandung = 'KOORDINASI TARGET 1994 BANDUNG'
whatsapp_group_koordinasi_serang = 'KOORDINASI TARGET 1994 SERANG'

DEPARTMENT_CATEGORY_LIST = {
    'MINUMAN': ['espresso', 'teas', 'powder', 'espresso based', 'tea', 'powder based', 'large', 'mocktails', 'blend', 'manual', 'manual brew', ],
    'MAKANAN': ['bites', 'dessert', 'eats', 'eats and bites', ],
}

branches = [
    Branch(
        [8733, ],
        [10210, ],
        'DAGO',
        ['582E227AX2XLTOJCDDGAQX84O1CA8C39', ],
        ['5b0c7b868ca031f555e490e9b29fd8de', ],
        ['a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5', ],
        args.targets[0],
        whatsapp_group_koordinasi_bandung,
        10,
        3,
    ),
    Branch(
        [8733, ],
        [14376, ],
        'NARIPAN',
        ['582E227AX2XLTOJCDDGAQX84O1CA8C39', ],
        ['5b0c7b868ca031f555e490e9b29fd8de', ],
        ['a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5', ],
        args.targets[1],
        whatsapp_group_koordinasi_bandung,
        8,
        3,
    ),
    Branch(
        [8733, 13182, ],
        [16284, 16179, ],
        'SERANG',
        ['582E227AX2XLTOJCDDGAQX84O1CA8C39', '865038d2211cd111b16dd23e39ea342f', ],
        ['5b0c7b868ca031f555e490e9b29fd8de', '6549F75F84PCI8HOCAIWBM2P5E3K070F', ],
        ['a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5', 'b8YFauEf1FfJjVu%2Fx1wHRvYBDnbRS6CKIQBAYUDqyWK0nszbtZMb2HuUILEBZsNHo%2FRZRGOjhaH4LGkj%2BlQlu5Uy55iSOsJOydM45NJlbf2X6RfQG%2Fj2fLc7LeHYlxkp2C0S9A%2F5Rrs7O5%2BxQXWdX41Qmgir6FLKSu%2Bkt4aoVShlRgXAesQHjDPRS3sHSRr3CCQCRz%2BFTyWG1fUTObOMVdcrfmE9Qmfz6Qs6SGOoxsHnOHDenAhDFdY3UdTaCgEsJZ9xbH5vrQR0F3%2FSfYVsm6QkZEQkCuZqaNE8G1tCMC8RDqZGwOK54635aB5jx8ViSH4USbax2cpY9RJ0laC1bKa321gp7Kr%2BE9RMTqp7sw3AJfIhxFzL0evIgmVriCmonqkGN16rJv2yE1aBNDrlvrHjOlDutEEiZMmwx7JVFbM%3Dbfd16832cae10478f51a7e7257ac9c15087e5a93', ],
        args.targets[2],
        whatsapp_group_koordinasi_serang,
        8,
        3,
    )
]

messenger = WhatsApp()


def get_report_date_range():
    now = datetime.datetime.now()
    start_hour = datetime.datetime.today().replace(hour=8, minute=0, second=0, microsecond=0)

    if now.hour < 3:
        return (start_hour - datetime.timedelta(1)), (now-datetime.timedelta(1)).replace(hour=4, minute=0, second=0)
    else:
        return start_hour, now.replace(hour=23, minute=59, second=0)


def get_laporan_sales_by_category(branch_id, company_id, start_date, start_time, end_date, end_time, cookies):
    # The interval in which the sales report will be retrieved
    print(f'{branch.get_start_date_string()} {branch.get_start_time()} - {branch.get_end_date_string()} {branch.get_end_time()}')

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
        'column': '[{"name":"column[]","value":"category_name"},{"name":"column[]","value":"qty"},{"name":"column[]","value":"void"}]',
        'companyid': company_id,
        'company_type': '0',
    }

    response = requests.post(
        'https://backoffice.dretail.id/mpos-server/index.php/C_report_mt_salesbycategory/exportXls',
        cookies=cookies,
        data=data,
    )

    with open(f'laporan_sales_by_category_{branch_id}.xlsx', 'wb') as f:
        f.write(response.content)
    
    return pd.read_excel(f'laporan_sales_by_category_{branch_id}.xlsx', skiprows=7)


def get_laporan_sales_by_item_detail(branch_name):
    branch_id = BRANCH_IDS[branch_name]

    startdate, enddate = get_start_and_end_date(branch_name)
    starttime, endtime = get_start_and_end_time(branch_name, startdate, enddate)

    startdate = startdate.strftime('%d/%m/%Y')
    enddate = enddate.strftime('%d/%m/%Y')

    # The interval in which the sales report will be retrieved
    print(f'{startdate} {starttime} - {enddate} {endtime}')

    data = {
        'radio-duration': 'all-day',
        'time-left': '00',
        'time-left': '00',
        'time-right': '00',
        'time-right': '00',
        'branch': str(branch_id),
        'arr_branch': str(branch_id),
        'arr_staff': '',
        'reportrange': f'{startdate} - {enddate}',
        'duration': f'{starttime} - {endtime}',
        'flagEachday': 'false',
        'column': '[{"name":"column[]","value":"category_name"},{"name":"column[]","value":"qty"},{"name":"column[]","value":"void"}]',
        'companyid': '8733',
        'company_type': '0',
    }

    response = requests.post(
        'https://backoffice.dretail.id/mpos-server/index.php/C_report_mt_salesitem/exportXlsDetail',
        cookies=cookies,
        data=data,
    )

    with open(f'laporan_sales_by_category_{branch_id}.xlsx', 'wb') as f:
        f.write(response.content)

    items = defaultdict(int)
    item_sales = pd.read_excel(f'laporan_sales_by_category_{branch_id}.xlsx', skiprows=7)

    for _, row in item_sales.iterrows():
        items[row['Item Name']] += row['Item Sold'] + row['Item Void']
    
    return items


def get_report_salesrealtime_detail(cookies):
    def get_report(reffnumber):
        data = {
            'reffnumber': reffnumber,
        }

        response = requests.post(
            'https://backoffice.dretail.id/mpos-server/index.php/C_report_salesrealtime/details',
            cookies=cookies,
            data=data,
        )

        opbill_data = json.loads(response.content)
        
        # still unknown why sometimes it returns a list instead of detail
        if type(opbill_data['txnproductitem']) == list:
            return []

        return opbill_data['txnproductitem']['detail']
    return get_report


def get_open_bill(branch_id, cookies):
    data = {
        'draw': '1',
        'branch': str(branch_id),
        'status': 'all status',
        'date': 'today',
        'columns[0][name]': '',
        'order[0][column]': '0',
        'order[0][dir]': '',
    }

    response = requests.post(
        'https://backoffice.dretail.id/mpos-server/index.php/C_report_salesrealtime/getData',
        cookies=cookies,
        data=data,
    )

    salesrealtime_data = json.loads(response.content)
    reffnumbers = filter(lambda x: x != '', map(itemgetter('reff_number'), salesrealtime_data['data']))
    open_bills = list(filter(lambda x: len(x) != 0, map(get_report_salesrealtime_detail(cookies), reffnumbers)))
    
    # convert into flat list of items
    open_bills = [item for sublist in open_bills for item in sublist]
    return open_bills


def print_items(items):
    MINUMAN = sum([items[x] for x in items.keys() if x.lower() in DEPARTMENT_CATEGORY_LIST['MINUMAN']])
    MAKANAN = sum([items[x] for x in items.keys() if x.lower() in DEPARTMENT_CATEGORY_LIST['MAKANAN']])
    BEER = items['Beer'] + items['BEER']
    ROKOK = items['Rokok'] + items['ROKOK']
    EVENT = items['Event']
    MERCHANDISE = items['Merchandise']
    OPEN_BILL = items.get('OPEN_BILL')
    PARKIR = items['Parkir']
    TOTAL = MINUMAN + MAKANAN + BEER

    return TOTAL, f'MINUMAN: {MINUMAN}\n' + \
        f'MAKANAN: {MAKANAN}\n' + \
        (f'BEER: {BEER}\n' if BEER else '') + \
        (f'ROKOK: {ROKOK}\n' if ROKOK else '') + \
        (f'EVENT: {EVENT}\n' if EVENT else '') + \
        (f'MERCHANDISE: {MERCHANDISE}\n' if MERCHANDISE else '') + \
        (f'OPEN BILL: {OPEN_BILL}\n' if OPEN_BILL else '') + \
        (f'PARKIR: {PARKIR}\n' if PARKIR else '') + \
        f'_*TOTAL: {TOTAL}*_\n'


def get_sales_by_category(branch, final=False):
    items = defaultdict(int)
    ob_items = defaultdict(int)

    for backoffice in branch.backoffices:
        df_laporan_sales = get_laporan_sales_by_category(
            backoffice.branch_id,
            backoffice.company_id,
            branch.get_start_date_string(),
            branch.get_start_time(),
            branch.get_end_date_string(),
            branch.get_end_time(),
            backoffice.get_cookies()
        )

        for _, row in df_laporan_sales.iterrows():
            items[row['Category']] += row['Item Sold'] - row['Item Void']
        
        df_open_bill_sales = get_open_bill(backoffice.branch_id, backoffice.get_cookies())

        for item in df_open_bill_sales:
            ob_items[item['catName']] += item['qty'] - item['voidQty']

    TOTAL_ITEMS, ITEMS_PRINTS = print_items(items)
    TOTAL_OB, OB_PRINTS = print_items(ob_items)

    GRAND_TOTAL = TOTAL_ITEMS + TOTAL_OB

    TARGET = branch.get_target(GRAND_TOTAL)

    if final:
        # Regenerate Items Prints with Open Bill
        items['OPEN_BILL'] = TOTAL_OB
        TOTAL_ITEMS, ITEMS_PRINTS = print_items(items)

        msg = \
            f'*[AUTO] UPDATE ITEM {branch.name}*\n' + \
            f'*{branch.get_shifting_date().strftime("%d %B %Y")}*\n' + \
            f'*TARGET*: {TARGET}\n' + \
            '\n' + \
            '*ITEMS*\n' + \
            '\n'.join(ITEMS_PRINTS.splitlines()[:-1]) + \
            '\n' + \
            '\n' + \
            f'*TOTAL: {GRAND_TOTAL}*\n' + \
            f'*MINUS: {TARGET - GRAND_TOTAL}*\n'
    else:
        msg = \
            f'*[AUTO] UPDATE ITEM {branch.name}*\n' + \
            f'*{branch.get_shifting_date().strftime("%d %B %Y")}*\n' + \
            f'*TARGET*: {TARGET}\n' + \
            '\n' + \
            '*ITEMS*\n' + \
            ITEMS_PRINTS + \
            '\n' + \
            '*OPEN BILLS*\n' + \
            OB_PRINTS + \
            '\n' + \
            f'*GRAND TOTAL: {GRAND_TOTAL}*\n' + \
            f'*MINUS: {TARGET - GRAND_TOTAL}*\n'

    print(msg)

    messenger.send_direct_message(branch.whatsapp_group_name, msg)


def get_dynamic_interval():
    with open('interval_schema', 'r') as file:
        interval_schema = [int(line.strip()) for line in file]
        return interval_schema[datetime.datetime.now().hour]


def get_seconds_to_sleep():
    # return seconds to sleep until the next minutes of INTERVAL_IN_MINUTE
    interval_in_minute = max(2, args.interval) if args.interval > 0 else get_dynamic_interval()
    now = datetime.datetime.now()
    minutes_to_sleep = interval_in_minute - now.minute % interval_in_minute
    return minutes_to_sleep * 60 - now.second


def should_do_final():
    now = datetime.datetime.now()
    return now.hour == 3 and now.minute == 0


if args.skip_initial:
    seconds_to_sleep = get_seconds_to_sleep()
    print(f'Skipping initial update. Next update in {seconds_to_sleep // 60} minute(s).')
    time.sleep(seconds_to_sleep)


while True:
    for branch in branches:
        if not (branch.closing_hour <= datetime.datetime.now().hour < branch.opening_hour):
            try:
                get_sales_by_category(branch, should_do_final())
            except Exception as e:
                print(e)
    
    seconds_to_sleep = get_seconds_to_sleep()
    print(f'Update success. Next update in {seconds_to_sleep // 60} minute(s).')
    time.sleep(seconds_to_sleep)
