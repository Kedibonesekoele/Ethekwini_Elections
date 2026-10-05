import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="eThekwini 2026 Election Analytics",
    page_icon="🗳️",
    layout="wide"
)
@st.cache_data
def load_data():
    forecast = pd.read_csv("forecast_2026.csv")
    ward_forecast = pd.read_csv("ward_forecast_2026.csv")
    ward_winners = pd.read_csv("ward_winners_2026.csv")
    turnout = pd.read_csv("turnout_summary.csv")

    return forecast, ward_forecast, ward_winners, turnout


forecast_2026, ward_forecast, ward_winners, turnout_summary = load_data()
#Tittle
st.title("🗳️ eThekwini 2026 Election Analytics Dashboard")

st.markdown(
    """
    ### 2026 South African Local Government Election Analysis

    This dashboard presents machine-learning-based analytical estimates
    for the **eThekwini Metropolitan Municipality** using historical
    election results from 2011, 2016 and 2021.
    """
)

st.divider()

leading_party = forecast_2026.iloc[0]

registered_voters = turnout_summary.loc[
    turnout_summary["Metric"] == "Registered Voters", "Value"
].iloc[0]

estimated_votes = turnout_summary.loc[
    turnout_summary["Metric"] == "Estimated Votes Cast", "Value"
].iloc[0]

turnout_rate = turnout_summary.loc[
    turnout_summary["Metric"] == "Estimated Turnout (%)", "Value"
].iloc[0]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Projected Leading Party",
        leading_party["Party"]
    )

with col2:
    st.metric(
        "Projected Vote Share",
        f"{leading_party['Projected2026VoteShare']:.2f}%"
    )

with col3:
    st.metric(
        "Registered Voters",
        f"{int(registered_voters):,}"
    )

with col4:
    st.metric(
        "Estimated Turnout",
        f"{turnout_rate:.2f}%"
    )


st.divider()

st.header("1. Projected Leading Party")

st.write(
    f"According to the model, **{leading_party['Party']}** "
    f"has the highest projected vote share."
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Leading Party",
        leading_party["Party"]
    )

with col2:
    st.metric(
        "Projected Votes",
        f"{int(leading_party['Projected2026Votes']):,}"
    )

#output 3
st.header("2. Projected Result for Each Relevant Party")

display_forecast = forecast_2026[
    [
        "Party",
        "VoteShare2021",
        "Projected2026VoteShare",
        "Projected2026Votes"
    ]
].copy()

display_forecast.columns = [
    "Party",
    "2021 Vote Share (%)",
    "Projected 2026 Vote Share (%)",
    "Projected 2026 Votes"
]

display_forecast["Projected 2026 Vote Share (%)"] = (
    display_forecast["Projected 2026 Vote Share (%)"].round(2)
)

display_forecast["Projected 2026 Votes"] = (
    display_forecast["Projected 2026 Votes"].astype(int)
)

st.dataframe(
    display_forecast,
    use_container_width=True,
    hide_index=True
)

# party forecast chart 
chart_data = forecast_2026.sort_values(
    "Projected2026VoteShare",
    ascending=True
)

fig_party = px.bar(
    chart_data,
    x="Projected2026VoteShare",
    y="Party",
    orientation="h",
    title="Projected 2026 eThekwini Vote Share",
    labels={
        "Projected2026VoteShare": "Projected Vote Share (%)",
        "Party": "Political Party"
    }
)

fig_party.update_layout(
    height=500
)

st.plotly_chart(
    fig_party,
    use_container_width=True
)


st.divider()

#selected wards
st.header("3. Projected Leaders in Three Selected Wards")

st.write(
    "Three wards with historical election data available across "
    "the three election periods were selected for ward-level analysis."
)

ward_display = ward_winners[
    [
        "Ward",
        "Party",
        "Projected2026VoteShare"
    ]
].copy()

ward_display.columns = [
    "Ward",
    "Projected Leading Party",
    "Projected Vote Share (%)"
]

ward_display["Projected Vote Share (%)"] = (
    ward_display["Projected Vote Share (%)"].round(2)
)

st.dataframe(
    ward_display,
    use_container_width=True,
    hide_index=True
)

#Ward chart
fig_ward = px.bar(
    ward_display,
    x="Ward",
    y="Projected Vote Share (%)",
    color="Projected Leading Party",
    title="Projected Leading Party Vote Share in Selected Wards"
)

fig_ward.update_layout(
    height=450
)

st.plotly_chart(
    fig_ward,
    use_container_width=True
)


st.divider()

#Ward detailed view
st.subheader("Detailed Ward Forecast")

selected_ward = st.selectbox(
    "Select a ward to view projected party shares:",
    sorted(ward_forecast["Ward"].unique())
)

selected_ward_data = ward_forecast[
    ward_forecast["Ward"] == selected_ward
].copy()

selected_ward_data = selected_ward_data.sort_values(
    "Projected2026VoteShare",
    ascending=False
)

ward_chart = px.bar(
    selected_ward_data,
    x="Party",
    y="Projected2026VoteShare",
    title=f"Projected Party Vote Shares — {selected_ward}",
    labels={
        "Projected2026VoteShare": "Projected Vote Share (%)",
        "Party": "Political Party"
    }
)

ward_chart.update_layout(
    height=450
)

st.plotly_chart(
    ward_chart,
    use_container_width=True
)


st.divider()

# Coliation Model Output
st.header("4. Coalition Model Output")

largest_share = forecast_2026[
    "Projected2026VoteShare"
].max()

if largest_share >= 50:

    st.success(
        "Model output: No coalition indicator based on "
        "projected vote share because the projected leading "
        "party reaches or exceeds 50%."
    )

else:

    st.warning(
        "Model output: Coalition formation indicated because "
        "no projected party reaches 50% of the projected vote share."
    )

st.info(
    "Important: This is a vote-share-based model output. "
    "It does not predict which party will govern."
)


st.divider()

#Voter Turnout
st.header("4. Coalition Model Output")

largest_share = forecast_2026[
    "Projected2026VoteShare"
].max()

if largest_share >= 50:

    st.success(
        "Model output: No coalition indicator based on "
        "projected vote share because the projected leading "
        "party reaches or exceeds 50%."
    )

else:

    st.warning(
        "Model output: Coalition formation indicated because "
        "no projected party reaches 50% of the projected vote share."
    )

st.info(
    "Important: This is a vote-share-based model output. "
    "It does not predict which party will govern."
)


st.divider()

#Methodology
st.header("Methodology")

st.markdown(
    """
    **Historical data:**  
    Election results from 2011, 2016 and 2021 were used to construct
    historical party and ward-level vote-share features.

    **Machine learning:**  
    Previous-election vote share was used as an input feature and
    subsequent-election vote share was used as the target variable.

    **Models evaluated:**
    - Linear Regression
    - Random Forest Regression

    **Evaluation measures:**
    - Mean Absolute Error (MAE)
    - Root Mean Squared Error (RMSE)
    - R²

    The better-performing model was selected to generate the
    2026 vote-share estimates.
    """
)

#Limitations 
st.header("Limitations")

st.markdown(
    """
    - Only three historical election periods were available.
    - Election forecasts are estimates and are not guaranteed outcomes.
    - Historical election conditions may differ from those in 2026.
    - Ward boundary changes can affect direct geographic comparisons
      between election years.
    - The coalition result is a vote-share-based indicator and should
      not be interpreted as a prediction of which party will govern.
    - The turnout figure is an analytical estimate based on the
      available election data.
    """
)



st.divider()

st.caption(
    "eThekwini 2026 Election Analytics | DS2 Examination Project"
)
