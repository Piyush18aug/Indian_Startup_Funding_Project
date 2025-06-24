import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Funding Analysis')

df = pd.read_csv('startup_cleaning1.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month


def load_overall_analysis():
    st.title('Over All Analysis')

    total = round(df['amount'].sum())
    max_funding = round(df.groupby('startup')['amount'].max().sort_values(ascending=False)).head(1).values[0]
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    no_of_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total Funding', str(total) + ' Cr')
    with col2:
        st.metric('Max Funding', str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg Funding', str(avg_funding) + ' Cr')
    with col4:
        st.metric('No. of Startups', str(no_of_startups))

    st.header('Month-on-Month (MOM) Graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig5)




def load_investor_details(investor):
    st.title(investor)
#st.dataframe(df)
#load recent 5 investment of the investor
    last5_df=df[df['investor'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investor')
    st.dataframe(last5_df)
    col1, col2, col3 = st.columns(3)
    with col1:
        big_series = df[df['investor'].str.contains(investor, case=False, na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment In')
        if big_series.empty:
            st.warning("No investment data available.")
        else:
            fig, ax = plt.subplots()
            ax.bar(big_series.index, big_series.values)
            st.pyplot(fig)
    with col2:
        vertical_series = df[df['investor'].str.contains(investor, case=False, na=False)].groupby('vertical')[
            'amount'].sum().sort_values(ascending=False)
        st.subheader('Sectors Invested In')
        if vertical_series.empty:
            st.warning('No sector data available.')
        else:
            fig1, ax1 = plt.subplots()
            ax1.pie(vertical_series, labels=vertical_series.index, autopct='%1.1f%%')
            st.pyplot(fig1)
    with col3:
        round_series = df[df['investor'].str.contains(investor, case=False, na=False)].groupby('round')[
            'amount'].sum().sort_values(ascending=False)
        st.subheader('Stages Invested In')
        if round_series.empty:
            st.warning('No round data available.')
        else:
            fig2, ax2 = plt.subplots()
            ax2.pie(round_series, labels=round_series.index, autopct='%1.1f%%')
            st.pyplot(fig2)

    col1, col2, col3 = st.columns(3)
    with col1:
        city_series = df[df['investor'].str.contains(investor, case=False, na=False)].groupby('city')[
            'amount'].sum().sort_values(ascending=False)
        st.subheader('City Wise Investment')
        if city_series.empty:
            st.warning("No city data available.")
        else:
            fig3, ax3 = plt.subplots()
            ax3.pie(city_series, labels=city_series.index, autopct='%1.1f%%')
            st.pyplot(fig3)
    with col2:
        year_series = df[df['investor'].str.contains(investor, case=False, na=False)].groupby('year')[
            'amount'].sum().sort_values(ascending=False)
        st.subheader('Year-wise Investment')
        if year_series.empty:
            st.warning("No year-wise data available.")
        else:
            fig4, ax4 = plt.subplots()
            ax4.pie(year_series, labels=year_series.index, autopct='%1.1f%%')
            st.pyplot(fig4)
    with col3:
        df_exploded = df.copy()
        df_exploded['investor'] = df_exploded['investor'].str.split(',')
        df_exploded = df_exploded.explode('investor')
        df_exploded['investor'] = df_exploded['investor'].str.strip()
        common_investor = df_exploded.groupby('investor')['startup'].nunique()
        common_investor = common_investor[common_investor > 1].sort_values(ascending=False).head(10)
        st.subheader('Common Investors (Top 10)')
        if common_investor.empty:
            st.warning("No common investor data available.")
        else:
            fig5, ax5 = plt.subplots()
            ax5.pie(common_investor, labels=common_investor.index, autopct='%1.1f%%')
            st.pyplot(fig5)


def load_startup_detail(startup):
    df['startup'] = df['startup'].str.strip().str.replace("\\", "")

    df['vertical'] = df['vertical'].str.strip()

    df['investor'] = df['investor'].str.strip()

    df['round_info'] = df['date'].astype(str) + '|' + df['round'].astype(str) + '|' + df['investor'].astype(str)

    df['city'] = df['city'].str.strip()
    startup_row = df[df['startup'] == startup]
    if startup_row.empty:
        st.warning('No Data Available')
        return
    name = startup_row['startup'].iloc[0]
    vertical = startup_row['vertical'].iloc[0]
    investors = startup_row['investor'].unique()
    investor_name = ', '.join(investors)
    city=startup_row['city'].iloc[0]
    funding_rounds = df.groupby('startup')['round_info'].count().sort_values(ascending=False)
    col1, col2= st.columns(2)
    with col1:
        st.metric('Name', name)
    with col2:
        st.metric('Industry', vertical)
    st.subheader("Investors")
    st.write(investor_name)

    st.metric('Location',city)

    st.subheader('Funding Round')
    st.dataframe(funding_rounds)

    df_exploded = df.copy()
    df_exploded['startup'] = df_exploded['startup'].str.split(',')
    df_exploded = df_exploded.explode('startup')
    df_exploded['startup'] = df_exploded['startup'].str.strip()
    common_investor = df_exploded.groupby('startup')['investor'].nunique()
    common_investor = common_investor[common_investor > 1].sort_values(ascending=False).head(10)
    st.subheader('Common startup (Top 10)')
    if common_investor.empty:
        st.warning("No common investor data available.")
    else:
        fig5, ax5 = plt.subplots()
        ax5.pie(common_investor, labels=common_investor.index, autopct='%1.1f%%')
        st.pyplot(fig5)


st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(set(df['startup'].str.strip())))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_detail(selected_startup)

else:
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investor'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
    else:
        st.title('Please Choose the Investor and press the button')

