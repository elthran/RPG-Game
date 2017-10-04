I would like to suggest/request that we default to "Human readable" (a.k.a. random capitalization) as the default format for all data and then use a standard module to convert the default data format into some common forms such as ClassName or variable_name.

An example of this (an why) is as follows:
    "Resist poison" (Human readable/default, spaces + capitalize first - this format is hard to generate programatically as it requires a complex understanding of what kind of syntax is best suited to various situations)
    "ResistPoison" (ClassName - simple to convert to from Human readable with `var.title().replace(" ", '')`)
    "resist_poinson" (variable_name - simple to convert to from Human readable with `var.lower().replace(" ", "_")`)
    
The alternatives/alternate defaults up for discussion:
1.
    "ResistPoison" (use ClassName as the default)
        - how do I convert this to human readable?
        - how do I convert this from "variable_name"?
2.
    "Resist Poison" (capitalize all words, keep spaces)
        - maybe just fine?
        - usage in a sentance might be best?
        
I am developing a function (which might become a class) in 'factories.py' currently called 'normalize_naming' that accepts a list (currently, though should be a string with a separte list version :P) and a "scheme" that you want to convert to.

I believe that having a standard way of describing data with help me avoid the hard to detect "capitialization bug" that requires hours of print statement/manual debugging.
    
