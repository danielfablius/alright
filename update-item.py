# If you DO have the WhatsApp Desktop app installed
import dretail
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
parser.add_argument('targets', nargs=3, type=int,
                    help='Target items for all branches, each for DAGO, NARIPAN, and SERANG respectively.')
parser.add_argument('interval', nargs='?', type=int, help='The interval in which the update should occur.', default=0)
parser.add_argument('-s', '--skip-initial', action='store_true',
                    help='Whether the update should trigger immediately or wait for the next interval.')
args = parser.parse_args()

locale.setlocale(locale.LC_TIME, 'id_ID.utf8')

whatsapp_group_koordinasi_bandung = 'KOORDINASI TARGET 1994 BANDUNG'
# whatsapp_group_koordinasi_bandung = 'XD'
whatsapp_group_koordinasi_serang = 'KOORDINASI TARGET 1994 SERANG'
# whatsapp_group_koordinasi_serang = 'XD'

DEPARTMENT_CATEGORY_LIST = {
    'MINUMAN': ['espresso', 'teas', 'powder', 'espresso based', 'tea', 'powder based', 'large', 'mocktails', 'blend',
                'manual', 'manual brew', 'bukber_minuman', ],
    'MAKANAN': ['bites', 'dessert', 'eats', 'eats and bites', 'rice bowl', 'bukber_makanan', ],
    'CROISSANT': ['croissant', ],
    'CAKE': ['cake', ],
}

headers = {
    'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjE5OTRjbmNzQGdtYWlsLmNvbSIsImNvbXBhbnlpZCI6ODczMywidXNlcl9pZCI6MzI4NDV9.j6Y705cfds-CNSFCIExv8GkV4_S3jlLF_ar-h8EPVnk',
}

branches = [
    Branch(
        ["ODczMw==", ],
        [10210, ],
        'DAGO',
        ['582E227AX2XLTOJCDDGAQX84O1CA8C39', ],
        ['5b0c7b868ca031f555e490e9b29fd8de', ],
        ['a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5', ],
        args.targets[0],
        whatsapp_group_koordinasi_bandung,
        10,
        4,
        (450, 450, 450, 450, 600, 1000, 600,),
    ),
    Branch(
        ["ODczMw==", ],
        [14376, ],
        'NARIPAN',
        ['582E227AX2XLTOJCDDGAQX84O1CA8C39', ],
        ['5b0c7b868ca031f555e490e9b29fd8de', ],
        ['a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5', ],
        args.targets[1],
        whatsapp_group_koordinasi_bandung,
        7,
        4,
        (350, 350, 350, 350, 450, 600, 450,),
    ),
    Branch(
        ["ODczMw==", ],
        [16284, ],
        'SERANG ATAS',
        ['582E227AX2XLTOJCDDGAQX84O1CA8C39', ],
        ['5b0c7b868ca031f555e490e9b29fd8de', ],
        ['a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5', ],
        args.targets[2],
        whatsapp_group_koordinasi_serang,
        10,
        4,
        (1000, 1000, 1000, 1000, 1500, 2500, 1500,),
    ),
    Branch(
        ["MTMxODI=", ],
        [16179, ],
        'SERANG BAWAH',
        ['865038d2211cd111b16dd23e39ea342f', ],
        ['6549F75F84PCI8HOCAIWBM2P5E3K070F', ],
        ['b8YFauEf1FfJjVu%2Fx1wHRvYBDnbRS6CKIQBAYUDqyWK0nszbtZMb2HuUILEBZsNHo%2FRZRGOjhaH4LGkj%2BlQlu5Uy55iSOsJOydM45NJlbf2X6RfQG%2Fj2fLc7LeHYlxkp2C0S9A%2F5Rrs7O5%2BxQXWdX41Qmgir6FLKSu%2Bkt4aoVShlRgXAesQHjDPRS3sHSRr3CCQCRz%2BFTyWG1fUTObOMVdcrfmE9Qmfz6Qs6SGOoxsHnOHDenAhDFdY3UdTaCgEsJZ9xbH5vrQR0F3%2FSfYVsm6QkZEQkCuZqaNE8G1tCMC8RDqZGwOK54635aB5jx8ViSH4USbax2cpY9RJ0laC1bKa321gp7Kr%2BE9RMTqp7sw3AJfIhxFzL0evIgmVriCmonqkGN16rJv2yE1aBNDrlvrHjOlDutEEiZMmwx7JVFbM%3Dbfd16832cae10478f51a7e7257ac9c15087e5a93', ],
        args.targets[2],
        whatsapp_group_koordinasi_serang,
        10,
        4,
        (1000, 1000, 1000, 1000, 1500, 2000, 1500,),
    ),
    Branch(
        ["ODczMw==", "MTMxODI=", ],
        [16284, 16179, ],
        'SERANG',
        ['582E227AX2XLTOJCDDGAQX84O1CA8C39', '865038d2211cd111b16dd23e39ea342f', ],
        ['5b0c7b868ca031f555e490e9b29fd8de', '6549F75F84PCI8HOCAIWBM2P5E3K070F', ],
        ['a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5',
         'b8YFauEf1FfJjVu%2Fx1wHRvYBDnbRS6CKIQBAYUDqyWK0nszbtZMb2HuUILEBZsNHo%2FRZRGOjhaH4LGkj%2BlQlu5Uy55iSOsJOydM45NJlbf2X6RfQG%2Fj2fLc7LeHYlxkp2C0S9A%2F5Rrs7O5%2BxQXWdX41Qmgir6FLKSu%2Bkt4aoVShlRgXAesQHjDPRS3sHSRr3CCQCRz%2BFTyWG1fUTObOMVdcrfmE9Qmfz6Qs6SGOoxsHnOHDenAhDFdY3UdTaCgEsJZ9xbH5vrQR0F3%2FSfYVsm6QkZEQkCuZqaNE8G1tCMC8RDqZGwOK54635aB5jx8ViSH4USbax2cpY9RJ0laC1bKa321gp7Kr%2BE9RMTqp7sw3AJfIhxFzL0evIgmVriCmonqkGN16rJv2yE1aBNDrlvrHjOlDutEEiZMmwx7JVFbM%3Dbfd16832cae10478f51a7e7257ac9c15087e5a93', ],
        args.targets[2],
        whatsapp_group_koordinasi_serang,
        10,
        4,
        (1000, 1000, 1000, 1000, 1500, 2000, 1500,),
    ),
]

messenger = WhatsApp()


def get_report_date_range():
    now = datetime.datetime.now()
    start_hour = datetime.datetime.today().replace(hour=8, minute=0, second=0, microsecond=0)

    if now.hour < 3:
        return (start_hour - datetime.timedelta(1)), (now - datetime.timedelta(1)).replace(hour=4, minute=0, second=0)
    else:
        return start_hour, now.replace(hour=23, minute=59, second=0)


def get_laporan_sales_by_category(branch_id, company_id, start_date, start_time, end_date, end_time, cookies):
    # The interval in which the sales report will be retrieved
    print(
        f'{branch.get_start_date_string()} {branch.get_start_time()} - {branch.get_end_date_string()} {branch.get_end_time()}')

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


def get_report_salesrealtime_detail(cookies):
    def get_report(reffnumber):
        data = {
            'reffnumber': reffnumber,
        }

        response = requests.post(
            'https://backoffice.dretail.id/mpos-server/index.php/C_report_salesrealtime/details',
            cookies=cookies,
            headers=headers,
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
    headers = {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjE5OTRjbmNzQGdtYWlsLmNvbSIsImNvbXBhbnlpZCI6ODczMywidXNlcl9pZCI6MzI4NDV9.j6Y705cfds-CNSFCIExv8GkV4_S3jlLF_ar-h8EPVnk',
    }

    response = requests.post(
        'https://backoffice.dretail.id/mpos-server/index.php/C_report_salesrealtime/getData',
        cookies=cookies,
        headers=headers,
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
    CROISSANT = sum([items[x] for x in items.keys() if x.lower() in DEPARTMENT_CATEGORY_LIST['CROISSANT']])
    CAKE = sum([items[x] for x in items.keys() if x.lower() in DEPARTMENT_CATEGORY_LIST['CAKE']])
    MINERAL_WATER = sum([items[x] for x in items.keys() if x.lower() == 'mineral water'])
    BEER = items['Beer'] + items['BEER']
    ROKOK = items['Rokok'] + items['ROKOK']
    PAKET_BUKBER = items['Paket Bukber']
    PAKET_BUKBER_ITEMS = items['bukber_makanan'] + items['bukber_minuman']
    EVENT = items['Event']
    MERCHANDISE = items['Merchandise']
    OPEN_BILL = items.get('OPEN_BILL')
    PARKIR = items['Parkir']
    TOTAL = MINUMAN + MAKANAN + BEER + CROISSANT + CAKE + MINERAL_WATER

    return TOTAL, f'MINUMAN: {MINUMAN}\n' + \
                  f'MAKANAN: {MAKANAN}\n' + \
                  (f'CROISSANT: {CROISSANT}\n' if CROISSANT else '') + \
                  (f'CAKE: {CAKE}\n' if CAKE else '') + \
                  (f'MINERAL WATER: {MINERAL_WATER}\n' if MINERAL_WATER else '') + \
                  (f'BEER: {BEER}\n' if BEER else '') + \
                  (f'ROKOK: {ROKOK}\n' if ROKOK else '') + \
                  (f'PAKET BUKBER: {PAKET_BUKBER_ITEMS} ({PAKET_BUKBER} Paket)\n' if PAKET_BUKBER else '') + \
                  (f'EVENT: {EVENT}\n' if EVENT else '') + \
                  (f'MERCHANDISE: {MERCHANDISE}\n' if MERCHANDISE else '') + \
                  (f'OPEN BILL: {OPEN_BILL}\n' if OPEN_BILL else '') + \
                  (f'PARKIR: {PARKIR}\n' if PARKIR else '') + \
                  f'_*TOTAL: {TOTAL}*_\n'


def get_sales_by_category(branch, final=False):
    items = defaultdict(int)
    ob_items = defaultdict(int)

    for backoffice in branch.backoffices:
        df_laporan_sales = dretail.get_laporan_sales_by_item_detail(
            backoffice.branch_id,
            backoffice.company_id,
            branch.get_start_date_string(),
            branch.get_start_time(),
            branch.get_end_date_string(),
            branch.get_end_time(),
            backoffice.get_cookies()
        )

        for _, row in df_laporan_sales.iterrows():
            if row['Item Name'] == 'TOTAL' or pd.isna(row['Category']):
                continue

            if row['Category'] == 'Paket Bukber':
                if 'Ala-ala' in row['Item Name'] or 'Jomblo' in row['Item Name']:
                    items['bukber_minuman'] += (1 * (row['Item Sold'] - row['Item Void']))
                elif 'Bucin' in row['Item Name']:
                    items['bukber_minuman'] += (2 * (row['Item Sold'] - row['Item Void']))
                elif 'Gosip' in row['Item Name']:
                    items['bukber_minuman'] += (4 * (row['Item Sold'] - row['Item Void']))
                
                for bukber_menu_modifier in row['Modifier'].split(','):
                    bukber_menu, qty = bukber_menu_modifier.rsplit(' ', maxsplit=1)
                    items['bukber_makanan'] += int(qty.rstrip('X'))

            items[row['Category']] += row['Item Sold'] - row['Item Void']

        df_open_bill_sales = get_open_bill(backoffice.branch_id, backoffice.get_cookies())

        for item in df_open_bill_sales:
            if item['catName'] == 'Paket Bukber':
                if 'Ala-ala' in item['name'] or 'Jomblo' in item['name']:
                    ob_items['bukber_makanan'] += (1 * (item['qty'] - item['voidQty']))
                    ob_items['bukber_minuman'] += (1 * (item['qty'] - item['voidQty']))
                elif 'Bucin' in item['name']:
                    ob_items['bukber_makanan'] += (3 * (item['qty'] - item['voidQty']))
                    ob_items['bukber_minuman'] += (2 * (item['qty'] - item['voidQty']))
                elif 'Gosip' in item['name']:
                    ob_items['bukber_makanan'] += (6 * (item['qty'] - item['voidQty']))
                    ob_items['bukber_minuman'] += (4 * (item['qty'] - item['voidQty']))

            ob_items[item['catName']] += item['qty'] - item['voidQty']

    TOTAL_ITEMS, ITEMS_PRINTS = print_items(items)
    TOTAL_OB, OB_PRINTS = print_items(ob_items)

    GRAND_TOTAL = TOTAL_ITEMS + TOTAL_OB

    TARGET = branch.get_target(GRAND_TOTAL)

    if final and TOTAL_OB == 0:
        # Regenerate Items Prints with Open Bill
        items['OPEN_BILL'] = TOTAL_OB
        TOTAL_ITEMS, ITEMS_PRINTS = print_items(items)

        msg = \
            f'*FINAL ITEM {branch.name}*\n' + \
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


def get_sales_data_week_range(branch, start_date, end_date):
    """
    Get sales data from start_date to end_date.
    Each day runs from 10 AM to next day 6 AM.
    Returns a dictionary with aggregated item counts for the entire period.
    """
    # Ensure we have datetime objects at 10 AM
    current_start = datetime.datetime.combine(start_date, datetime.time(10, 0, 0))
    end_datetime = datetime.datetime.combine(end_date, datetime.time(23, 59, 59))
    
    monthly_items = defaultdict(int)
    
    print(f'\n*Fetching weekly sales data for {branch.name}*')
    print(f'Period: {start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")}')
    
    # Loop through each day until end_date
    while current_start.date() <= end_date:
        # Each day runs from 10 AM to next day 6 AM
        current_end = current_start + datetime.timedelta(days=1)
        current_end = current_end.replace(hour=6, minute=0, second=0)
        
        print(f"Fetching: {current_start.strftime('%d/%m/%Y %H:%M')} - {current_end.strftime('%d/%m/%Y %H:%M')}")
        
        # Get sales by category for this day
        items = defaultdict(int)
        
        for backoffice in branch.backoffices:
            df_laporan_sales = get_laporan_sales_by_category(
                backoffice.branch_id,
                backoffice.company_id,
                current_start.strftime('%d/%m/%Y'),
                current_start.strftime('%H:%M'),
                current_end.strftime('%d/%m/%Y'),
                current_end.strftime('%H:%M'),
                backoffice.get_cookies()
            )

            for _, row in df_laporan_sales.iterrows():
                items[row['Category']] += row['Item Sold'] - row['Item Void']
        
        # Aggregate daily data into totals
        for category, count in items.items():
            monthly_items[category] += count
        
        # Move to next day
        current_start = current_start + datetime.timedelta(days=1)
        current_start = current_start.replace(hour=10, minute=0, second=0)
    
    return monthly_items


def get_sales_data_month_to_yesterday(branch):
    """
    Get sales data from the first day of yesterday's month until yesterday.
    Each day runs from 10 AM to next day 6 AM.
    Returns a dictionary with aggregated item counts for the entire period.
    """
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    first_day_of_month = yesterday.replace(day=1).date()
    return get_sales_data_week_range(branch, first_day_of_month, yesterday.date())


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


def should_do_final(branch):
    now = datetime.datetime.now()
    # has_final = final_item_recorder[branch.branch_id][branch.get_shifting_date().date()] = True
    return branch.closing_hour <= now.hour <= branch.closing_hour + 2


if args.skip_initial:
    seconds_to_sleep = get_seconds_to_sleep()
    print(f'Skipping initial update. Next update in {seconds_to_sleep // 60} minute(s).')
    time.sleep(seconds_to_sleep)

# Configuration for weekly report
WEEKLY_REPORT_CHECK_HOUR = 12  # 12 PM - check daily at this hour
def get_last_sunday():
    """Get the date of the most recent Sunday (last completed week)."""
    today = datetime.datetime.now().date()
    # If today is Sunday, get last Sunday (7 days ago)
    # Otherwise, get the most recent Sunday
    days_since_sunday = (today.weekday() + 1) % 7
    if days_since_sunday == 0:
        days_since_sunday = 7
    last_sunday = today - datetime.timedelta(days=days_since_sunday)
    return last_sunday


def get_month_start_from_sunday(sunday_date):
    """Get the first day of the month for the given Sunday."""
    return sunday_date.replace(day=1)


def get_monday_message_flag_file(branch):
    """Get the flag file name for a specific branch."""
    return f'weekly_report_{branch.name.replace(" ", "_")}.txt'


def has_weekly_report_been_sent(branch, sunday_date):
    """Check if weekly report has been sent for a specific week ending on sunday_date."""
    flag_file = get_monday_message_flag_file(branch)
    try:
        with open(flag_file, 'r') as f:
            last_sent_date_str = f.read().strip()
            if last_sent_date_str:
                last_sent_date = datetime.datetime.strptime(last_sent_date_str, '%Y-%m-%d').date()
                # Check if the report for this week (ending on sunday_date) has been sent
                return last_sent_date == sunday_date
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'Error reading weekly report flag file for {branch.name}: {e}')
    return False


def mark_weekly_report_as_sent(branch, sunday_date):
    """Mark weekly report as sent for a specific week ending on sunday_date."""
    flag_file = get_monday_message_flag_file(branch)
    try:
        with open(flag_file, 'w') as f:
            f.write(sunday_date.strftime('%Y-%m-%d'))
    except Exception as e:
        print(f'Error writing weekly report flag file for {branch.name}: {e}')


while True:
    now = datetime.datetime.now()
    
    # Check every iteration if weekly report needs to be sent
    last_sunday = get_last_sunday()
    month_start = get_month_start_from_sunday(last_sunday)
    
    # Check and send report for each branch individually
    for branch in branches:
        if not has_weekly_report_been_sent(branch, last_sunday):
            try:
                print(f'\nWeekly report check at {now.strftime("%Y-%m-%d %H:%M:%S")}')
                print(f'Sending weekly report for {branch.name} (period ending {last_sunday.strftime("%d %B %Y")})...')
                
                weekly_items = get_sales_data_week_range(branch, month_start, last_sunday)
                
                # Format the weekly sales report
                TOTAL_ITEMS, ITEMS_PRINTS = print_items(weekly_items)
                
                # Calculate number of days and average
                num_days = (last_sunday - month_start).days + 1
                average_per_day = TOTAL_ITEMS / num_days if num_days > 0 else 0
                
                msg = \
                    f'*WEEKLY REPORT - {branch.name}*\n' + \
                    f'*Period: {month_start.strftime("%d %B %Y")} - {last_sunday.strftime("%d %B %Y")}*\n' + \
                    '\n' + \
                    ITEMS_PRINTS + \
                    f'\n*AVERAGE PER DAY: {average_per_day:.1f}*'
                
                print(f'Sending weekly report to {branch.whatsapp_group_name}')
                # messenger.send_direct_message(branch.whatsapp_group_name, msg)
                
                # Mark as sent for this specific week
                mark_weekly_report_as_sent(branch, last_sunday)
                print(f'Weekly report sent successfully for {branch.name}')
                
            except Exception as e:
                print(f'Failed to fetch/send weekly report for {branch.name}: {e}')
    
    for branch in branches:
        if not (branch.closing_hour < datetime.datetime.now().hour < branch.opening_hour):
            try:
                get_sales_by_category(branch, should_do_final(branch))
            except Exception as e:
                print(e)

    seconds_to_sleep = get_seconds_to_sleep()
    print(f'Update success. Next update in {seconds_to_sleep // 60} minute(s).')
    time.sleep(seconds_to_sleep)
