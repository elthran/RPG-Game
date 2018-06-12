import pandas


profs = pandas.read_csv('abilities.csv', dtype={'Name': str, "Description": str})  #You can declare each column's data type
ALL_ABILITIES = []
for i, row in enumerate(profs.itertuples(), 1):
    ALL_ABILITIES.append((row.Name, row.Type, row.Tree, row.TreeType, row.Maximum, row.Description, row.Current, row.Learnable, row.Prof1, row.Value1))
print(ALL_ABILITIES)
