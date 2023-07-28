import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

st.header("Analysis of Event Activities on East Asia Pacific regions from 2010 to 2022")

df = pd.read_csv("East-Asia-Pacific_2018-2022_May20.csv")
df.dropna(axis=1,inplace=True)
df.drop_duplicates(inplace=True)
df =df[["EVENT_DATE", "YEAR", "EVENT_TYPE", "SUB_EVENT_TYPE", "ACTOR1", "INTERACTION", "REGION", "COUNTRY", "LOCATION",
        "LATITUDE", "LONGITUDE", "FATALITIES", "TIMESTAMP"]]
df["EVENT_DATE"] = pd.to_datetime(df.EVENT_DATE, errors="coerce")
df["NEWS_DATE"] = df.TIMESTAMP.apply(lambda x: datetime.strftime(datetime.fromtimestamp(x), "%A, %Y/%b/%d, %I:%M %p"))
df.reset_index(drop=True, inplace=True)
df.set_index("EVENT_DATE", inplace=True)

show = st.checkbox("Click to see dataframe")
if show:
    st.dataframe(df)
else:
    st.write("")
    
col1, col2 = st.columns(2)

with col1:
    yearly_fatal = df.resample("1Y")[["FATALITIES"]].sum()
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_title("Yearly fatalities trend", fontsize="xx-large")
    ax1.set_ylabel("Fatalities", fontsize="x-large")
    ax1.set_xlabel("Event_date", fontsize="x-large")
    ax1.set_xticks(yearly_fatal.index)
    ax1.set_xticklabels(yearly_fatal.index, rotation=90)
    ax1.plot(yearly_fatal.index, yearly_fatal.FATALITIES, marker="o", mfc="red", ms=10, linewidth=4, linestyle="--")

    st.pyplot(fig1)

with col2:
    fatalOverCountry = df.groupby("COUNTRY")[["FATALITIES"]].sum()
    fatalOverCountry = fatalOverCountry[fatalOverCountry["FATALITIES"] > 0]
    fig2, ax2= plt.subplots(figsize=(12,6))
    ax2.set_title("Fatalities all around East Asia Pacific", fontsize="xx-large")
    ax2.set_ylabel("Fatalities", fontsize="x-large")
    ax2.set_xlabel("Countries", fontsize="x-large")
    ax2.set_xticklabels(fatalOverCountry.index, rotation=90)
    ax2.bar(fatalOverCountry.index, fatalOverCountry.FATALITIES, color="red", edgecolor= "black", linewidth=2)

    st.pyplot(fig2)

with col1:
    countries = ["myanmar", "indonesia", "philippines", "thailand"]
    timeframe = [year for year in range(2010, 2023)]
    fig3, ax3 = plt.subplots(figsize=(12, 8))
    ax3.set_title("Remarkable fatalities around East Asia Pacific from 2010 to 2022", fontsize="xx-large")
    ax3.set_ylabel("Numbers of person", fontsize="x-large")
    ax3.set_xlabel("Timeline", fontsize="x-large")
    ax3.set_xticks(ticks=timeframe)
    for country in countries:
        dataset = df[df.COUNTRY.str.lower() == country].groupby("YEAR")[["FATALITIES"]].sum()
        ax3.plot(dataset.index, dataset.FATALITIES, label=country)
    ax3.legend(loc="upper left", fontsize=12)

    st.pyplot(fig3)

with col2:
    event_df = df["EVENT_TYPE"].value_counts()
    fig4, ax4 = plt.subplots(figsize=(12,6))
    ax4.set_title("EVENT_TYPE most happened all these year over East Asia Pacific", fontsize="xx-large")
    ax4.set_ylabel("Number of Occurance", fontsize="x-large")
    ax4.set_xlabel("EVENT_TYPE", fontsize="x-large")
    ax4.set_xticklabels(event_df.index, rotation=90)
    ax4.bar(event_df.index, event_df.values)

    st.pyplot(fig4)

with col1:
    events = {name for name in df.EVENT_TYPE}
    events = list(events)
    fig5, ax5 = plt.subplots(figsize=(12, 8))
    ax5.set_title("Remarkable Events around East Asia Pacific from 2010 to 2022", fontsize="xx-large")
    ax5.set_ylabel("Numbers of Occurance", fontsize="x-large")
    ax5.set_xlabel("Timeline", fontsize="x-large")
    ax5.set_xticks(ticks=timeframe)
    for event in events:
        dataset = df[df.EVENT_TYPE == event].groupby("YEAR")[["EVENT_TYPE"]].count()
        ax5.plot(dataset.index, dataset.EVENT_TYPE, label=event)
    ax5.legend(loc="upper left", fontsize=12)

    st.pyplot(fig5)

st.subheader("Casuality on map")
df_map = df[df.FATALITIES > 0]
df_map = df_map[["YEAR", "COUNTRY", "LATITUDE", "LONGITUDE", "FATALITIES", "EVENT_TYPE", "ACTOR1"]]
df_map.columns = ["YEAR", "COUNTRY", "lat", "lon", "FATALITIES", "EVENT_TYPE", "ACTOR1"]
country_index = df_map.groupby("COUNTRY")["FATALITIES"].sum().sort_values(ascending=False).index
year_list = list({year for year in df_map.YEAR})
year_list.sort(reverse=True)


country = st.selectbox("Select Country", country_index)
year = st.selectbox("Select Year", year_list)
df_selected = df_map[(df_map.COUNTRY == country) & (df_map.YEAR == year)]
st.map(df_selected)

event_types = df_selected.EVENT_TYPE.value_counts()
event_types.name = "Event Types"
actors = df_selected.ACTOR1.value_counts()
actors.name = "Activists"

st.write("Event types: ")
st.write(event_types)
st.write("Activists: ")
st.write(actors)


