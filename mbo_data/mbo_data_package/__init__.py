
import pandas

from mbo_data_package.filter_df_remove_fill_cancel_pairs_get_index import filter_df_remove_fill_cancel_pairs_get_index


def filter_df_remove_fill_cancel_pairs(df: pandas.DataFrame):
    '''
    This function removes rows which are Fills followed immediatly by a Cancel.
    The row data much match meaning that both rows are related to the same
    originating event, presumably a Trade event.
    '''
    df_select_index = filter_df_remove_fill_cancel_pairs_get_index(df=df)
    df_orders = df.iloc[list(df_select_index)]
    return df_orders

