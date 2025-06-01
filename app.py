import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Climate Insights Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f5f7f9;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #ffffff;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            border: none;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4e8cff;
            color: white;
        }
        .stButton>button {
            background-color: #4e8cff;
            color: white;
            border-radius: 4px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #3a7ad9;
        }
        .metric-card {
            background-color: white;
            border-radius: 5px;
            padding: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
    </style>
    """, unsafe_allow_html=True)

# Data helper functions
def generate_temperature_data(start_year=1950, end_year=2023):
    """Generate simulated global temperature anomaly data."""
    years = list(range(start_year, end_year + 1))
    # Simulate increasing temperature anomaly with some random variation
    base_anomaly = np.linspace(-0.1, 1.2, len(years))
    noise = np.random.normal(0, 0.15, len(years))
    anomalies = base_anomaly + noise
    
    # Create regional variations
    regions = ['Global', 'Northern Hemisphere', 'Southern Hemisphere', 
               'North America', 'Europe', 'Asia', 'Africa', 'Oceania']
    
    data = []
    for region in regions:
        # Add regional variation
        region_factor = np.random.uniform(0.8, 1.2)
        region_offset = np.random.uniform(-0.2, 0.2)
        region_anomalies = anomalies * region_factor + region_offset
        
        for i, year in enumerate(years):
            data.append({
                'Year': year,
                'Region': region,
                'Temperature Anomaly (°C)': round(region_anomalies[i], 2)
            })
    
    return pd.DataFrame(data)

def generate_co2_data(start_year=1950, end_year=2023):
    """Generate simulated CO2 concentration data."""
    years = list(range(start_year, end_year + 1))
    # Simulate exponential increase in CO2 levels
    base_level = 310 + np.exp(np.linspace(0, 1.2, len(years))) * 60
    noise = np.random.normal(0, 3, len(years))
    co2_levels = base_level + noise
    
    data = []
    for i, year in enumerate(years):
        data.append({
            'Year': year,
            'CO2 Concentration (ppm)': round(co2_levels[i], 1)
        })
    
    return pd.DataFrame(data)

def generate_sea_level_data(start_year=1950, end_year=2023):
    """Generate simulated sea level rise data."""
    years = list(range(start_year, end_year + 1))
    # Simulate accelerating sea level rise
    base_rise = np.power(np.linspace(0, 1, len(years)), 1.5) * 250
    noise = np.random.normal(0, 5, len(years))
    sea_level = base_rise + noise
    
    data = []
    for i, year in enumerate(years):
        data.append({
            'Year': year,
            'Sea Level Rise (mm)': round(sea_level[i], 1)
        })
    
    return pd.DataFrame(data)

def generate_arctic_ice_data(start_year=1950, end_year=2023):
    """Generate simulated Arctic sea ice extent data."""
    years = list(range(start_year, end_year + 1))
    # Simulate decreasing ice extent
    base_extent = 8 - np.power(np.linspace(0, 1, len(years)), 1.2) * 3
    noise = np.random.normal(0, 0.3, len(years))
    ice_extent = base_extent + noise
    
    # Ensure values don't go below a reasonable minimum
    ice_extent = np.maximum(ice_extent, 2)
    
    data = []
    for i, year in enumerate(years):
        data.append({
            'Year': year,
            'Arctic Ice Extent (million sq km)': round(ice_extent[i], 2)
        })
    
    return pd.DataFrame(data)

def generate_country_emissions_data():
    """Generate simulated emissions data by country."""
    countries = [
        'United States', 'China', 'India', 'Russia', 'Japan', 
        'Germany', 'Canada', 'Brazil', 'Indonesia', 'United Kingdom',
        'Mexico', 'France', 'Italy', 'Australia', 'South Korea'
    ]
    
    data = []
    for country in countries:
        # Simulate different emission levels for different countries
        if country in ['United States', 'China']:
            emissions = np.random.uniform(5000, 10000)
        elif country in ['India', 'Russia', 'Japan', 'Germany']:
            emissions = np.random.uniform(1500, 5000)
        else:
            emissions = np.random.uniform(300, 1500)
        
        data.append({
            'Country': country,
            'CO2 Emissions (Mt)': round(emissions, 1)
        })
    
    return pd.DataFrame(data)

def generate_scenario_data(baseline_temp, reduction_level):
    """Generate climate scenario projection data based on emission reduction levels."""
    years = list(range(2023, 2101))
    
    # Different trajectories based on reduction level
    if reduction_level == "No Action (Business as Usual)":
        temp_increase = np.linspace(0, 4.5, len(years))
        uncertainty = 0.5
    elif reduction_level == "Moderate Action":
        temp_increase = np.linspace(0, 2.7, len(years))
        uncertainty = 0.4
    elif reduction_level == "Strong Action":
        temp_increase = np.linspace(0, 1.8, len(years))
        uncertainty = 0.3
    else:  # Paris Agreement Target
        temp_increase = np.linspace(0, 1.5, len(years))
        uncertainty = 0.2
    
    # Add some noise and uncertainty bands
    noise = np.random.normal(0, 0.1, len(years))
    temp_projection = baseline_temp + temp_increase + noise
    
    lower_bound = temp_projection - np.random.uniform(0, uncertainty, len(years))
    upper_bound = temp_projection + np.random.uniform(0, uncertainty, len(years))
    
    data = []
    for i, year in enumerate(years):
        data.append({
            'Year': year,
            'Temperature Projection (°C)': round(temp_projection[i], 2),
            'Lower Bound': round(lower_bound[i], 2),
            'Upper Bound': round(upper_bound[i], 2),
            'Scenario': reduction_level
        })
    
    return pd.DataFrame(data)

def get_report_download_link(df, filename, text):
    """Generate a link to download the data as a CSV file."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Main application
def main():
    load_css()
    
    # Header
    st.title("🌍 Climate Insights Dashboard")
    st.markdown("""
    This interactive dashboard visualizes global climate data and trends. 
    Use the sidebar to filter data and explore different visualizations.
    """)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Year range slider
    min_year = 1950
    max_year = 2023
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(1980, max_year)
    )
    
    # Region selection
    all_regions = ['Global', 'Northern Hemisphere', 'Southern Hemisphere', 
                  'North America', 'Europe', 'Asia', 'Africa', 'Oceania']
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=all_regions,
        default=['Global']
    )
    
    if not selected_regions:
        selected_regions = ['Global']
    
    # Generate data based on filters
    temp_data = generate_temperature_data(min_year, max_year)
    co2_data = generate_co2_data(min_year, max_year)
    sea_level_data = generate_sea_level_data(min_year, max_year)
    ice_data = generate_arctic_ice_data(min_year, max_year)
    emissions_data = generate_country_emissions_data()
    
    # Filter data based on year range
    temp_data_filtered = temp_data[
        (temp_data['Year'] >= year_range[0]) & 
        (temp_data['Year'] <= year_range[1]) &
        (temp_data['Region'].isin(selected_regions))
    ]
    
    co2_data_filtered = co2_data[
        (co2_data['Year'] >= year_range[0]) & 
        (co2_data['Year'] <= year_range[1])
    ]
    
    sea_level_data_filtered = sea_level_data[
        (sea_level_data['Year'] >= year_range[0]) & 
        (sea_level_data['Year'] <= year_range[1])
    ]
    
    ice_data_filtered = ice_data[
        (ice_data['Year'] >= year_range[0]) & 
        (ice_data['Year'] <= year_range[1])
    ]
    
    # Key metrics
    st.header("Key Climate Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        latest_temp = temp_data_filtered[temp_data_filtered['Region'] == 'Global']['Temperature Anomaly (°C)'].iloc[-1]
        st.metric(
            "Current Temperature Anomaly", 
            f"{latest_temp} °C",
            f"{round(latest_temp - temp_data_filtered[temp_data_filtered['Region'] == 'Global']['Temperature Anomaly (°C)'].iloc[0], 2)} °C"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        latest_co2 = co2_data_filtered['CO2 Concentration (ppm)'].iloc[-1]
        st.metric(
            "Current CO₂ Concentration", 
            f"{latest_co2} ppm",
            f"{round(latest_co2 - co2_data_filtered['CO2 Concentration (ppm)'].iloc[0], 1)} ppm"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        latest_sea = sea_level_data_filtered['Sea Level Rise (mm)'].iloc[-1]
        st.metric(
            "Sea Level Rise (since 1950)", 
            f"{latest_sea} mm",
            f"{round(latest_sea - sea_level_data_filtered['Sea Level Rise (mm)'].iloc[0], 1)} mm"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        latest_ice = ice_data_filtered['Arctic Ice Extent (million sq km)'].iloc[-1]
        st.metric(
            "Arctic Ice Extent", 
            f"{latest_ice} M km²",
            f"{round(latest_ice - ice_data_filtered['Arctic Ice Extent (million sq km)'].iloc[0], 2)} M km²",
            delta_color="inverse"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Temperature Trends", 
        "CO₂ & Emissions", 
        "Sea Level & Ice", 
        "Climate Scenarios",
        "Reports"
    ])
    
    # Tab 1: Temperature Trends
    with tab1:
        st.header("Global Temperature Anomalies")
        st.markdown("Temperature anomalies show the difference from the 1951-1980 average global temperature.")
        
        # Line chart for temperature anomalies
        fig_temp = px.line(
            temp_data_filtered, 
            x="Year", 
            y="Temperature Anomaly (°C)", 
            color="Region",
            title="Temperature Anomalies by Region",
            labels={"Temperature Anomaly (°C)": "Temperature Anomaly (°C)"},
            line_shape="spline",
            render_mode="svg"
        )
        fig_temp.update_layout(
            xaxis_title="Year",
            yaxis_title="Temperature Anomaly (°C)",
            legend_title="Region",
            hovermode="x unified"
        )
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Heatmap of temperature anomalies by region and decade
        st.subheader("Temperature Anomalies by Decade")
        
        # Create decade column
        temp_data_filtered['Decade'] = (temp_data_filtered['Year'] // 10) * 10
        decade_temp = temp_data_filtered.groupby(['Region', 'Decade'])['Temperature Anomaly (°C)'].mean().reset_index()
        
        fig_heatmap = px.density_heatmap(
            decade_temp,
            x="Decade",
            y="Region",
            z="Temperature Anomaly (°C)",
            color_continuous_scale="RdBu_r",
            title="Average Temperature Anomalies by Decade and Region"
        )
        fig_heatmap.update_layout(
            xaxis_title="Decade",
            yaxis_title="Region",
            coloraxis_colorbar_title="Temp. Anomaly (°C)"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Tab 2: CO₂ & Emissions
    with tab2:
        st.header("CO₂ Concentration and Emissions")
        
        # Line chart for CO2 concentration
        fig_co2 = px.line(
            co2_data_filtered, 
            x="Year", 
            y="CO2 Concentration (ppm)",
            title="Atmospheric CO₂ Concentration Over Time",
            labels={"CO2 Concentration (ppm)": "CO₂ Concentration (ppm)"},
            line_shape="spline"
        )
        fig_co2.update_layout(
            xaxis_title="Year",
            yaxis_title="CO₂ Concentration (ppm)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_co2, use_container_width=True)
        
        # Bar chart for emissions by country
        st.subheader("CO₂ Emissions by Country")
        
        fig_emissions = px.bar(
            emissions_data.sort_values('CO2 Emissions (Mt)', ascending=False),
            x="Country",
            y="CO2 Emissions (Mt)",
            title="Annual CO₂ Emissions by Country",
            color="CO2 Emissions (Mt)",
            color_continuous_scale="Viridis"
        )
        fig_emissions.update_layout(
            xaxis_title="Country",
            yaxis_title="CO₂ Emissions (Million Tonnes)",
            xaxis={'categoryorder':'total descending'}
        )
        st.plotly_chart(fig_emissions, use_container_width=True)
        
        # Pie chart for emissions distribution
        st.subheader("Emissions Distribution")
        
        fig_pie = px.pie(
            emissions_data,
            values="CO2 Emissions (Mt)",
            names="Country",
            title="Share of Global CO₂ Emissions"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Tab 3: Sea Level & Ice
    with tab3:
        st.header("Sea Level Rise and Arctic Ice Extent")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Area chart for sea level rise
            fig_sea = px.area(
                sea_level_data_filtered,
                x="Year",
                y="Sea Level Rise (mm)",
                title="Global Sea Level Rise Since 1950",
                labels={"Sea Level Rise (mm)": "Sea Level Rise (mm)"},
                color_discrete_sequence=["#5D9CEC"]
            )
            fig_sea.update_layout(
                xaxis_title="Year",
                yaxis_title="Sea Level Rise (mm)",
                hovermode="x unified"
            )
            st.plotly_chart(fig_sea, use_container_width=True)
        
        with col2:
            # Line chart for Arctic ice extent
            fig_ice = px.line(
                ice_data_filtered,
                x="Year",
                y="Arctic Ice Extent (million sq km)",
                title="Arctic Sea Ice Extent",
                labels={"Arctic Ice Extent (million sq km)": "Ice Extent (million sq km)"},
                line_shape="spline",
                color_discrete_sequence=["#4FC1E9"]
            )
            fig_ice.update_layout(
                xaxis_title="Year",
                yaxis_title="Ice Extent (million sq km)",
                hovermode="x unified"
            )
            st.plotly_chart(fig_ice, use_container_width=True)
        
        # Combined visualization
        st.subheader("Relationship Between Temperature and Sea Ice")
        
        # Merge datasets
        merged_data = pd.merge(
            temp_data_filtered[temp_data_filtered['Region'] == 'Global'],
            ice_data_filtered,
            on='Year'
        )
        
        fig_scatter = px.scatter(
            merged_data,
            x="Temperature Anomaly (°C)",
            y="Arctic Ice Extent (million sq km)",
            color="Year",
            size="Year",
            size_max=15,
            title="Arctic Ice Extent vs. Global Temperature Anomaly",
            labels={
                "Temperature Anomaly (°C)": "Temperature Anomaly (°C)",
                "Arctic Ice Extent (million sq km)": "Arctic Ice Extent (million sq km)"
            },
            color_continuous_scale="Viridis"
        )
        fig_scatter.update_layout(
            xaxis_title="Temperature Anomaly (°C)",
            yaxis_title="Arctic Ice Extent (million sq km)"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Tab 4: Climate Scenarios
    with tab4:
        st.header("Climate Scenario Projections")
        st.markdown("""
        Explore different climate scenarios based on global emission reduction efforts.
        These projections show potential temperature pathways until 2100.
        """)
        
        # Get the latest global temperature as baseline
        baseline_temp = temp_data[temp_data['Region'] == 'Global']['Temperature Anomaly (°C)'].iloc[-1]
        
        # Scenario selection
        scenario = st.selectbox(
            "Select Emission Reduction Scenario",
            ["No Action (Business as Usual)", "Moderate Action", "Strong Action", "Paris Agreement Target (1.5°C)"]
        )
        
        # Generate scenario data
        scenario_data = generate_scenario_data(baseline_temp, scenario)
        
        # Plot scenario projection
        fig_scenario = go.Figure()
        
        # Add the historical data
        historical = temp_data[temp_data['Region'] == 'Global']
        fig_scenario.add_trace(go.Scatter(
            x=historical['Year'],
            y=historical['Temperature Anomaly (°C)'],
            name="Historical Data",
            line=dict(color='black', width=2)
        ))
        
        # Add the projection
        fig_scenario.add_trace(go.Scatter(
            x=scenario_data['Year'],
            y=scenario_data['Temperature Projection (°C)'],
            name=f"{scenario} Projection",
            line=dict(color='red', width=2)
        ))
        
        # Add uncertainty range
        fig_scenario.add_trace(go.Scatter(
            x=scenario_data['Year'].tolist() + scenario_data['Year'].tolist()[::-1],
            y=scenario_data['Upper Bound'].tolist() + scenario_data['Lower Bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name="Uncertainty Range"
        ))
        
        # Add reference lines
        fig_scenario.add_shape(
            type="line",
            x0=min(historical['Year']),
            y0=1.5,
            x1=2100,
            y1=1.5,
            line=dict(color="green", width=2, dash="dash"),
            name="1.5°C Target"
        )
        
        fig_scenario.add_shape(
            type="line",
            x0=min(historical['Year']),
            y0=2.0,
            x1=2100,
            y1=2.0,
            line=dict(color="orange", width=2, dash="dash"),
            name="2.0°C Limit"
        )
        
        fig_scenario.update_layout(
            title=f"Temperature Projection: {scenario}",
            xaxis_title="Year",
            yaxis_title="Temperature Anomaly (°C)",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Add annotations for the reference lines
        fig_scenario.add_annotation(
            x=2090,
            y=1.5,
            text="1.5°C Paris Target",
            showarrow=False,
            font=dict(color="green")
        )
        
        fig_scenario.add_annotation(
            x=2090,
            y=2.0,
            text="2.0°C Threshold",
            showarrow=False,
            font=dict(color="orange")
        )
        
        st.plotly_chart(fig_scenario, use_container_width=True)
        
        # Scenario impact description
        st.subheader("Potential Impacts")
        
        if scenario == "No Action (Business as Usual)":
            st.error("""
            ### High Risk Scenario
            - Severe and irreversible impacts on ecosystems
            - Significant sea level rise threatening coastal cities
            - Extreme weather events becoming much more frequent
            - Mass migration due to uninhabitable regions
            - Substantial economic damage globally
            """)
        elif scenario == "Moderate Action":
            st.warning("""
            ### Medium Risk Scenario
            - Significant stress on ecosystems and biodiversity
            - Moderate sea level rise affecting coastal areas
            - Increased frequency of extreme weather events
            - Water scarcity in many regions
            - Notable economic impacts requiring adaptation
            """)
        elif scenario == "Strong Action":
            st.info("""
            ### Lower Risk Scenario
            - Ecosystems under pressure but many can adapt
            - Limited sea level rise with manageable impacts
            - Some increase in extreme weather events
            - Adaptation measures can be effective
            - Economic transition costs offset by avoided damages
            """)
        else:  # Paris Agreement
            st.success("""
            ### Minimum Risk Scenario
            - Most ecosystems can adapt to changes
            - Sea level rise limited to manageable levels
            - Moderate increase in some extreme weather events
            - Successful adaptation possible in most regions
            - Economic benefits of green transition outweigh costs
            """)
    
    # Tab 5: Reports
    with tab5:
        st.header("Data Reports")
        st.markdown("Download data reports for further analysis.")
        
        report_type = st.selectbox(
            "Select Report Type",
            ["Temperature Data", "CO₂ Concentration Data", "Sea Level Data", "Arctic Ice Data", "Emissions Data"]
        )
        
        if report_type == "Temperature Data":
            st.dataframe(temp_data_filtered)
            st.markdown(
                get_report_download_link(
                    temp_data_filtered, 
                    "temperature_data.csv", 
                    "Download Temperature Data CSV"
                ), 
                unsafe_allow_html=True
            )
        elif report_type == "CO₂ Concentration Data":
            st.dataframe(co2_data_filtered)
            st.markdown(
                get_report_download_link(
                    co2_data_filtered, 
                    "co2_data.csv", 
                    "Download CO₂ Data CSV"
                ), 
                unsafe_allow_html=True
            )
        elif report_type == "Sea Level Data":
            st.dataframe(sea_level_data_filtered)
            st.markdown(
                get_report_download_link(
                    sea_level_data_filtered, 
                    "sea_level_data.csv", 
                    "Download Sea Level Data CSV"
                ), 
                unsafe_allow_html=True
            )
        elif report_type == "Arctic Ice Data":
            st.dataframe(ice_data_filtered)
            st.markdown(
                get_report_download_link(
                    ice_data_filtered, 
                    "arctic_ice_data.csv", 
                    "Download Arctic Ice Data CSV"
                ), 
                unsafe_allow_html=True
            )
        else:  # Emissions Data
            st.dataframe(emissions_data)
            st.markdown(
                get_report_download_link(
                    emissions_data, 
                    "emissions_data.csv", 
                    "Download Emissions Data CSV"
                ), 
                unsafe_allow_html=True
            )
        
        # Generate comprehensive report
        st.subheader("Comprehensive Climate Report")
        
        if st.button("Generate Comprehensive Report"):
            # Create a BytesIO object
            buffer = BytesIO()
            
            # Create a pandas Excel writer using the BytesIO object
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                temp_data_filtered.to_excel(writer, sheet_name='Temperature Data', index=False)
                co2_data_filtered.to_excel(writer, sheet_name='CO2 Data', index=False)
                sea_level_data_filtered.to_excel(writer, sheet_name='Sea Level Data', index=False)
                ice_data_filtered.to_excel(writer, sheet_name='Arctic Ice Data', index=False)
                emissions_data.to_excel(writer, sheet_name='Emissions Data', index=False)
            
            # Get the value of the BytesIO buffer
            excel_data = buffer.getvalue()
            
            # Convert to base64
            b64 = base64.b64encode(excel_data).decode()
            
            # Generate download link
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="climate_report.xlsx">Download Comprehensive Excel Report</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            st.success("Comprehensive report generated successfully!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <p>Climate Insights Dashboard | Created with Streamlit | Data for educational purposes</p>
            <p>© 2023 Climate Insights Project</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
