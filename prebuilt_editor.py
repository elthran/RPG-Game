import csv
import pprint

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
    """
    
    def build_csv():
        """Build all CSV files from database or game modules.
        
        """
        Editor.build_from_bestiary()
        
    def build_from_bestiary():
        """Build a CSV file from the data in bestiary.py
        """
        with open('static/bestiary_archetypes.csv', 'w', newline='') as csvfile:
            ids = sorted(bestiary.archetypes.keys())
            fieldnames = sorted(bestiary.archetypes[ids[0]].keys())
            
            writer = csv.DictWriter(csvfile, fieldnames=["ID"] + fieldnames)

            writer.writeheader()
            for key in ids:
                archtype_row = bestiary.archetypes[key]
                archtype_row["ID"] = key
                writer.writerow(archtype_row)

    def build_objects():
        """Build all python object from CSV files.
        """
        Editor.build_objects_for_bestiary()
        
    def build_objects_for_bestiary():
        """Return recreate objects for bestiary from CSV file.
        """
        archetypes = {}
        with open('static/bestiary_archetypes.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                key = row["ID"]
                del row["ID"]
                archetypes[key] = row
                
        pprint.pprint(archetypes)
        return archetypes
        
if __name__ == "__main__":
    # Editor.build_csv()
    
    #or 
    Editor.build_objects()