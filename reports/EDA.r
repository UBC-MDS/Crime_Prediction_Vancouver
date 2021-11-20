library(tidyverse)

# Relationship between crime and time of day 
df <- read.csv("archive/crime.csv") |>
         select("TYPE", "YEAR", "MONTH", "HOUR", "NEIGHBOURHOOD") |>
        drop_na()
head(df)

crime_hour_plot <- df |>
            ggplot(aes(x = HOUR)) + geom_bar() + ggtitle("All Crime Plotted over Hours of Day")
crime_hour_plot

mean_crime_hour <- df |>
        group_by(TYPE) |>
        summarize(mean_hr =mean(HOUR))
mean_crime_hour

mean_crime_hour_plot <- mean_crime_hour |>
            ggplot(aes(x = mean_hr, y = TYPE)) + geom_point() + xlim(5, 20) +theme_bw(base_size = 15) +
            ggtitle("Crime Type and Mean Hour") + xlab("Mean Hour") +ylab("Crime Type")
mean_crime_hour_plot