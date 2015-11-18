rm pytw.sqlite3
./src/recreate_tables.py
./src/import_worlds.py
mv import/reports-imported/*.htm* import/reports/ #TODO no overwrite, no fail on empty
#TODO auto-import old reports
