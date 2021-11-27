# contributors: Ramiro Francisco Mejia, Jasmine Ortega, Thomas Siu, Shi Yan Wang
# date: 2021-11-25
# last updated: 2021-11-27

#rm -rf data/processed/
#rm -rf data/raw/
#rm -rf src/figure-preprocess/
#rm -rf src/figure-eda/
#rm src/crime_vancouver_eda.md
#rm src/crime_vancouver_eda.html
#rm -rf results/

# download the data
python src/download_data.py --url=https://geodash.vpd.ca/opendata/crimedata_download/crimedata_csv_all_years.zip?disclaimer=on --file_path=data/raw --zip_file_name=crimedata_csv_all_years.csv

# split the data into train and test
python src/split_data.py --input_path=data/raw/crimedata_csv_all_years.csv --out_path=data/processed/  --graph_path=src/figure-preprocess/

# perform EDA
python src/crime_vancouver_eda.py --input_path=data/processed/training_df.csv --out_dir=src/figure-eda/

# render EDA figures
Rscript -e "rmarkdown::render('src/crime_vancouver_eda.Rmd')"

# create pre-processor for column transformation
python src/pre_process_data.py --out_path=data/processed/

# fit and tune the model
python src/modelling.py --input_path=data/processed/ --out_path=results/

# render final report
Rscript -e "rmarkdown::render('doc/vancouver_crime_predict_report.Rmd')"