import numpy as np
import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import datetime

app = dash.Dash(__name__)
server = app.server

# ---------------------------------------------------------------
# Taken from https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases
df = pd.read_csv("COVID-19-geographic-disbtribution-worldwide-2020-03-29.csv")

datadf = pd.read_csv("data_covid/data19_12.csv")
# dff_circuits=df_circuits.groupby('country',as_index=False)[['']].sum()

dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths', 'cases']].sum()


cols = ['country', 'year_week','datetime', 'day', 'month', 'year',  'cases', 'deaths', 'cases_weekly_count', 'deaths_weekly_count', 'continent', 'country_code']
lst = []
uniqueValuesCountries = (datadf['country']).unique()
uniqueValuesWeeks = datadf['year_week'].unique()


def getDateRangeFromWeek(p_year, p_week):
    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week) - 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek

def saveChangedDf(datadf):
    for country in uniqueValuesCountries:
        rslt_df_cases = datadf[(datadf['country'] == country) &
                    (datadf['indicator'] == "cases")]

        rslt_df_deaths = datadf[(datadf['country'] == country) &
                     (datadf['indicator'] == "deaths")]

        import datetime
        import time

        for week_data in uniqueValuesWeeks:

            week_elem = week_data

            week_num = week_elem.split('-')[1]
            year_num = week_elem.split('-')[0]
            print(week_elem)

            firstdate, lastdate = getDateRangeFromWeek(str(year_num), str(week_num))

            datetime_elem = firstdate
            day_elem = firstdate.day
            month_elem = firstdate.month
            year_elem  = firstdate.year

            print(day_elem)
            print(month_elem)
            print(year_elem)

            country_elem = country

            rslt_df_cases_week = rslt_df_cases[(rslt_df_cases['year_week'] == week_data)]
            rslt_df_deaths_week = rslt_df_deaths[(rslt_df_deaths['year_week'] == week_data)]

            cases_elem = 0
            deaths_elem = 0

            available_weeks_cases = rslt_df_cases['year_week'].values
            available_weeks_deaths = rslt_df_deaths['year_week'].values

            if week_data in available_weeks_cases :
                cases_elem = rslt_df_cases_week.iloc[0][8]

            if( week_data in available_weeks_deaths):
                deaths_elem = rslt_df_deaths_week.iloc[0][8]

            cases_weekly_count = rslt_df_cases_week['weekly_count'].values
            if cases_weekly_count.size != 0:
                cases_weekly_count = cases_weekly_count[0]

            deaths_weekly_count = rslt_df_deaths_week['weekly_count'].values
            if deaths_weekly_count.size != 0:
                deaths_weekly_count = deaths_weekly_count[0]

            continent_elem = rslt_df_cases_week['continent'].values
            if continent_elem.size != 0:
                continent_elem = continent_elem[0]

            country_code = rslt_df_cases_week['country_code'].values
            if country_code.size != 0:
                country_code = country_code[0]

            print(country)




            lst.append([country_elem, week_elem, datetime_elem, day_elem, month_elem, year_elem, cases_elem, deaths_elem,cases_weekly_count, deaths_weekly_count, continent_elem, country_code])

    changed_df = pd.DataFrame(lst, columns=cols)
    changed_df.to_csv('data_covid_19_12.csv')



#saveChangedDf(datadf)

changed_df = pd.read_csv('data_covid_19_12.csv')

changed_dff = changed_df.groupby('country', as_index=False)[['deaths', 'cases']].sum()



subset_dfdata_cases = datadf[datadf["indicator"] == "cases"]
subset_dfdata_deaths = datadf[datadf["indicator"] == "deaths"]


print("New subset data")
print(subset_dfdata_cases[:5])

print(dff[:5])



# ---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        html.H1('Yet another visualisation of COVID19 cases'),
        html.Div([
            html.P('Illia Kostenko PV251'),
            html.P('All the data was taken from the: ')
        ])
    ]),

    html.Div([
        html.A('Data Source ECDC', href='https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases', target='_blank')]),

    html.Div([
        html.H3('Map of distribution ncov cases per week/year')]),


    html.Div([
        html.Div([
            dcc.Graph(id='map_cases'),
        ]),

    ], className='row'),

    html.Div([
        html.H3('Map of distribution ncov deaths per week/year')]),

    html.Div([
        html.Div([
            dcc.Graph(id='map_deaths'),
        ]),

    ], className='row'),

    html.Div([
        html.H3('Data per each country')]),

    html.Div([
        dash_table.DataTable(

            id='datatable_id',
            data=changed_dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in changed_dff.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            fixed_rows={'headers': True, 'data': 0},
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'countriesAndTerritories'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'deaths'},
                 'width': '30%', 'textAlign': 'left'},
                {'if': {'column_id': 'cases'},
                 'width': '30%', 'textAlign': 'left'},
            ],

            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
        ),
    ], className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='linedropdown',
                         options=[
                             {'label': 'Deaths', 'value': 'deaths'},
                             {'label': 'Cases', 'value': 'cases'}
                         ],
                         value='deaths',

                         ),
        ], className='six columns'),

        html.Div([
            dcc.Dropdown(id='piedropdown',
                         options=[
                             {'label': 'Deaths per week', 'value': 'deaths_weekly_count'},
                             {'label': 'Cases per week', 'value': 'cases_weekly_count'}
                         ],
                         value='cases',

                         ),
        ], className='six columns'),

    ], className='row'),

    html.Div([
        html.Div([
            dcc.Graph(id='linechart'),
        ], className='six columns'),

        html.Div([
            dcc.Graph(id='piechart'),
        ], className='six columns'),




    ], className='row'),



])


# ------------------------------------------------------------------
@app.callback(
    [
     Output('linechart', 'figure'),
     Output('piechart', 'figure'),
     Output('map_cases', 'figure'),
     Output('map_deaths', 'figure'),

     ],


    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('linedropdown', 'value')]
)
def update_data(chosen_rows, piedropval, linedropval):
    subset_dfdata_cases

    if len(chosen_rows) == 0:
        changed_df_filtered = changed_df[changed_df['country'].isin(['China', 'Australia', 'Spain', 'Italy'])]
        df_filterd = dff[dff['countriesAndTerritories'].isin(['China'])]
    else:
        print(chosen_rows)
        changed_df_filtered = changed_dff[changed_dff.index.isin(chosen_rows)]
        df_filterd = dff[dff.index.isin(chosen_rows)]

    list_chosen_countries = changed_df_filtered['country'].tolist()

    subset_dfdata_line = changed_df[changed_df['country'].isin(list_chosen_countries)]

    pie_chart = px.line(
        data_frame=subset_dfdata_line,
        x='datetime',
        y=piedropval,
    template="plotly_dark",
        color='country',
        labels={'country': 'Countries', 'dateRep': 'datetime'},
    )
    pie_chart.update_layout(uirevision='foo')

    # extract list of chosen countries


    line_chart = px.line(
        data_frame=subset_dfdata_line,
        x='datetime',
        y=linedropval,
    template="plotly_dark",
        color='country',
        labels={'country': 'Countries', 'dateRep': 'datetime'},
    )
    line_chart.update_layout(uirevision='foo')

  #  df_test = px.data.gapminder().query("year_week==2021-47")

   # print(df_test['iso_alpha'])
    map_cases = px.scatter_geo(changed_df, locations="country_code", color="continent",
                      hover_name="country", size="cases",
                         template="plotly_dark",
                      projection="natural earth", animation_frame="datetime", )

    map_deaths = px.scatter_geo(changed_df, locations="country_code", color="continent",
                      hover_name="country", size="deaths",
                         template="plotly_dark",
                      projection="natural earth", animation_frame="datetime" )




    return ( line_chart,pie_chart, map_cases, map_deaths)


# ------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
