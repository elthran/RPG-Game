"""
Name, Description, Attribute_Type, Type, [(Values Name, Value type,
    (Modifiers of value), Decimal Places)]
Linear: (Level multiplier), (Starting Value)
Root: Not finished. Looks like square root function. Used for diminishing
    returns and things that get better the larger they are. (Starting value)
    [Currently approaches 100]

Curvy: (larger "0" means it reaches the cap quicker) (smaller [1] means it
    reaxhes the cap quicker) ([2] is the cap or maximum possible value)
    ([3] is the negative amount)
Sensitive: Like curvy but has decimals (larger [0] means it reaches the cap
    quicker) (smaller [1] means it reaches the cap quicker) ([2] is the cap
    or maximum possible value) ([3] is the negative amount)
Modifier: (larger [0] means greater amplitude), (larger [1] means greater
    steepness and faster increase), (greater [2]  means greater frequency of
    waves)
Percent: ???
Empty: Sets this value to take on the value of "maximum". Must be placed after
    "Maximum" in the list of variables
"""

"""
Prof_Name, Prof_Descr, Prof_Attrib, [Formula_Type, Base_Value, Weight, # of Decimals], hidden_boolean, percent_boolean
"""

import pandas


profs = pandas.read_csv('profs.csv', dtype={'Name': str, "Description": str})
PROFICIENCY_INFORMATION = []
for i, row in enumerate(profs.itertuples(), 1):
    PROFICIENCY_INFORMATION.append((row.Name, row.Description, row.Attribute, row.GrowthFunction, row.Base, row.Weight, row.Decimals, row.Hidden))
