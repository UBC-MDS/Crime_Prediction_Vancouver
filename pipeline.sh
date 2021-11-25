rm -rf data/processed/
rm -rf data/raw/

python src/download_data.py --url=https://geodash.vpd.ca/opendata/crimedata_download/crimedata_csv_all_years.zip?disclaimer=on --file_path=data/raw --zip_file_name=crimedata_csv_all_years.csv
python src/split_data.py --input_path=data/raw/crimedata_csv_all_years.csv --out_path=data/processed/
python src/pre_process_data.py --out_path=data/processed/