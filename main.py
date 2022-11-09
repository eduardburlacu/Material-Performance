import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def generate_data(df,name,range_Young,x='Displacement',y='Force'):
    df.astype({'Displacement':'float','Force':'float','Time':'float'})
    df.Displacement = df.Displacement - df.iloc[1, 1]
    young_df = df.loc[(df.Force<range_Young[1]) & (df.Force>range_Young[0]) & (df.Time<range_Young[2])]
    xe = np.array(young_df.Displacement)
    ye = np.array(young_df.Force) / g
    thickness, mass = thickness_mass[name]
    S, error = np.polyfit(xe, ye,deg=1)
    y_yield = S * df.Displacement+ error*1.002
    figur = go.Figure()
    figur.add_scatter(x=df.Displacement,y=df.Force)
    figur.add_scatter(x=df.Displacement, y=y_yield * g)
    figur.show()
    print(S,error)
    S*=1000
    E = S *length**3 /(4 *width * thickness**3 *(1E9))  ## transform it into GPa
    r = mass/ (thickness*width*length)
    sigma =3/2 *length *range_Young[3] / (width * thickness**2 * (1E6))
    figure = px.line(df, x=x, y=y, render_mode='webgl',
                     title=f'Force-Displacement diagram for {name.capitalize()}. Stiffness={round(S,2)} N/m ; E={round(E,2)} GPa; Density = {round(r,2)} kg/m^3; Yield Stress = {round(sigma,2)} MPa')
    figure.show()
    print(S,E,r)

if __name__=='__main__':
    length = 0.2
    width = 25/1000
    g=9.81
    material = 'pmma'
    filepaths = {'aluminium':'Instron_Results/87-aluminium_3pb_2_1.csv','pmma':'Instron_Results/87-pmma_3pb_1_1.csv',
                 'steel':'Instron_Results/87-mild_steel_3pb_1.csv'}
    thickness_mass = {'steel':[1.11/1000,43.75/1000],
                 'pmma':[2.97/1000,17.47/1000],
                 'aluminium':[1.117/1000, 15.12/1000]
                  }
    ranges = {'steel':[20.0,50.0,66, 25],
              'pmma':[20.0,80.0,200,68],
              'aluminium':[15,35,105,13]}

    df = pd.read_csv(filepaths[material])
    generate_data(df,material,range_Young=ranges[material])
