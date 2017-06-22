@echo off
PUSHD data
python build_code.py
POPD
REM Second build code engine .. build_code.py(s) are not the same.
PUSHD templates\abstraction_lv1
python build_code.py
POPD
echo Code built!
