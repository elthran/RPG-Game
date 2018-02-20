# Import up one level import of package ...
# because I cannot grok relative import :P
import sys
old_path = sys.path[0].split('\\')
new_path = '\\'.join(old_path[:-1])
# -1 refers to how many levels of directory to go up
sys.path.insert(0, new_path)
import build_code
sys.path.pop(0)

if __name__ == "__main__":
    # This should be an automatic function! Not manual.
    # names = ["attributes", "proficiencies", "abilities"]
    names = ["proficiencies", "abilities"]
    build_code.build_templates(names, '.py')
