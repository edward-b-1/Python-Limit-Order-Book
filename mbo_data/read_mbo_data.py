#!/usr/bin/env python3


import pandas
import databento
import jsons


def get_path(ticker, filename=None):
    #return f'/databento/data/cme-futures/{ticker}/...'
    ticker = 'nvda'
    #filename = 'xnas-itch-20240105.mbo.dbn.zst'
    return f'/databento/data/mbo/{ticker}/XNAS-20240622-WPPRESG4BH/{filename}'


def main():

    ticker = 'nvda'
    filenames_to_load = []

    with open(f'/databento/data/mbo/{ticker}/XNAS-20240622-WPPRESG4BH/manifest.json') as f:
        d = jsons.loads(f.read())
        
        files = d['files']
        for file in files:
            filename = file['filename']
            if '.zst' in filename:
                filenames_to_load.append(filename)

    filenames_to_load.sort()

    for filename in filenames_to_load:
        path = get_path(ticker='nvda', filename=filename)
        stored_data = databento.DBNStore.from_file(path)
        df = stored_data.to_df()

        #print(df.head())
        #print(df.columns)
        if filename == filenames_to_load[0]:
            print(df.dtypes)
        print(df['action'].unique())
        print((df['flags'] & databento.RecordFlags.F_LAST).unique())
        #print(df['side'].unique())
        #print(df['instrument_id'].unique())


if __name__ == '__main__':
    main()

