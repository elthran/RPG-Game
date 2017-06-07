import csv
import pprint
import inspect
import argparse
import sys
from collections import OrderedDict

from database import EZDB
import prebuilt_objects
import bestiary


database = EZDB('sqlite:///static/database.db', debug=False)


# with open('static/prebuilt_objects.csv', newline='') as f:
    # reader = csv.reader(f)
    # for row in reader:
        # print(row)
        

class Editor:
    """Allow the editing of python data objects and database data from
    CSV files.
    
    Hopefully this same concept can be used to implement an online editor
    using HTML forms and maybe some graphics? Like for Quests? Because I
    think I need a visual editor for them.
    
    Uses argparse see: https://docs.python.org/3.6/howto/argparse.html
    https://docs.python.org/3/library/argparse.html
    
    Uses inspect.signature see:
    https://docs.python.org/3/library/inspect.html#inspect-signature-object
    """
    folder = "static/spreadsheets/"
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Print objects to command line.",
        action='store_true')
    parser.add_argument("-csv", help="Build CSV files.", action='store_true')
    parser.add_argument("-obj", "--objects", help="Return objects.",
        action='store_true')
        
    args = None
    
    def unique(biglist):
        known = set()
        newlist = []

        for element in biglist:
            if element not in known: 
                newlist.append(element)
                known.add(element)
        return newlist
    
    def build_csv():
        """Build all CSV files from database or game modules.
        
        """
        Editor.build_from_bestiary()
        Editor.build_from_prebuilt_objects()
        
    def build_from_prebuilt_objects():
        """Build a CSV file from data in prebuilt_objects.py
        
        Currently only builds abilities.
        
        Problem:
            I need to match a created object with its list of creation
            arguments. So it need a "translation table?" matching a class
            with its list of arguments.
            -This must account for any argument in *args (super class?)
            and **kwargs (super class).
            -Needs to accomodate default arguments.
        """
        filename = Editor.folder + 'prebuilt_objects_abilities.csv'
        with open(filename, 'w', newline='') as csvfile:
            
            #Find out how many objects I am dealing with and what they are.
            objs = Editor.unique([type(item) for item in prebuilt_objects.all_abilities])
            
            #Find out what the class name are for the "Class field"
            #Maybe not needed?
            class_names = [obj.__name__ for obj in objs]
            
            #Map the arguments for each class to itself.
            #These have default arguments which need to be dealt with.
            object_argument_dict = OrderedDict()
            for obj in objs:
                object_argument_dict[obj] = str(inspect.signature(obj)
                    ).strip("()").split(", ")
                    
            # pprint.pprint(object_argument_dict)
            
            #Get all possible arguments as one list (in order).
            #Then remove generic arguments and duplicates.
            fieldnames = []
            for key in object_argument_dict:
                fieldnames += object_argument_dict[key]
            fieldnames = Editor.unique(fieldnames)
            fieldnames.remove("*args")
            fieldnames.remove("**kwargs")
            
            print(fieldnames)
            exit('testing build csv from prebuilt_objects')
            fieldnames = sorted(set(prebuilt_objects.all_abilities[class_names[0]].keys()))
            
            writer = csv.DictWriter(csvfile, fieldnames=["Class"] + fieldnames)
            writer.writeheader()
            for obj in prebuilt_objects.all_abilities:
                row["Class"] = type(obj).__name__
                
                writer.writerow(archtype_row)
        
        if Editor.args.verbose:
            print("Built: {}".format(filename))
        
        
    def build_from_bestiary():
        """Build a CSV file from the data in bestiary.py
        """
        filename = Editor.folder + 'bestiary_archetypes.csv'
        with open(filename , 'w', newline='') as csvfile:
            ids = sorted(bestiary.archetypes.keys())
            fieldnames = sorted(bestiary.archetypes[ids[0]].keys())
            
            writer = csv.DictWriter(csvfile, fieldnames=["ID"] + fieldnames)

            writer.writeheader()
            for key in ids:
                archtype_row = bestiary.archetypes[key]
                archtype_row["ID"] = key
                writer.writerow(archtype_row)
        
        if Editor.args.verbose:
            print("Built: {}".format(filename))

    def build_objects():
        """Build all python object from CSV files.
        """
        return Editor.build_objects_for_bestiary()
        
    def build_objects_for_bestiary():
        """Return recreate objects for bestiary from CSV file.
        """
        archetypes = {}
        with open(Editor.folder + 'bestiary_archetypes.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                key = row["ID"]
                del row["ID"]
                archetypes[key] = row
        
        if Editor.args.verbose:
            pprint.pprint(archetypes)
        return archetypes
        
if __name__ == "__main__":
    #Print help dialogue as default.
    if len(sys.argv) == 1:
        sys.argv.append("-h")
        
    args = Editor.parser.parse_args()
    # print(args)
    Editor.args = args
    
    if args.csv:
        print("CSV files built.")
        Editor.build_csv()
    elif args.objects:
        # Editor.args.verbose = True
        print("Returning objects.")
        Editor.build_objects()