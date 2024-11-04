import requests
import time
import pandas as pd
from datetime import datetime

# Data
prob = {'blue':0.80128, 'purple':0.16026, 'pink':0.03205, 'red':0.00641}
missing_link_charm_items = {'red': ['968349','968241'], 'pink':['968019','968301','968223'],
                            'purple':['968239','968192','968154','968248','968182','968172'],
                            'blue':['967978','968129','968012','967999','967946','967985']}

small_arms_charm_items = {'red': ['968232','968238'], 'pink':['968270','968082','968284'],
                            'purple':['968112','968115','968026','968131','968221'],
                            'blue':['968062','968091','967979','968162','967983','968153']}

elemental_craft_stickers_items = {'red': ['967964','968350'], 'pink':['967958','967989','968234','968070'],
                            'purple':['967959','967962','968016','967956','967970'],
                            'blue':['967974','967967','967945','967948','967966','967944',
                                    '967950','967940','968042','967949','967951','968006',
                                    '967935','967952','967965']}

character_craft_stickers_items = {'red': ['968132','968331'], 'pink':['968194','968171','968299'],
                            'purple':['968001', '967947','967986','968020','968087'],
                            'blue':['968014','967936','968027','967972','968011','968065',
                                    '968128','968031','968045','967943','967988','967976',
                                    '967971','968076','967997']}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Calculate return
def calculate_expectation(items, stars_per_collection=1):
    expected_income = 0
    for key, value in items.items():
        for id in value:
            url = f'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={id}&page_num=1&sort_by=default'
            for attempt in range(3):
                try:
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        if data['data']['items']:
                            price = data['data']['items'][0]['price']
                            expected_income += prob[key] * float(price) / len(value)
                        else:
                            print(f"No items found for goods_id {id}")
                        break
                    else:
                        print(f"Failed to retrieve data for item {id}: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed for item {id}: {e}")
                time.sleep(5)
            else:
                print(f"Failed to retrieve data for item {id} after 3 attempts.")

            time.sleep(1)
    expected_income /= stars_per_collection  # 按开箱所需星数修正回报
    return round(expected_income, 2)

collections = {
    "Missing Link Charm Items": missing_link_charm_items,
    "Small Arms Charm Items": small_arms_charm_items,
    "Elemental Craft Stickers Items": elemental_craft_stickers_items,
    "Character Craft Stickers Items": character_craft_stickers_items
}

results = []
for collection_name, items in collections.items():
    # 挂链需要3颗星
    stars_per_collection = 3 if "Charm" in collection_name else 1

    expectation = calculate_expectation(items, stars_per_collection)
    results.append(expectation)
    print(f"Expectation for {collection_name}: {expectation}")

# write to file
df = pd.DataFrame({
    'Time': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    'Missing Link Charm Items': [results[0]],
    'Small Arms Charm Items': [results[1]],
    'Elemental Craft Stickers Items': [results[2]],
    'Character Craft Stickers Items': [results[3]]
})

file_path = 'result.csv'
df.to_csv(file_path, mode='a', index=False, header=not pd.io.common.file_exists(file_path))
print(f"Results written to {file_path}")


