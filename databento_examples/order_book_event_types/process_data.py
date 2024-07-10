import databento
import pandas

pandas.set_option('display.max_rows', 500)
#pandas.set_option('display.min_rows', 20)

data = databento.DBNStore.from_file('GLBX.MDP3-20220826T105900-220806T110000.mbo.dtn.zst')
df = data.to_df().reset_index()

# Now, we will inspect the history of a particular order
ORDER_ID = 6410543150678
order_df = df.loc[df["order_id"] == ORDER_ID]

print(order_df)
# 1009
# 1478

#print(df.loc[1009:1478])
df.loc[1009:1478].to_csv('GLBX.MDP3-selected.csv')

# # Finally, we will process each event for this order
# print(f"events for order_id: {ORDER_ID}")
# for index, row in order_df.iterrows():
#     event = (row["price"], row["size"])
#     action = row["action"]
#     if action == "A":
#         # Add action
#         print(index, *event, "[A]dded", sep="\t")
#     elif action == "C":
#         # Cancel action
#         print(index, *event, "[C]anceled", sep="\t")
#     elif action == "M":
#         # Modify action
#         print(index, *event, "[M]odified", sep="\t")
#     elif action == "R":
#         # Book clear action
#         print(index, *event, "clea[R]ed", sep="\t")
#     elif action == "T":
#         # Trade action
#         print(index, *event, "[T]raded", sep="\t")
#     elif action == "F":
#         # Fill action
#         print(index, *event, "[F]illed", sep="\t")

'''
It seems like a Fill followed by a Modify is the normal way to update the book
when there is still some volume remaining after the fill.

Whereas, Fill followed by Cancel is the normal way to update the book when there
is no volume remaining after the fill.

(At least for the CLBX.MDP3 dataset.)

Not the case for Nasdaq.
'''