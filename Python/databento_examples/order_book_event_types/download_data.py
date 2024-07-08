import databento as db

# First, create a historical client
client = db.Historical("db-5CCaMgGJJgsxw3kQCXkHBcHQwd3HV")

# Next, we will request a minute of mbo data
data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    start="2022-08-26T10:59:00",
    end="2022-08-26T11:00:00",
    symbols="ES.v.0",
    schema="mbo",
    stype_in="continuous",
)

data.to_file('GLBX.MDP3-20220826T105900-220806T110000.mbo.dtn.zst')
data.to_parquet('GLBX.MDP3-20220826T105900-220806T110000.mbo.parquet')
data.to_csv('GLBX.MDP3-20220826T105900-220806T110000.mbo.csv')

df = data.to_df()

# Now, we will inspect the history of a particular order
ORDER_ID = 6410543150678
order_df = df.loc[df["order_id"] == ORDER_ID]

# Finally, we will process each event for this order
print(f"events for order_id: {ORDER_ID}")
for index, row in order_df.iterrows():
    event = (row["price"], row["size"])
    action = row["action"]
    if action == "A":
        # Add action
        print(index, *event, "[A]dded", sep="\t")
    elif action == "C":
        # Cancel action
        print(index, *event, "[C]anceled", sep="\t")
    elif action == "M":
        # Modify action
        print(index, *event, "[M]odified", sep="\t")
    elif action == "R":
        # Book clear action
        print(index, *event, "clea[R]ed", sep="\t")
    elif action == "T":
        # Trade action
        print(index, *event, "[T]raded", sep="\t")
    elif action == "F":
        # Fill action
        print(index, *event, "[F]illed", sep="\t")
