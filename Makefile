# crime predictor vancouver data pipe
# author: Thomas Siu
# date: 2021-12-03

# Usage: Make all
# Creates the EDA report and final analysis report through checking all dependencies
all: src/crime_vancouver_eda.md doc/vancouver_crime_predict_report.md

# Usage: Make data/raw/crimedata_csv_all_years.csv
# Downloads the necessary crime data from Vancouver Police Department and extract the zip file
data/raw/crimedata_csv_all_years.csv: src/download_data.py
	python src/download_data.py --url=https://geodash.vpd.ca/opendata/crimedata_download/crimedata_csv_all_years.zip?disclaimer=on --file_path=data/raw --zip_file_name=crimedata_csv_all_years.csv

# Usage: Make data/processed/training_feature.csv
# Date range can be specified in the script "python src/..." with from_year and to_year parameter.
# Splits the data into train and test, and generate necessary graphs for final report
data/processed/training_feature.csv \
data/processed/training_target.csv \
data/processed/test_feature.csv \
data/processed/test_target.csv \
data/processed/training_df.csv \
src/figure-preprocess/data_before_balance.png \
src/figure-preprocess/data_after_balance.png \
src/figure-preprocess/observations.png: src/split_data.py data/raw/crimedata_csv_all_years.csv
	python src/split_data.py --input_path=data/raw/crimedata_csv_all_years.csv --out_path=data/processed/  --graph_path=src/figure-preprocess/ --from_year=2016 --to_year=2020

# Usage: Make src/figure-eda/neighbour_crimes.png
# Performs EDA and generates necessary graphs and tables
src/figure-eda/neighbour_crimes.png \
src/figure-eda/crime_type.png \
src/figure-eda/crime_evolution.png \
src/figure-eda/crime_correlation.png \
src/figure-eda/crime_top5.png: src/crime_vancouver_eda.py data/processed/training_df.csv
	python src/crime_vancouver_eda.py --input_path=data/processed/training_df.csv --out_dir=src/figure-eda/ 

# Usage: Make src/crime_vancouver_eda.md
# Render EDA report
src/crime_vancouver_eda.md: src/crime_vancouver_eda.Rmd src/figure-eda/neighbour_crimes.png src/figure-preprocess/observations.png src/figure-eda/crime_type.png src/figure-eda/crime_evolution.png src/figure-eda/crime_correlation.png src/figure-eda/crime_top5.png
	Rscript -e "rmarkdown::render('src/crime_vancouver_eda.Rmd')"

# Usage: Make data/processed/models.p
# create pre-processor for column transformation
data/processed/preprocessor.p data/processed/models.p: src/pre_process_data.py
	python src/pre_process_data.py --out_path=data/processed/

# Usage: Make results/pipe_best.p
# Fit and tune model
results/pipe_best.p \
results/models_results_cv.png \
results/best_LR_model.png \
results/confusion_matrix.png \
esults/classification_report.png: src/modelling.py \
data/processed/training_feature.csv \
data/processed/training_target.csv \
data/processed/test_feature.csv \
data/processed/test_target.csv \
data/processed/models.p \
data/processed/preprocessor.p
	python src/modelling.py --input_path=data/processed/ --out_path=results/

# Usage: Make doc/vancouver_crime_predict_report.md
# render report
doc/vancouver_crime_predict_report.md: \
doc/vancouver_crime_predict_report.Rmd \
doc/references.bib src/figure-eda/crime_correlation.png \
src/figure-eda/crime_top5.png src/figure-preprocess/data_before_balance.png \
src/figure-preprocess/data_after_balance.png \
results/models_results_cv.png \
results/best_LR_model.png \
results/confusion_matrix.png \
results/classification_report.png
	Rscript -e "rmarkdown::render('doc/vancouver_crime_predict_report.Rmd')"

# Usage: Make clean
# remove all necessary files for a fresh start of analysis
clean: 
	rm -rf data/processed
	rm -rf data/raw/crimedata_csv_all_years.csv
	rm -rf results
	rm -rf src/figure-eda src/figure-preprocess
	rm -rf src/crime_vancouver_eda.md src/crime_vancouver_eda.html	
	rm -rf doc/vancouver_crime_predict_report.md doc/vancouver_crime_predict_report.html