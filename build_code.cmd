@echo off
PUSHD abstraction_lv1
python build_code.py
POPD
REM Second build code engine .. build_code.py(s) are not the same.
REM PUSHD templates\abstraction_lv1
REM python build_code.py
REM POPD
echo Code built!
