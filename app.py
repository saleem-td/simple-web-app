import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import random
from data_helper import load_sample_data, get_random_quote

# Page configuration
st.set_page_config(
    page_title="Climate Insights Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #26A69A;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .card {
        border-radius: 5px;
        padding: 1.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 1rem;
        color: #616161;
    }
    .stProgress > div > div > div > div {
        background-color: #26A69A;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/616/616490.png", width=100)
    st.markdown("## Climate Insights")
    st.markdown("Explore global climate data and trends")
    
    # Add filters
    st.markdown("### Filters")
    year_range = st.slider("Select Year Range", 1950, 2023, (2000, 2023))
    regions = st.multiselect("Select Regions", 
                           ["North America", "South America", "Europe", "Africa", "Asia", "Oceania"],
                           default=["North America", "Europe", "Asia"])
    
    # Add a quote that changes periodically
    st.markdown("### Climate Quote")
    quote, author = get_random_quote()
    st.markdown(f"*\"{quote}\"*")
    st.markdown(f"— {author}")
    
    # Add a simulated real-time update
    st.markdown("### Last Data Update")
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"🕒 {current_time}")

# Main content
st.markdown('<h1 class="main-header">Global Climate Insights Dashboard</h1>', unsafe_allow_html=True)

# Load data
df = load_sample_data()

# Filter data based on sidebar selections
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
filtered_df = filtered_df[filtered_df['Region'].isin(regions)]

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Average Temperature Rise</p>', unsafe_allow_html=True)
    avg_temp = round(filtered_df['Temperature_Anomaly'].mean(), 2)
    st.markdown(f'<p class="metric-value">{avg_temp}°C</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">CO₂ Concentration</p>', unsafe_allow_html=True)
    avg_co2 = int(filtered_df['CO2_Concentration'].mean())
    st.markdown(f'<p class="metric-value">{avg_co2} ppm</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Sea Level Rise</p>', unsafe_allow_html=True)
    avg_sea = round(filtered_df['Sea_Level_Rise'].mean(), 1)
    st.markdown(f'<p class="metric-value">{avg_sea} mm</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Arctic Ice Loss</p>', unsafe_allow_html=True)
    ice_loss = round(filtered_df['Arctic_Ice_Extent'].mean(), 1)
    st.markdown(f'<p class="metric-value">{ice_loss}%</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main charts
st.markdown('<h2 class="sub-header">Temperature Anomaly Over Time</h2>', unsafe_allow_html=True)

# Temperature anomaly chart
fig_temp = px.line(filtered_df, x='Year', y='Temperature_Anomaly', color='Region',
                  title='Global Temperature Anomaly by Region',
                  labels={'Temperature_Anomaly': 'Temperature Anomaly (°C)', 'Year': 'Year'})
fig_temp.update_layout(
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=40, t=40, b=40),
)
st.plotly_chart(fig_temp, use_container_width=True)

# Two column layout for additional charts
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h2 class="sub-header">CO₂ Concentration Trends</h2>', unsafe_allow_html=True)
    fig_co2 = px.area(filtered_df, x='Year', y='CO2_Concentration', color='Region',
                     title='CO₂ Concentration by Region',
                     labels={'CO2_Concentration': 'CO₂ (ppm)', 'Year': 'Year'})
    fig_co2.update_layout(height=400)
    st.plotly_chart(fig_co2, use_container_width=True)

with col2:
    st.markdown('<h2 class="sub-header">Sea Level Rise</h2>', unsafe_allow_html=True)
    fig_sea = px.line(filtered_df, x='Year', y='Sea_Level_Rise',
                     title='Global Sea Level Rise',
                     labels={'Sea_Level_Rise': 'Sea Level Rise (mm)', 'Year': 'Year'})
    fig_sea.update_layout(height=400)
    st.plotly_chart(fig_sea, use_container_width=True)

# Interactive section
st.markdown('<h2 class="sub-header">Climate Impact Explorer</h2>', unsafe_allow_html=True)

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["Temperature Map", "Emissions by Sector", "Climate Scenarios"])

with tab1:
    st.markdown("### Global Temperature Distribution")
    year_selected = st.slider("Select Year", min_value=year_range[0], max_value=year_range[1], value=year_range[1])
    
    # Filter data for selected year
    year_data = filtered_df[filtered_df['Year'] == year_selected]
    
    # Create a choropleth map
    fig_map = px.choropleth(year_data, 
                          locations='Country_Code', 
                          color='Temperature_Anomaly',
                          hover_name='Region',
                          color_continuous_scale=px.colors.sequential.Plasma,
                          title=f'Temperature Anomaly by Region ({year_selected})')
    fig_map.update_layout(height=500)
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.markdown("### Emissions by Sector")
    
    # Sample emissions data by sector
    sectors = ['Energy', 'Industry', 'Agriculture', 'Waste', 'Land Use', 'Transport']
    emissions = [40, 21, 15, 5, 9, 10]
    
    fig_sectors = px.pie(values=emissions, names=sectors, hole=0.4,
                       title='Global Greenhouse Gas Emissions by Sector')
    fig_sectors.update_layout(height=500)
    st.plotly_chart(fig_sectors, use_container_width=True)

with tab3:
    st.markdown("### Climate Scenarios Simulation")
    
    scenario = st.selectbox("Select Climate Scenario", 
                          ["Business as Usual", "Moderate Mitigation", "Strong Mitigation"])
    
    if st.button("Run Simulation"):
        with st.spinner("Running climate model simulation..."):
            # Simulate processing time
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            # Show results based on scenario
            if scenario == "Business as Usual":
                result = "4.5°C increase by 2100"
                color = "red"
            elif scenario == "Moderate Mitigation":
                result = "2.7°C increase by 2100"
                color = "orange"
            else:
                result = "1.5°C increase by 2100"
                color = "green"
                
            st.success("Simulation complete!")
            st.markdown(f"<h3 style='color:{color};'>Projected Outcome: {result}</h3>", unsafe_allow_html=True)
            
            # Add a random chart based on the scenario
            years = list(range(2025, 2101, 5))
            
            if scenario == "Business as Usual":
                temps = [0.85 + i*0.073 for i in range(len(years))]
            elif scenario == "Moderate Mitigation":
                temps = [0.85 + i*0.037 for i in range(len(years))]
            else:
                temps = [0.85 + i*0.013 for i in range(len(years))]
                
            scenario_df = pd.DataFrame({
                'Year': years,
                'Temperature_Increase': temps
            })
            
            fig_scenario = px.line(scenario_df, x='Year', y='Temperature_Increase',
                                 title=f'Projected Temperature Increase - {scenario} Scenario',
                                 labels={'Temperature_Increase': 'Temperature Increase (°C)', 'Year': 'Year'})
            fig_scenario.update_layout(height=400)
            st.plotly_chart(fig_scenario, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("### About This Dashboard")
st.markdown("""
This interactive dashboard visualizes global climate data and trends. The data shown includes temperature anomalies,
CO₂ concentrations, sea level rise, and Arctic ice extent. You can filter the data by year range and regions using
the sidebar controls.

The dashboard also includes a climate impact explorer that allows you to explore temperature distributions across
different regions, emissions by sector, and simulate different climate scenarios.

**Note:** This is a demonstration using simulated data for educational purposes.
""")

# Add a download button for a sample report
if st.button("Generate Climate Report"):
    with st.spinner("Generating report..."):
        time.sleep(2)
        st.success("Report generated successfully!")
        
        # Create a sample CSV for download
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Report Data (CSV)",
            data=csv,
            file_name="climate_data_report.csv",
            mime="text/csv",
        )
