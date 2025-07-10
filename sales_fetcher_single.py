import calendar
import datetime
import argparse

from collections import defaultdict
from dateutil.relativedelta import relativedelta
from openpyxl import Workbook

import dretail
from branch import Branch


parser = argparse.ArgumentParser()
parser.add_argument('year', nargs='?', type=int, default=datetime.datetime.today().year)
parser.add_argument('month', nargs='?', type=int, default=datetime.datetime.today().month)
parser.add_argument('day', nargs='?', type=int, default=datetime.datetime.today().day)
args = parser.parse_args()

branch = Branch(
    [8733, 13182, ],
    [16284, 16179, ],
    'SERANG',
    ['582E227AX2XLTOJCDDGAQX84O1CA8C39', '865038d2211cd111b16dd23e39ea342f', ],
    ['5b0c7b868ca031f555e490e9b29fd8de', '6549F75F84PCI8HOCAIWBM2P5E3K070F', ],
    ['a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5', 'b8YFauEf1FfJjVu%2Fx1wHRvYBDnbRS6CKIQBAYUDqyWK0nszbtZMb2HuUILEBZsNHo%2FRZRGOjhaH4LGkj%2BlQlu5Uy55iSOsJOydM45NJlbf2X6RfQG%2Fj2fLc7LeHYlxkp2C0S9A%2F5Rrs7O5%2BxQXWdX41Qmgir6FLKSu%2Bkt4aoVShlRgXAesQHjDPRS3sHSRr3CCQCRz%2BFTyWG1fUTObOMVdcrfmE9Qmfz6Qs6SGOoxsHnOHDenAhDFdY3UdTaCgEsJZ9xbH5vrQR0F3%2FSfYVsm6QkZEQkCuZqaNE8G1tCMC8RDqZGwOK54635aB5jx8ViSH4USbax2cpY9RJ0laC1bKa321gp7Kr%2BE9RMTqp7sw3AJfIhxFzL0evIgmVriCmonqkGN16rJv2yE1aBNDrlvrHjOlDutEEiZMmwx7JVFbM%3Dbfd16832cae10478f51a7e7257ac9c15087e5a93', ],
    0,
    '',
    10,
    3,
    (1000, 1000, 1000, 1000, 1500, 2000, 1500, ),
)

modifiers = {
     ''
      'Hot Chocolate': {
            'Mint': 'Hot Chocolate Mint',
            'Strawberry': 'Hot Chocolate Berry',
      },
      'Iced Chocolate': {
            'Mint': 'Iced Chocolate Mint',
            'Strawberry': 'Iced Chocolate Berry',
      },
      'Iced Chocolate Large': {
            'Mint': 'Iced Chocolate Mint Large',
            'Strawberry': 'Iced Chocolate Berry Large',
      },
      'Pisang': {
            'Keju': 'Pisang Keju',
      },
}

wb = Workbook()
ws = wb.active
ws.title = f'{calendar.month_name[args.month]} {args.year}'

menus = defaultdict(int)

start_time = datetime.datetime(args.year, args.month, args.day, 10, 0, 0)
end_time   = start_time + relativedelta(months=1, day=1, hour=3)

for backoffice in branch.backoffices:
    df_sales_report = dretail.get_laporan_sales_by_item_detail(
        backoffice.branch_id,
        backoffice.company_id,
        start_time.strftime('%d/%m/%Y'),
        start_time.strftime('%H:%M'),
        end_time.strftime('%d/%m/%Y'),
        end_time.strftime('%H:%M'),
        backoffice.get_cookies(),
    )

    for _, row in df_sales_report.iterrows():
        modifier = str(row['Modifier']).rstrip(' 1X')
        item_name = row['Item Name'].rstrip('.')
        
        if item_name in modifiers and modifier in modifiers[item_name]:
                menus[modifiers[item_name][modifier]] += row['Item Sold'] - row['Item Void']
        else:
            menus[item_name] += row['Item Sold'] - row['Item Void']

menu_print_list_foods = [
    'Espresso (Single Shot)',
    'Hot Americano',
    'Iced Americano',
    'Iced Americano Large',
    'Hot Cappuccino',
    'Iced Cappuccino',
    'Iced Cappuccino Large',
    'Hot Cappuccino Butterscotch',
    'Iced Cappuccino Butterscotch',
    'Iced Cappuccino Butterscotch Large',
    'Hot Cappuccino Hazelnut',
    'Iced Cappuccino Hazelnut',
    'Iced Cappuccino Hazelnut Large',
    'Hot Cappuccino Gula Aren',
    'Iced Cappuccino Gula Aren',
    'Iced Cappuccino Gula Aren Large',
    'Hot Latte',
    'Iced Latte',
    'Iced Latte Large',
    'Hot Latte Butterscotch',
    'Iced Latte Butterscotch',
    'Iced Latte Butterscotch Large',
    'Hot Latte Hazelnut',
    'Iced Latte Hazelnut',
    'Iced Latte Hazelnut Large',
    'Coffee Milk Butterscotch',
    'Coffee Milk Butterscotch Large',
    'Coffee Milk Gula Aren',
    'Coffee Milk Gula Aren Large',
    'Coffee Milk Hazelnut',
    'Coffee Milk Hazelnut Large',
    'Con Heiloo',
    'Affogato',
    'Hot Chocolate',
    'Iced Chocolate',
    'Iced Chocolate Large',
    'Iced Chocolate Mint',
    'Iced Chocolate Mint Large',
    'Iced Chocolate Berry',
    'Iced Chocolate Berry Large',
    'Hot Matcha',
    'Iced Matcha',
    'Iced Matcha Large',
    'Iced Red Velvet',
    'Iced Red Velvet Large',
    'Iced Taro',
    'Iced Taro Large',
    'Cocomoon',
    'Mojito',
    'Strawberry Milkshake',
    'Summer Passion',
    'Tropical Berries',
    'Vanilla Regal',
    'Cookies n’ Cream',
    'V60',
    'Japanese',
    'Vietnam Drip',
    'Hot Tea',
    'Iced Tea',
    'Hot Lemon Tea',
    'Iced Lemon Tea',
    'Iced Lemon Tea Large',
    'Lychee Tea',
    'Lychee Tea Large',
    'Thai Tea',
    'Thai Tea Large',
    'Mineral Water',
]
# 
menu_print_list_beverages = [
    'Kentang Sosis',
    'Pisang',
    'Pisang Keju',
    'Tahu Cabai Garam',
    'Classic Burger',
    'Rice Bowl Sambal Matah',
    'Rice Bowl Black Pepper',
    'Rice Bowl Teriyaki',
    'Rice Bowl Yakiniku',
    'Spaghetti Carbonara',
    'Spaghetti Aglio e Olio',
    'Mie Goreng',
    'Mie Kuah',
    'Nasi Goreng',
    'Waffle',
    'Pancake',
]

del menus['TOTAL']
print(menus)

print()
print('Beverages')
for menu in menu_print_list_foods:
    print(menus[menu])
    del menus[menu]

print()
print('Foods')
for menu in menu_print_list_beverages:
    print(menus[menu])
    del menus[menu]

print()
print('Total')
print(sum(menus.values()))
print(menus)