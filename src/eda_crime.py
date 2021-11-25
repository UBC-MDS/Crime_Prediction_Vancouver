# author: Group 24
# date: 2021-11-25

''' Creates eda plots for the pre-processed training data from the Crime Vancouver Data 
    (from https://geodash.vpd.ca/opendata/) and saves the plots as a pdf and png files

Usage: src/eda_crime.py --input_path=<input_path> --out_dir=<out_dir>
  
Options:
--input_path=<train_path>     Path (including filename) to training data (which needs to be saved as a .csv file)
--out_dir=<out_dir>           Path to directory where the plots should be saved
'''

import altair as alt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
alt.data_transformers.enable('data_server')
alt.renderers.enable('mimetype')
from fpdf import FPDF
from docopt import docopt

opt = docopt(__doc__)

def main(input_path, out_dir):
    
    # Read data from csv and get the train data
    df = pd.read_csv(input_path)
    df = df.query('2010 < YEAR <= 2020')
    train_df, test_df = train_test_split(df, test_size=0.20, random_state=123)

    # Add PDF Object
    pdf = FPDF()
    
    # Use train_df to explore trends and relationships
    # Type of crimes
    crime_type = alt.Chart(train_df, title='Crimes in Vancouver in the past 10 years').mark_bar().encode(
                    y=alt.Y('TYPE', sort='-x', title='Type of Crime'),
                    x=alt.X('count()', title='Number of Crimes'))

    crime_type.save('crime_type.png')
    pdf.add_page()
    pdf.image('crime_type.png', 10, 10, 180)

    # Relationship between neighbourhoods and type of crimes
    crime_correlation = alt.Chart(train_df.dropna(), title = "Relationships between neighbourhoods and type of crimes"
        ).mark_square().encode(
            x='TYPE',
            y='NEIGHBOURHOOD',
            color='count()',
            size='count()').properties(
            width=500,
            height=350
    )

    crime_correlation.save('crime_correlation.png')
    pdf.add_page()
    pdf.image('crime_correlation.png', 10, 10, 180)

    # Top 5 neighbourhoods with most reported crimes
    top5 = train_df.groupby(['NEIGHBOURHOOD']).count().sort_values(by=['TYPE'], ascending=False).reset_index().head()
    
    crime_top5 = alt.Chart(top5, title = "Top 5 Neighbourhoods with most crimes").mark_bar().encode(
         x=alt.X('NEIGHBOURHOOD', sort=alt.EncodingSortField(field='TYPE', op='count',order='descending')),
         y=alt.Y('TYPE')).properties(width=200)
    
    crime_top5.save(str(out_dir) + 'crime_top5.png')
    pdf.add_page()
    pdf.image(str(out_dir) + 'crime_top5.png')

    # Evolution of crimes in Vancouver
    crime_evolution = alt.Chart(train_df, title ='Evolution of Crimes in Vancouver').mark_line().encode(
        x=alt.X('YEAR'),
        y=alt.Y('count(YEAR)', title ='Number of Crimes'),
        color=alt.Color('TYPE', title='Type of Crime'))

    crime_evolution.save('crime_evolution.png')
    pdf.add_page()
    pdf.image('crime_evolution.png', 10, 10, 180)
    
    # Export plots to PDF
    pdf.output('src/eda_crime.pdf', 'F')


if __name__ == "__main__":
    main(opt['--input_path'], opt['--out_dir'])
