
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("IPL PRO DASHBOARD")

with st.spinner("Loading data..."):
    df = pd.read_csv("ipl_real_data1.csv")

# ---------------- DATA (3 players per team) ----------------
df = pd.read_csv("ipl_real_data1.csv")
df["impact_score"] = (df["runs"] * df["strike_rate"]) / 100
st.session_state.df = df

# ---------------- TEAM LOGOS ----------------
team_logos = {
    "RCB": "https://upload.wikimedia.org/wikipedia/en/4/47/Royal_Challengers_Bangalore_Logo.png",
    "MI": "https://upload.wikimedia.org/wikipedia/en/c/cd/Mumbai_Indians_Logo.svg",
    "CSK": "https://upload.wikimedia.org/wikipedia/en/2/2e/Chennai_Super_Kings_Logo.svg",
    "KKR": "https://upload.wikimedia.org/wikipedia/en/4/4b/Kolkata_Knight_Riders_Logo.svg",
    "SRH": "https://upload.wikimedia.org/wikipedia/en/8/81/Sunrisers_Hyderabad.svg",
    "PBKS": "https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg",
    "RR": "https://upload.wikimedia.org/wikipedia/en/6/60/Rajasthan_Royals_Logo.svg",
    "DC": "https://upload.wikimedia.org/wikipedia/en/2/2f/Delhi_Capitals.svg",
    "LSG": "https://upload.wikimedia.org/wikipedia/en/a/a9/Lucknow_Super_Giants_IPL_Logo.svg",
    "GT": "https://upload.wikimedia.org/wikipedia/en/0/09/Gujarat_Titans_Logo.svg"
}

# ---------------- TEAM COLORS ----------------
team_colors = {
    "RCB": "#EC1C24",
    "MI": "#004BA0",
    "CSK": "#FFD700",
    "KKR": "#3A225D",
    "SRH": "#FF822A",
    "PBKS": "#D71920",
    "RR": "#EA1A85",
    "DC": "#00008B",
    "LSG": "#00A9E0",
    "GT": "#1C1C1C"
}
plt.style.use("dark_background")

st.subheader(" Search Player")

search = st.text_input("Enter player name")

if search:
    result = df[df["player"].str.contains(search, case=False)]
    st.dataframe(result)



st.subheader(" Key Insights")

top_player = df.sort_values(by="runs", ascending=False).iloc[0]
best_sr = df.sort_values(by="strike_rate", ascending=False).iloc[0]
best_avg = df.sort_values(by="average", ascending=False).iloc[0]

st.success(f" Top Performer: {top_player['player']} ({top_player['runs']} runs)")
st.info(f" Most Explosive: {best_sr['player']} (SR {best_sr['strike_rate']})")
st.warning(f" Most Consistent: {best_avg['player']} (Avg {best_avg['average']})")

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("Filters")
team = st.sidebar.selectbox("Select Team", df["team"].unique())

filtered_df = df[df["team"] == team]

st.divider()

st.subheader(" Player Comparison")

col1, col2 = st.columns(2)

players = df["player"].unique()

with col1:
    p1_name = st.selectbox("Player 1", players)

with col2:
    p2_name = st.selectbox("Player 2", players)

if p1_name == p2_name:
    st.warning(" Select two different players")
p1 = df[df["player"] == p1_name].iloc[0]
p2 = df[df["player"] == p2_name].iloc[0]

comp = {
    "Metric": ["Runs", "Average", "Strike Rate", "Impact Score"],
    p1_name: [p1["runs"], p1["average"], p1["strike_rate"], p1["impact_score"]],
    p2_name: [p2["runs"], p2["average"], p2["strike_rate"], p2["impact_score"]]
}

st.dataframe(pd.DataFrame(comp))

st.subheader(" Team Comparison")

team_stats = df.groupby("team").agg({
    "runs": "sum",
    "strike_rate": "mean"
})

st.dataframe(team_stats)

st.subheader(" Impact Score Ranking")

impact_df = df.sort_values(by="impact_score", ascending=False)


st.dataframe(impact_df[["player", "team", "impact_score"]])
st.subheader(" What is Impact Score?")

st.markdown("""
**Impact Score** is a custom metric designed to evaluate a player's overall batting performance.

###  Formula:
**Impact Score = (Runs × Strike Rate) / 100**

###  Why this matters:
- **Runs** → Measures total contribution  
- **Strike Rate** → Measures scoring speed  
- Combining both gives a **balanced performance score**

###  Interpretation:
- Higher score → More impactful player  
- Helps identify players who score **fast AND big**

---
""")


# ---------------- HEADER ----------------
col1, col2 = st.columns([1,5])

with col1:
    st.image(team_logos[team], width=80)

with col2:
    st.markdown(f"## {team} Team Analysis")

# ---------------- KPI ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Players", len(df))
col2.metric("Total Runs", int(df["runs"].sum()))
col3.metric("Avg Strike Rate", round(df["strike_rate"].mean(), 2))
# ---------------- CHARTS ----------------
col5, col6 = st.columns(2)

color = team_colors[team]

with col5:
    fig, ax = plt.subplots()
    ax.bar(filtered_df["player"], filtered_df["runs"], color=color)
    plt.xticks(rotation=45)
    ax.set_title("Runs")
    st.pyplot(fig)

with col6:
    fig2, ax2 = plt.subplots()
    ax2.bar(filtered_df["player"], filtered_df["strike_rate"], color=color)
    plt.xticks(rotation=45)
    ax2.set_title("Strike Rate")
    st.pyplot(fig2)

col1, col2 = st.columns(2)

with col1:
    st.subheader(" Impact Score")
    impact_df = df.sort_values(by="impact_score", ascending=False)
    st.bar_chart(impact_df.set_index("player")["impact_score"])

with col2:
    st.subheader(" Team Runs")
    team_runs = df.groupby("team")["runs"].sum()
    st.bar_chart(team_runs)

# ---------------- TABLE ----------------
st.subheader(" Player Stats")
st.dataframe(filtered_df)

with st.spinner("Loading data..."):
    df = pd.read_csv("ipl_real_data1.csv")
