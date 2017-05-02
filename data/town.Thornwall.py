default = "default" #or some kind of shortcut anyways.

shops = {"Blacksmith": "Gerald's Ironworks", "Barracks": default, "Marketplace": default}

other = {"Tavern": default, "Old Man's Hut": "Home of Master Wenzdar"}

outskirts = {"Village Gate": default}

"""
## v.03
Hopefully at some point I could build a location "editor" that would automate the process of creating
and editing python dictionary objects or a simple way to put the same data in a database like
a point and click and type html form or something.

## v.02
If the blacksmith is a generic blacksmith it would then load all items for the generic blacksmith
class. If it was custom to this town it could load town.Thornwall.Gerald's Ironworks(a.k.a the Thornwall blacksmith shop.)

## v.01
A Python comment ...

Maybe this file should even be a python module?
In theory it should tell the main program that when you create a Town(class) named
"Thornwall" it should load Thornwall.txt and when it loads this file it will
know that Thornwall has 3 shops named "Blacksmith", "Barracks" and "Marketplace".
These shops should have generic Shop(class) code with specific data for Thornwall
defined here?

Eg.
Blacksmith
--Item1
--Item2
--Item3

Where each item could be looked up in a database or a similar file for items?
God this would be so much better as a database.
"""