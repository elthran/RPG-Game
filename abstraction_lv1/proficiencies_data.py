import pandas


profs = pandas.read_csv('proficiencies.csv', dtype={'Name': str, "Description": str})  #You can declare each column's data type
PROFICIENCY_INFORMATION = []
for i, row in enumerate(profs.itertuples(), 1):
    PROFICIENCY_INFORMATION.append((row.Name, row.Description, row.Attribute, row.GrowthFunction, row.Base, row.Weight, row.Decimals, row.Hidden))