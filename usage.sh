# python3 parseCM.py input output.csv set_code
# python3 search_occurrence.py seller file1.csv file2.csv > res 2>&1

python3 parseCM.py raviel raviellist.csv
python3 parseCM.py hamon hamonlist.csv CORI
python3 search_occurrence.py seller hamonlist.csv raviellist.csv > res 2>&1