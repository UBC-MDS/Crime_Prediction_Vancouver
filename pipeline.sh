# contributors: Ramiro Francisco Mejia, Jasmine Ortega, Thomas Siu, Shi Yan Wang
# date: 2021-11-25
# last updated: 2021-12-09

# download the data
python src/scripts/download_data.py --url=https://geodash.vpd.ca/opendata/crimedata_download/crimedata_csv_all_years.zip?disclaimer=on --file_path=data/raw --zip_file_name=crimedata_csv_all_years.csv

# split the data into train and test
python src/scripts/split_data.py --input_path=data/raw/crimedata_csv_all_years.csv --out_path=data/processed/  --graph_path=src/figure-preprocess/ --from_year=2016 --to_year=2020

# perform EDA
python src/scripts/eda_script.py --input_path=data/processed/training_df.csv --out_dir=src/figure-eda/

# render EDA report
Rscript -e "rmarkdown::render('src/report-eda/crime_vancouver_eda.Rmd')"

# create pre-processor for column transformation
python src/scripts/pre_process_data.py --out_path=data/processed/

# fit and tune the model
python src/scripts/modelling.py --input_path=data/processed/ --out_path=results/

# render final report
Rscript -e "rmarkdown::render('doc/vancouver_crime_predict_report.Rmd')"