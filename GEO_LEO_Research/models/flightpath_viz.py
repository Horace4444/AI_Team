import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# Constants
EARTH_RADIUS = 6371  # km
GEO_ALTITUDE = 35786  # km
LEO_ALTITUDE_RANGE = (160, 2000)  # km
MEO_ALTITUDE_RANGE = (2000, 35786)  # km

# Satellite data
satellites = pd.DataFrame({
    'name': ['Sputnik 1', 'Telstar 1', 'Intelsat I', 'Hubble Space Telescope', 'Starlink-1',
             'Galaxy 15', 'GOES-16', 'Terra', 'GPS IIR-1', 'Iridium NEXT'],
    'type': ['LEO', 'LEO', 'GEO', 'LEO', 'LEO', 
             'GEO', 'GEO', 'LEO', 'MEO', 'LEO'],
    'launch_year': [1957, 1962, 1965, 1990, 2019, 
                    2005, 2016, 1999, 1997, 2017],
    'end_of_service_year': [1958, 1963, 1969, None, None,
                            None, None, None, 2019, None],
    'company': ['USSR', 'AT&T', 'Intelsat', 'NASA/ESA', 'SpaceX',
                'Intelsat', 'NOAA', 'NASA', 'USAF', 'Iridium'],
    'frequency_range': ['20-40 MHz', '6 GHz', '4 GHz', 'Optical', '10.7-12.7 GHz',
                        'C-band', 'Ku-band', 'Terahertz', 'L-band', 'Ka-band'],
    'position': ['LEO', 'LEO', 'GEO', 'LEO', 'LEO', 
                 'GEO', 'GEO', 'LEO', 'MEO', 'LEO']
})

# Replace NaN end_of_service_year with current year
current_year = datetime.now().year
satellites['end_of_service_year'] = satellites['end_of_service_year'].fillna(current_year)

def calculate_orbit(altitude, num_points=100, inclination=0):
    theta = np.linspace(0, 2*np.pi, num_points)
    r = EARTH_RADIUS + altitude
    x = r * np.cos(theta)
    y = r * np.sin(theta) * np.cos(np.radians(inclination))
    z = r * np.sin(theta) * np.sin(np.radians(inclination))
    return x, y, z

def create_earth():
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, np.pi, 100)
    x = EARTH_RADIUS * np.outer(np.cos(theta), np.sin(phi))
    y = EARTH_RADIUS * np.outer(np.sin(theta), np.sin(phi))
    z = EARTH_RADIUS * np.outer(np.ones(100), np.cos(phi))
    return go.Surface(x=x, y=y, z=z, colorscale='Blues', showscale=False)

def create_satellite_traces():
    traces = []
    
    for _, sat in satellites.iterrows():
        if sat['type'] == 'GEO':
            x, y, z = calculate_orbit(GEO_ALTITUDE)
        elif sat['type'] == 'LEO':
            altitude = np.random.uniform(*LEO_ALTITUDE_RANGE)
            inclination = np.random.uniform(0, 90)
            x, y, z = calculate_orbit(altitude, inclination=inclination)
        elif sat['type'] == 'MEO':
            altitude = np.random.uniform(*MEO_ALTITUDE_RANGE)
            inclination = np.random.uniform(0, 90)
            x, y, z = calculate_orbit(altitude, inclination=inclination)
        
        hover_text = f"Name: {sat['name']}<br>Type: {sat['type']}<br>Company: {sat['company']}<br>" \
                     f"Frequency Range: {sat['frequency_range']}<br>Launch Year: {sat['launch_year']}<br>Position: {sat['position']}"
        
        trace = go.Scatter3d(x=x, y=y, z=z, mode='lines', name=sat['name'],
                             line=dict(width=2), hoverinfo='text', hovertext=hover_text, 
                             legendgroup=sat['type'], showlegend=True,
                             customdata=[sat['launch_year']])  # Store launch year in customdata
        traces.append(trace)
    
    return traces

def create_visualization():
    earth = create_earth()
    all_traces = create_satellite_traces()
    
    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='', showticklabels=False),
            yaxis=dict(title='', showticklabels=False),
            zaxis=dict(title='', showticklabels=False),
            aspectmode='data'
        ),
        title='Satellite Orbits',
        hovermode='closest',
        margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(x=0.85, y=0.85),
        updatemenus=[{
            'buttons': [
                {
                    'args': [{'visible': [True] + [trace.customdata[0] <= decade for trace in all_traces]}],
                    'label': str(decade),
                    'method': 'update'
                } for decade in range(1950, 2030, 10)
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.85,
            'xanchor': 'right',
            'y': 1.1,
            'yanchor': 'top'
        }],
        sliders=[{
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Decade: ',
                'visible': True,
                'xanchor': 'right'
            },
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': [
                {
                    'args': [{'visible': [True] + [trace.customdata[0] <= decade for trace in all_traces]}],
                    'label': str(decade),
                    'method': 'update'
                } for decade in range(1950, 2030, 10)
            ]
        }]
    )
    
    fig = go.Figure(data=[earth] + all_traces, layout=layout)
    return fig

def main():
    fig = create_visualization()
    fig.show()

if __name__ == "__main__":
    main()