import os,sys
import json
from pathlib import Path
import pandas as pd
global required_cols
def _load_lookup_data(lookup_dir):
    required_cols = ['card_id','card_name','card_number','set_id','set_name','card_market_value']
    all_lookup_df = []
    for file in os.listdir(lookup_dir):
        if file.endswith('.json'):
            filepath = os.path.join(lookup_dir, file)
            print(f"Loading lookup data from {filepath}")
            with open(filepath, 'r', encoding='utf-8') as f: data = json.load(f)
            df=pd.json_normalize(data['data'])
            
            holo_prices = df.get('tcgplayer.prices.holofoil.market', pd.Series([None] * len(df)))
            normal_prices = df.get('tcgplayer.prices.normal.market', pd.Series([None] * len(df)))
            df['card_market_value'] = holo_prices.fillna(normal_prices).fillna(0.0)

            df = df.rename(columns={
    'id': 'card_id',
    'name': 'card_name',
    'number': 'card_number',
    'set.id': 'set_id',
    'set.name': 'set_name'
})

            all_lookup_df.append(df[required_cols].copy())
    if not all_lookup_df:
        print("Look up data is enpty", file=sys.stderr)
        return
    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df.sort_values(by='card_market_value', ascending=False, inplace=True)
    lookup_df.drop_duplicates(subset=['card_id'], keep='first',inplace=True)
    return lookup_df
def _load_inventory_data(inventory_dir):
    inventory_data = []
    all_lookup_df = []
    for inventory_file in inventory_dir.glob('*.csv'):
        data = pd.read_csv(inventory_file)
        inventory_data.append(data)
    if inventory_data is None:
        return
    inventory_df = pd.concat(inventory_data, ignore_index=True)
    inventory_df['card_id'] = inventory_df['set_id'].astype(str)+"-"+inventory_df['card_number'].astype(str)
    return inventory_df
       
import pandas as pd
import sys

def update_portfolio(inventory_dir, lookup_dir, output_file):
    # Load lookup and inventory data
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    # Define required columns
    required_cols = [
        'card_id', 'card_name', 'card_number',
        'set_id', 'set_name', 'card_market_value',
        'binder_name', 'page_number', 'slot_number'
    ]

    # Handle empty inventory
    if inventory_df is None or inventory_df.empty:
        print("No inventory data found", file=sys.stderr)
        inventory_df = pd.DataFrame(columns=required_cols)
        inventory_df.to_csv(output_file, index=False)
        return

    # Merge inventory and lookup on 'card_id', add suffixes to avoid collision
    merged_df = pd.merge(
        inventory_df, lookup_df,
        on='card_id',
        how='left',
        suffixes=('_inv', '_lookup')
    )

    # Resolve final columns using lookup values if available, otherwise inventory
    merged_df['card_name'] = merged_df['card_name_lookup'].combine_first(merged_df['card_name_inv'])
    merged_df['card_number'] = merged_df['card_number_lookup'].combine_first(merged_df['card_number_inv'])
    merged_df['set_id'] = merged_df['set_id_lookup'].combine_first(merged_df['set_id_inv'])
    merged_df['set_name'] = merged_df['set_name'].fillna('NOT_FOUND')
    merged_df['card_market_value'] = merged_df['card_market_value'].fillna(0.0)

    # Create final location index
    merged_df['index'] = (
        merged_df['binder_name'].astype(str) + '_' +
        merged_df['page_number'].astype(str) + '_' +
        merged_df['slot_number'].astype(str)
    )

    # Drop helper columns created by merge
    merged_df.drop(
        columns=[
            'card_name_inv', 'card_name_lookup',
            'card_number_inv', 'card_number_lookup',
            'set_id_inv', 'set_id_lookup'
        ],
        inplace=True
    )


    # Define final columns for output
    final_cols = [
        'card_id', 'card_name', 'card_number',
        'set_id', 'set_name', 'card_market_value',
        'index'
    ]

    # Select final columns
    final_df = merged_df[final_cols]

    # Save to CSV
    final_df.to_csv(output_file, index=False)
    print(f"Portfolio updated and saved to {output_file}")


def main():
    update_portfolio(
        
        inventory_dir=Path('/workspaces/DS-2002-F25/Labs/Lab_04/pokemon_lab/card_inventory/'),
        lookup_dir=Path('/workspaces/DS-2002-F25/Labs/Lab_04/pokemon_lab/card_set_lookup/'),
        output_file='card_portfolio.csv'
    )
def test():
    update_portfolio(
        inventory_dir=Path('/workspaces/DS-2002-F25/Labs/Lab_04/pokemon_lab/card_inventory_test/'),
        lookup_dir=Path('/workspaces/DS-2002-F25/Labs/Lab_04/pokemon_lab/card_set_lookup_test/'),
        output_file='test_card_portfolio.csv'
    )
if __name__ == '__main__':
    print("Starting script in Test Mode")
    test();