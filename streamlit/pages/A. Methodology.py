import streamlit as st
from pathlib import Path

current_dir = Path(__file__).parent

linear_graph_path = current_dir / "static/images/lineage_graph.png"

image_paths=[
        current_dir / "static/images/bigquery.svg",
        current_dir / "static/images/dbt.png",
        current_dir / "static/images/github.png",
        current_dir / "static/images/pandas.png",
        current_dir / "static/images/plotly.png",
        current_dir / "static/images/Postgresql_elephant.svg.png",
        current_dir / "static/images/Python.png",
        current_dir / "static/images/sql.png",
        current_dir / "static/images/streamlit.png"
    ]



# Page Body
st.title("Methodology")

with st.container():   
    st.divider()
    st.image(
        image=linear_graph_path,
        caption="The lineage graph generated by dbt to generate the metrics from raw wind data"
    )
    
    columns = st.columns(9)
    
    for col, img_path in zip(columns,image_paths):
        with col:
                st.image(img_path,use_column_width=True)
                

with st.container():
    st.write(
    """
        ### Programming Skills and Tools Implmented
        - **Python**: To facilitate streamlit/plotly/pandas
        - **SQL**: The actual transformation code as used in dbt
        - **Google BigQuery**: This is where our data is stored, it is also where the queries are run
        - **Data Build Tool (dbt)**: This is what we used to transform our data systematically 
        - **Streamlit**: This is what we used to build our dashboard and deploy it
        - **Plotly**: This is the graphing library that was used
        - **Pandas**: For minor data manipulation on the streamlit side
        
        A similar implementation can be done using dbt and a **postgres/mysql** instance. 
        This can be locally installed, or hosted on a **docker** container. A postgres 
        implemntation was the first complete iteration of this project
        
        In addition, the first implementation also used Vizro to create the dashboard.
        This was replaced with streamlit **due to the author not knowing how to deploy it**. 
        
        
        ### Software Engineering Best Practices Implemented
        
        The following were implemented to build proficiency in these practices:
        
        - A **virtual environment** was used to have a stable, reproducible, and portable environment
        - **Version Control** was applied using Git and Github via the VSCode interface
        - A **git workflow**/code review and collaboration system was applied due to it being a dbt cloud requirement
        - Testing and validation was done at some of the dbt models using in-build methods
        - Documentation of the dbt process was done using `dbt docs generate` and hosted on **github pages**
        - Modularity and reusability. This entire project can be applied to any other 
        wind site to do resource assessment.
    """
    )
    
    st.write(
        """ 
            ### Wind Resource Assessment Skills and Domain Knowledge
            
            A staging model was first built in dbt to remove null values, and to cast 
            the data types as appropriate for analysis later on. 
            
            Following this, a feature engineering model was done on the raw or hourly
            aggregated data
            
        """
    )
    
    st.code(
        """ 
            with
            source_data as (
                
                select
                    datetime as date_time,
                    windspeed as wind_speed,
                    gustspeed as gust_speed,
                    winddirection as wind_direction

                from {{ source("raw", "upd_wind") }}
            ),

            cleaned_data as (
                
                select * from source_data

                where
                    wind_speed is not null
                    and gust_speed is not null
                    and wind_direction is not null
            ),

            casted_data as (
                
                select
                    parse_timestamp('%m/%d/%y %H:%M', date_time) as date_time,
                    cast(wind_speed as float64) as wind_speed,
                    cast(gust_speed as float64) as gust_speed,
                    cast(wind_direction as float64) as wind_direction

                from cleaned_data
                order by 1
            )

            select *
            from casted_data
        """,
    language="sql"
    )
    
    st.code(
        """ 
            with
            stg_wind as (

                select date_time, wind_speed, wind_direction from {{ ref("stg_wind") }}

            ),

            date_time_features as (

                select
                    extract(year from date_time) as years,
                    extract(month from date_time) as months,
                    format_timestamp('%Y-%B', date_time) as year_month,
                    extract(day from date_time) as days,
                    extract(hour from date_time) + 1 as hours,

                    wind_speed,
                    wind_direction

                from stg_wind

                order by 1, 2, 4, 5
            )

            select *
            from date_time_features
        """,
        language="sql"
    )
    
    st.code(
        """ 
            with
            feature_wind as (select * from {{ ref("feature_wind") }}),

            feature_wind_hourly as (

                select
                    years,
                    months,
                    year_month,
                    days,
                    hours,

                    round(avg(wind_speed), 4) as avg_wind_speed,
                    round(avg(wind_direction), 4) as avg_wind_direction

                from feature_wind

                group by 1, 2, 3, 4, 5

                order by 1, 2, 3, 4, 5
            )

            select *
            from feature_wind_hourly  
        """,
        language="sql"
    )
    
    st.write(
        """ 
            #### Data Availability
            Counted and aggregated the number of unique days 
            per month with a non-null wind record
        """
    )
    
    st.code(
        """ 
            with
            feature_wind as (select * from {{ ref("feature_wind") }}),

            data_availability as (
                select years, months, year_month, count(distinct days) as count_days

                from feature_wind

                group by 1, 2, 3

                order by 1, 2, 3
            )

            select *
            from data_availability
        """,
        language="sql"
    )
    
    st.write(
        """ 
            #### Diurnal Variation
            Aggregated wind speeds per hour on a daily, monthly, 
            and yearly basis       
        """
    )
    
    st.code(
        """ 
            with
            feature_wind_hourly as (select * from {{ ref("feature_wind_hourly") }}),
            
            diurnal_daily as (

                select
                    years,
                    months,
                    year_month,
                    days,
                    hours,

                    round(avg_wind_speed, 3) as avg_wind_speed

                from feature_wind_hourly

                order by 1, 2, 3, 4, 5
            )

            select *
            from diurnal_daily
        """,
        language="sql"
    )
    
    st.write(
        """ 
            #### Wind Rose Diagram
            Bins were created for both wind speed and wind direction. Then the count of 
            wind records that fell into each were counted. The cumulative count in each 
            wind direction bin was then done on a daily, monthly, and yearly basis
        """
    )
    
    st.code(
        """ 
            with
            cardinal_directions_hourly as (
                select * from {{ ref("cardinal_directions_hourly") }}
            ),

            frequency as (
                select
                    years,
                    months,
                    year_month,
                    days,
                    cardinal_direction,
                    speed_bin,

                    count(*) as count_freq

                from cardinal_directions_hourly

                group by 1, 2, 3, 4, 5, 6
            ),

            total_frequency as (
                select years, months, year_month, days, count(*) as count_total

                from cardinal_directions_hourly

                group by 1, 2, 3, 4
            ),

            percent_frequency as (
                select
                    years,
                    months,
                    year_month,
                    days,
                    cardinal_direction,
                    speed_bin,
                    count_freq,
                    count_total,

                    case
                        when count_total > 0
                        then round((count_freq * 100) / count_total, 3)
                        else 0
                    end as perc_freq

                from frequency

                join total_frequency using (years, months, year_month, days)
            ),

            cumulative_frequency as (
                select
                    years,
                    months,
                    year_month,
                    days,
                    cardinal_direction,
                    speed_bin,
                    count_freq,
                    count_total,
                    perc_freq,

                    round(
                        sum(perc_freq) over (
                            partition by years, months, year_month, days, cardinal_direction
                            order by speed_bin
                            rows between unbounded preceding and current row
                        ),
                        3
                    ) as cumulative_perc_freq

                from percent_frequency

                order by 1, 2, 3, 4, 5, 6
            )

            select *
            from cumulative_frequency
        """,
        language="sql"
    )
    
    st.write(
        """ 
            #### Frequency Distribution
            Bins were created for wind speeds. Then the count of wind records
            that fell into each bin was recorded
        """
    )    
    
    st.code(
        """ 
            with
            binned_speed as (select * from {{ ref("binned_speed") }}),

            monthly_counts as (

                select
                    years,
                    months,
                    year_month,
                    speed_bin,

                    count(*) as frequency,

                    sum(count(*)) over (partition by years, months) as monthly_total

                from binned_speed

                group by 1, 2, 3, 4
            ),

            frequency_distribution_monthly as (

                select
                    years,
                    months,
                    year_month,
                    speed_bin,
                    frequency,
                    round((frequency / monthly_total) * 100, 3) as percent_frequency

                from monthly_counts

                order by 1, 2, 3, 4
            )

            select *
            from frequency_distribution_monthly
        """,
        language="sql"
    )
    
    st.write(
        """ 
            #### Statistics
            The basic statistics were computed using SQL syntax
        """
    )
    
    st.code(
        """ 
            with 
            feature_wind as (select * from {{ ref("feature_wind") }}),

            monthly_stats as (
                select
                    years,
                    months,
                    year_month,

                    max(wind_speed) as max_speed,
                    min(wind_speed) as min_speed,
                    round(avg(wind_speed), 3) as avg_speed

                from feature_wind

                group by 1, 2, 3
                order by 1, 2, 3
            )

            select * from monthly_stats      
        """,
        language="sql"
    )
    
    
    
    st.write(
        """ 
            #### Weibull function (Wind Speed Distribution)
            Using the average wind speed at the turbine (calculated via wind shear) 
            and the wind speed increments of the representative 
        """
    )
    
    st.latex(
        r"""
        f(v) = \frac {\pi v}{2{(v_m)}^2} exp (\frac{\pi}{4}) (\frac{v}{v_m})^2
        """
    )
    
    st.code(
        """ 
            with
            delta_wind_height as (select * from {{ ref("delta_wind_height") }}),

            turbine_power_curve as (
                select
                    num as speed_at_turbine,
                    case
                        when num < 5
                        then 0
                        when num = 5
                        then 5
                        when num = 5.5
                        then 8
                        when num = 6
                        then 13
                        when num = 6.5
                        then 19
                        when num = 7
                        then 26
                        when num = 7.5
                        then 32
                        when num = 8
                        then 39
                        when num = 8.5
                        then 46
                        when num = 9
                        then 53
                        when num = 9.5
                        then 59
                        when num = 10
                        then 65
                        when num = 10.5
                        then 71
                        when num = 11
                        then 76
                        when num = 11.5
                        then 80
                        when num = 12
                        then 84
                        when num = 12.5
                        then 88
                        when num = 13
                        then 92
                        when num = 13.5
                        then 95
                        when num = 14
                        then 97
                        when num = 14.5
                        then 100
                        when num = 15
                        then 102
                        when num = 15.5
                        then 104
                        when num = 16
                        then 105
                        when num = 16.5
                        then 107
                        when num = 17
                        then 108
                        when num between 17.5 and 20.5
                        then 109
                        when num between 21 and 21.5
                        then 108
                        when num = 22
                        then 107
                        when num = 22.5
                        then 106
                        when num = 23
                        then 105
                        when num = 23.5
                        then 104
                        when num = 24
                        then 103
                        when num between 24.5 and 25
                        then 102
                    end as power_curve
                from (
                    {# Sub-query to generate the array 0-25 in 0.5 increments #}
                    {# generate_array creates the array with from min to max, with step-wise function #}
                    {# unnest returns a table with #}
                    select num 

                    from unnest(generate_array(0,25,0.5)) as num
                )
            ),

            combined_data as (
                select
                    years,
                    months,
                    year_month,
                    wind_shear,
                    speed_at_turbine,
                    power_curve

                from delta_wind_height as dwh

                cross join turbine_power_curve

                order by 1,2,3,4,5
            ),

            weibull as (
                select
                    years,
                    months,
                    year_month,
                    wind_shear,
                    speed_at_turbine,
                    power_curve,

                    case
                        when wind_shear > 0 then
                            ((acos(-1) * speed_at_turbine) / (2 * power(wind_shear,2)) * exp((-acos(-1) / 4) * power(speed_at_turbine / wind_shear,2)))
                        else 0
                    end as f_v

                from combined_data

            )

            select * from weibull
        """,
        language="sql"
    )
    
    st.write(
        """ 
            #### Periodic Energy Production
            The sum of the Weibull function and the powercurve multiplied
            by the amount of hours under consideration
        """
    )
    
    st.latex(
        r""" 
            YEY(v_m) = \sum_{v=1}^{25} f(v)P(v)24
        """
    )
    
    st.latex(
        r""" 
            YEY(v_m) = \sum_{v=1}^{25} f(v)P(v)8760
        """
    )

    st.code(
        """ 
            with 
            weibull as (select * from {{ ref('weibull') }}),

            yey as (
                select  
                    years,
                    months,
                    year_month,
                    f_v,
                    power_curve,
                    f_v * power_curve * 24 as daily_yey_per_month,
                    f_v * power_curve * 8760 as yearly_yey_per_month

                from weibull
            ),

            sum_yey as (
                select
                    years,
                    months,
                    year_month,
                    round(sum(daily_yey_per_month),3) as sum_yey_daily,
                    round(sum(yearly_yey_per_month),3) as sum_yey_yearly

                from yey

                group by 1,2,3

                order by 1,2,3
            )

            select *
            from sum_yey
        
        """
    )


