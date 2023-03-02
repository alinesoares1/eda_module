"""EDA Tool functions."""
import io
import pandas as pd
import streamlit as st


def space(num_lines=1):
    """Return the required number of spaced lines."""
    for _ in range(num_lines):
        st.write("")


def df_info(df):
    """
    Primary information analysis of the data.

        Parameters
        ----------
                df : DataFrame
                    Pandas DataFrame.
        Returns
        -------
                DataFrame
                    Pandas Dataframe with all the columns of the input
                    dataframe and their respectives data type and number
                    of non-null values.
    """
    df.columns = df.columns.str.replace(' ', '_')
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()

    df_info = s.split('\n')

    counts = []
    names = []
    nn_count = []
    dtype = []
    for i in range(5, len(df_info)-3):
        line = df_info[i].split()
        counts.append(line[0])
        names.append(line[1])
        nn_count.append(line[2])
        dtype.append(line[4])

    df_info_dataframe = pd.DataFrame(
        data={'#': counts, 'Column': names,
              'Non-Null Count': nn_count, 'Data Type': dtype})
    return df_info_dataframe.drop('#', axis=1)


def df_isnull(df):
    """
    Check the presence number of missing values of a numerical variable.

        Parameters
        ----------
                df : DataFrame
                    Pandas DataFrame.
        Returns
        -------
                DataFrame
                    Pandas Dataframe with all the columns of the input
                    dataframe and their respective number of null values.
    """
    res = pd.DataFrame(df.isnull().sum()).reset_index()
    res['Percentage'] = round(res[0] / df.shape[0] * 100, 2)
    res['Percentage'] = res['Percentage'].astype(str) + '%'
    return res.rename(columns={'index': 'Column', 0: 'Number of null values'})


def sidebar_multiselect_container(message, arr, key):
    """
    Function to enable the user choose which column of the data should be
    analyzed.

        Parameters
        ----------
                message : string.
                    Message indicating some user action. e.g: 'Choose
                    columns for Distribution plots:'
                arr : array.
                   Array of dataframe columns names.
                key: Keyword to the checkbox.
        Returns
        -------
                streamlit container
                    Invisible container that can be used to hold multiple elements.

    """

    container = st.sidebar.container()
    select_all_button = st.sidebar.checkbox("Select all for " + key + " plots")
    if select_all_button:
        selected_num_columns = container.multiselect(
            message, arr, default=list(arr))
    else:
        selected_num_columns = container.multiselect(
            message, arr, default=arr[0])

    return selected_num_columns


def number_of_outliers(df):
    """
    Outlier Analysis.

        Parameters
        ----------
                df : DataFrame
                    Pandas DataFrame.
        Returns
        -------
                DataFrame
                    Pandas Dataframe with all the columns of the input
                    dataframe and their respectives count of outliers.
    """

    df = df.select_dtypes(exclude='object')

    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    ans = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).sum()
    df = pd.DataFrame(ans).reset_index().rename(
        columns={'index': 'column', 0: 'count_of_outilers'})
    return df
