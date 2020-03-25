# Author    -   Hasan s
# Email     -   hasan@jaaga.in
# Site      -   https://curious.af/

import streamlit as st
import pandas as pd
import altair as alt


option = st.sidebar.radio(
    'Dataset',
     ['Mortality Factors', 'Geographical Data'])

if option == 'Geographical Data':

    @st.cache
    def get_cases_data():
        cases = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        return cases

    @st.cache
    def get_deaths_data():
        deaths = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
        return deaths

    @st.cache
    def turn_df_timeseries_format(df):
        df_grouped = df.groupby('Country/Region').sum().reset_index()
        df_shaped = df_grouped.drop(['Lat', 'Long'], axis=1).melt(id_vars=['Country/Region'])
        df_shaped.rename(columns = {'variable':'Date', 'value':'Cases'}, inplace = True) 
        df_shaped['Date'] = pd.to_datetime(df_shaped['Date'])
        return df_shaped

    cases = get_cases_data()
    deaths = get_deaths_data()

    cases_timeseries = turn_df_timeseries_format(cases)
    deaths_timeseries = turn_df_timeseries_format(deaths)

    selected_countries = st.multiselect('Countries', list(set(cases['Country/Region'])))
    if selected_countries:
        cases_timeseries = cases_timeseries[cases_timeseries['Country/Region'].isin(selected_countries)]
        deaths_timeseries = deaths_timeseries[deaths_timeseries['Country/Region'].isin(selected_countries)]

    base_cases = alt.Chart(cases_timeseries).encode(
        x='Date',
        y='Cases',
        color='Country/Region',
        tooltip=['Country/Region', 'Cases']
    )

    base_deaths = alt.Chart(deaths_timeseries).encode(
        x='Date',
        y=alt.Y('Cases', axis=alt.Axis(title='Deaths')),
        color='Country/Region',
        tooltip=['Country/Region', 'Cases']
    )
    st.write(base_cases.mark_line().properties(width=1024).interactive() +  base_cases.mark_circle())
    st.write(base_deaths.mark_line().properties(width=1024).interactive() +  base_deaths.mark_circle())
else:

    # source:           http://weekly.chinacdc.cn/en/article/id/e53946e2-c6c4-41e9-9a9b-fea8db1a8f51
    # processing code:  https://colab.research.google.com/drive/1R_B3sEsg5jBzbSnaVfnUJrFRuXXYQ5bP

    age_mortality_json = '{"Age":{"0":"\\u30000\\u20139","1":"\\u300010\\u201319","2":"\\u300020\\u201329","3":"\\u300030\\u201339","4":"\\u300040\\u201349","5":"\\u300050\\u201359","6":"\\u300060\\u201369","7":"\\u300070\\u201379","8":"\\u3000\\u226580"},"Cases Number":{"0":416,"1":549,"2":3619,"3":7600,"4":8571,"5":10008,"6":8583,"7":3918,"8":1408},"Cases Percentage":{"0":0.9,"1":1.2,"2":8.1,"3":17.0,"4":19.2,"5":22.4,"6":19.2,"7":8.8,"8":3.2},"Deaths Number":{"0":null,"1":1.0,"2":7.0,"3":18.0,"4":38.0,"5":130.0,"6":309.0,"7":312.0,"8":208.0},"Deaths Percentage":{"0":null,"1":0.1,"2":0.7,"3":1.8,"4":3.7,"5":12.7,"6":30.2,"7":30.5,"8":20.3},"Fatality":{"0":null,"1":0.2,"2":0.2,"3":0.2,"4":0.4,"5":1.3,"6":3.6,"7":8.0,"8":14.8},"Observed time":{"0":4383,"1":6625,"2":53953,"3":114550,"4":128448,"5":151059,"6":128088,"7":55832,"8":18671},"Mortality":{"0":null,"1":0.002,"2":0.001,"3":0.002,"4":0.003,"5":0.009,"6":0.024,"7":0.056,"8":0.111}}'
    comorbid_conditions_json = '{"Condition":{"0":"\\u3000Cardiovascular disease","1":"\\u3000Chronic respiratory disease","2":"\\u3000Cancer (any)","3":"\\u3000None","4":"\\u3000Missing"},"Cases Number":{"0":873,"1":511,"2":107,"3":15536,"4":23690},"Cases Percentage":{"0":4.2,"1":2.4,"2":0.5,"3":74.0,"4":53.0},"Deaths Number":{"0":92,"1":32,"2":6,"3":133,"4":617},"Deaths Percentage":{"0":22.7,"1":7.9,"2":1.5,"3":32.8,"4":60.3},"Fatality":{"0":10.5,"1":6.3,"2":5.6,"3":0.9,"4":2.6},"Observed time":{"0":13533,"1":8083,"2":1690,"3":242948,"4":331843},"Mortality":{"0":0.068,"1":0.04,"2":0.036,"3":0.005,"4":0.019}}'
    case_severity_json = '{"Severity":{"0":"\\u3000Mild","1":"\\u3000Severe","2":"\\u3000Critical","3":"\\u3000Missing"},"Cases":{"0":"36,160 (80.9)","1":"6,168 (13.8)","2":"2,087 (4.7)","3":"257 (0.6)"},"Deaths":{"0":"\\u2212","1":"\\u2212","2":"1,023 (100)","3":"\\u2212"},"Fatality":{"0":"\\u2212","1":"\\u2212","2":"49.0","3":"\\u2212"},"Observed time":{"0":"\\u2212","1":"\\u2212","2":"31,456","3":"\\u2212"},"Mortality":{"0":"\\u2212","1":"\\u2212","2":"0.325","3":"\\u2212"},"Cases Number":{"0":"36,160","1":"6,168","2":"2,087","3":"257"},"Cases Percentage":{"0":"80.9","1":"13.8","2":"4.7","3":"0.6"}}'

    # source:           https://www.who.int/docs/default-source/coronaviruse/who-china-joint-mission-on-covid-19-final-report.pdf
    symptoms_dict = {"symptom" : ["fever","dry cough","fatigue","sputum production","shortness of breath","sore throat","headache","myalgia or arthralgia","chills","nausea or vomiting" ,"nasal congestion" ,"diarrhea" ,"hemoptysis" ,"conjunctival congestion"],
                    "percentage": [87.9, 67.7, 38.1, 33.4, 18.6, 13.9, 13.6, 14.8, 11.4, 5.0, 4.8, 3.7, 0.9, 0.8]}

    symptoms = pd.DataFrame.from_dict(symptoms_dict)


    age_mortality = pd.read_json(age_mortality_json)
    comorbid_conditions = pd.read_json(comorbid_conditions_json)
    case_severity = pd.read_json(case_severity_json)

    #st.write(age_mortality)

    age_mortality_chart = alt.Chart(age_mortality).mark_point().encode(
        x='Age',
        y='Fatality',
        size='Cases Number',
        tooltip=['Age', 'Cases Number', 'Deaths Number', 'Deaths Percentage', 'Observed time',  'Fatality', 'Mortality']
    ).properties(height=400, width=800)

    comorbid_conditions_chart = alt.Chart(comorbid_conditions).mark_bar().encode(
        x='Fatality',
        y='Condition',
        #size='Cases Number',
        tooltip=['Condition', 'Cases Number', 'Deaths Number', 'Deaths Percentage', 'Observed time',  'Fatality', 'Mortality']
    ).properties(height=400, width=700)

    case_severity_chart = alt.Chart(case_severity).mark_bar().encode(
        x='Cases Percentage',
        row=alt.Row('Severity', sort=['Missing', 'Mild', 'Severe', 'Critical']),
        tooltip= ['Cases Percentage', 'Severity'],
        color=alt.Color('Severity', sort=['Missing', 'Mild', 'Severe', 'Critical'], scale=alt.Scale(scheme='reds')),
    ).properties(width=600)

    symptoms_chart = alt.Chart(symptoms).mark_bar().encode(
        order=alt.Order('percentage', sort='descending'),
        x='percentage',
        y=alt.Y('symptom:N', sort='-x'),
        tooltip=['symptom', 'percentage']
    ).properties(width=700, height=800)

    st.write(age_mortality_chart)
    st.write(symptoms_chart)
    st.write(comorbid_conditions_chart)
    st.write(case_severity_chart)