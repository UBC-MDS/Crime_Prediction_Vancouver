#rm -rf data/processed/
#rm -rf data/raw/
#rm -rf src/figure-preprocess/
#rm -rf src/figure-eda/
#rm src/crime_vancouver_eda.md
#rm src/crime_vancouver_eda.html
#rm -rf results/

Rscript -e "rmarkdown::render('README.Rmd')"
python src/download_data.py --url=https://geodash.vpd.ca/opendata/crimedata_download/crimedata_csv_all_years.zip?disclaimer=on --file_path=data/raw --zip_file_name=crimedata_csv_all_years.csv
python src/split_data.py --input_path=data/raw/crimedata_csv_all_years.csv --out_path=data/processed/  --graph_path=src/figure-preprocess/
python src/crime_vancouver_eda.py --input_path=data/processed/training_df.csv --out_dir=src/figure-eda/
Rscript -e "rmarkdown::render('src/crime_vancouver_eda.Rmd')"
python src/pre_process_data.py --out_path=data/processed/
python src/modelling.py --input_path=data/processed/ --out_path=results/
#Rscript -e "rmarkdown::render('doc/vancouver_crime_predict_report.Rmd')"