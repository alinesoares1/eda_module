"""Exploratory Data Analysis Module - 4.0 Industry."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import functions

st.set_page_config(
    layout="wide", page_icon='images/put_your_image_here.png',
    page_title='EDA - Di2win')

st.image('images/put_your_image_here.png', use_column_width=True)

st.header("Exploratory Data Analysis Tool for 4.0 Industries 🔍 ")

functions.space()
st.write('<p style="font-size:130%">Import Dataset</p>',
         unsafe_allow_html=True)
file_format = st.radio('Select file format:',
                       ('csv', 'excel', 'json', 'cosmosDB'), key='file_format')

dataset = st.file_uploader(label='')

if dataset is not None:
    if file_format == 'csv':
        df = pd.read_csv(dataset, sep=';|,')
    elif file_format == 'json':
        df = pd.read_json(dataset)
        st.subheader('Select target column:')
        target_column = st.selectbox("", df.columns, index=len(df.columns)-1)
        df = pd.concat([df[target_column].apply(pd.Series),
                       df.drop(target_column, axis=1)], axis=1)
    else:
        df = pd.read_excel(dataset)

    st.subheader('Dataframe:')
    n, m = df.shape
    st.write(
        f'<p style="font-size:100%">Dataset contains {n} rows \
            and {m} columns.</p>', unsafe_allow_html=True)

    st.dataframe(df.head())

    all_vizuals = ['Info', 'NA Info', 'Descriptive Analysis', 'Correlation Matrix',
                   'Target Analysis', 'Distribution of Numerical Columns',
                   'Box Plots', 'Outlier Analysis']
    functions.space(3)
    vizuals = st.sidebar.multiselect(
        "Choose which visualizations you want to see 👇", all_vizuals)

    if 'Info' in vizuals:
        st.subheader('Info:')
        c1, c2, c3 = st.columns([1, 2, 1])
        c2.dataframe(functions.df_info(df))

    if 'NA Info' in vizuals:
        st.subheader('NA Value Information:')
        if df.isnull().sum().sum() == 0:
            st.write('There is not any NA value in your dataset.')
        else:
            c1, c2, c3 = st.columns([0.5, 2, 0.5])
            c2.dataframe(functions.df_isnull(df), width=1500)
            functions.space(2)

    if 'Descriptive Analysis' in vizuals:
        st.subheader('Decriptive Analysis')
        st.dataframe(df.describe().round())

    num_columns = df.select_dtypes(exclude='object').columns
    cat_columns = df.select_dtypes(exclude='object').columns

    if 'Correlation Matrix' in vizuals:
        if len(num_columns) == 0:
            st.write('There is no numerical columns in the data.')
        else:
            selected_num_cols = functions.sidebar_multiselect_container(
                'Choose columns for Correlation Matrix:',
                num_columns,
                'Correlation Matrix'
            )
            st.subheader('Correlation Matrix')
            c1, c2 = st.columns([3, 1])
            df_corr = df[selected_num_cols].corr()
            fig = go.Figure()
            fig.add_trace(
                go.Heatmap(
                    x=df_corr.columns,
                    y=df_corr.index,
                    z=np.array(df_corr),
                    text=df_corr.values,
                    texttemplate='%{text:.2f}'
                )
            )
            c1.plotly_chart(fig, use_container_width=True)

    if 'Target Analysis' in vizuals:
        st.subheader('Select target column:')
        target_column = st.selectbox("", df.columns, index=len(df.columns)-1)

        st.subheader('Histogram of target column')
        fig = px.histogram(df, x=target_column)
        c1, c2, c3 = st.columns([0.5, 2, 0.5])
        c2.plotly_chart(fig)

    if 'Distribution of Numerical Columns' in vizuals:

        if len(num_columns) == 0:
            st.write('There is no numerical columns in the data.')
        else:
            selected_num_cols = functions.sidebar_multiselect_container(
                'Choose columns for Distribution plots:',
                num_columns,
                'Distribution'
            )
            st.subheader('Distribution of numerical columns')
            st.subheader('Select timestamp column:')
            timestamp_column = st.selectbox(
                " ", df.columns, index=len(df.columns)-1)
            i = 0
            while (i < len(selected_num_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_num_cols)):
                        break

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df[timestamp_column],
                                             y=df[selected_num_cols[i]],
                                             showlegend=True,
                                             name=selected_num_cols[i],
                                             mode='lines')
                                  )

                    fig.update_xaxes(
                        rangeslider_visible=True,
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1m", step="month",
                                     stepmode="backward"),
                                dict(count=6, label="6m", step="month",
                                     stepmode="backward"),
                                dict(count=1, label="YTD",
                                     step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year",
                                     stepmode="backward"),
                                dict(step="all")
                            ])
                        )
                    )
                    fig.update_layout(xaxis=dict(
                        rangeselector=dict(font=dict(color="black"))))

                    j.plotly_chart(fig, use_container_width=True)
                    i += 1

    if 'Box Plots' in vizuals:
        if len(num_columns) == 0:
            st.write('There is no numerical columns in the data.')
        else:
            selected_num_cols = functions.sidebar_multiselect_container(
                'Choose columns for Box plots:', num_columns, 'Box')
            st.subheader('Box plots')
            i = 0
            while (i < len(selected_num_cols)):
                c1, c2 = st.columns(2)
                for j in [c1, c2]:

                    if (i >= len(selected_num_cols)):
                        break

                    fig = px.box(df, y=selected_num_cols[i])
                    j.plotly_chart(fig, use_container_width=True)
                    i += 1

    if 'Outlier Analysis' in vizuals:
        st.subheader('Outlier Analysis')
        st.dataframe(functions.number_of_outliers(df))
