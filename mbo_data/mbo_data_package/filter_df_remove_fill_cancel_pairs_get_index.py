
import pandas

from mbo_data_package.compare_rows import compare_rows


def filter_df_remove_fill_cancel_pairs_get_index(df: pandas.DataFrame):

    '''
    This function iterates through the rows of a dataframe and finds all rows
    where there is a Fill followed by a Cancel where all the relevant data in
    the columns matches. (Meaning that the Fill and Cancel are releated to the
    same event.)

    Rows which match this criteria have their index added to a set which is used
    to deselect the rows with these index values.
    '''

    # set of index not selected
    df_not_select_index = set()
    # set of index selected
    df_select_index = set()
    # all observed index
    df_all_index = set()

    last_row = None
    last_row_index = None

    for index, row in df.iterrows():
        df_all_index.add(index)
        #print(f'index={index}')

        # if index > 208176 + 5:
        #     break

        if last_row is not None:
            if not compare_rows(index, last_row, row):
                pass
                #print(f'rows do not match')
                #print(last_row)
                #print(row)
            else:
                #print(f'rows match')
                # print(last_row)
                # print(row)
                #print(df.iloc[last_row_index:index+1])
                #break

                df_not_select_index.add(last_row_index)
                df_not_select_index.add(index)

                last_row = None
                last_row_index = None

                continue

        last_row = row
        last_row_index = index


    # print(len(df_not_select_index))
    # print(len(df_all_index))
    df_select_index = df_all_index - df_not_select_index
    # print(len(df_select_index))

    return df_select_index
