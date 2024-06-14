#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import io
import plotly.graph_objects as go
import plotly.io as pio
from streamlit import components
import openpyxl
from scipy import stats





# Page configuration
st.set_page_config(
    page_title="Gates Challenge SX",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: -10rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


# Load data
file_path = 'tips.xlsx'
sheet_name = 'Data'

# Read the specific sheet
df = pd.read_excel(file_path, sheet_name=sheet_name)
df = df.drop(columns=['Unnamed: 0'])


# Sidebar
with st.sidebar:
    # st.title('SX Challenge <br> México')
    st.markdown("<h3 style='text-align: center;'>Análisis de Propinas<br></h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Sales Excelence - GATES<br></h3>", unsafe_allow_html=True)

    # # Entidad
    # entidad_list = list(df_reshaped.ENTIDAD.unique())
    # selected_entidad = st.selectbox('Seleccione la entidad o República Mexicana:', sorted(entidad_list, reverse=False))
    # df_selected_entidad = df_reshaped[df_reshaped.ENTIDAD == selected_entidad]
    # input_entidad = df_selected_entidad
    # df_selected_entidad_sorted = df_selected_entidad.sort_values(by="POBLACION", ascending=False)

    # # Género
    # genero_list = list(df_reshaped.SEXO.unique())
    # selected_genero = st.selectbox('Seleccione por género o datos totales:', sorted(genero_list, reverse=True))
    # df_selected_genero = df_reshaped[df_reshaped.SEXO == selected_genero]
    # input_genero = df_selected_genero
    # df_selected_genero_sorted = df_selected_genero.sort_values(by="POBLACION", ascending=False)

    with st.expander('Fuentes y tecnologías', expanded=False):
        st.write('''
            - Se basa un set de datos no representativo.
            - Tecnologías y lenguajes: Python 3.10, Streamlit 1.30.0, CSS 3.0, HTML5, Google Colab y GitHub. 
            - Autor: Gates-SX
            ''', unsafe_allow_html=True)

##############
# Día preferido #
##############

day_counts = df['day'].value_counts().reset_index()
day_counts.columns = ['day', 'count']

# Sort by day to have a consistent order
day_order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
day_counts['day'] = pd.Categorical(day_counts['day'], categories=day_order, ordered=True)
day_counts = day_counts.sort_values('day')

# Create a bar chart using Plotly
fig = px.bar(day_counts, x='day', y='count', title='¿Cuál es el día preferido para comer (Any time)?', labels={'count': 'Frequency', 'day': 'Day'})

# Update layout for a black background
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font_color='white',
    legend_title_font_color='white',
)

# Customize bars with rounded corners
fig.update_traces(marker=dict(line=dict(color='white', width=1.5), opacity=0.8))

# Add rounded corners to bars using cornerradius
for trace in fig.data:
    trace.marker.update(cornerradius=20)

# Show the plot
dia_todos = fig


######################
##### Dinner or lunch #######
######################

# Aggregate data by day and time
day_counts = df.groupby(['day', 'time']).size().reset_index(name='count')

# Sort by day to have a consistent order
day_order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
day_counts['day'] = pd.Categorical(day_counts['day'], categories=day_order, ordered=True)
day_counts = day_counts.sort_values(['day', 'time'])

# Create a bar chart using Plotly
fig = px.bar(day_counts, x='day', y='count', color='time',
             title='¿Cuál es el día preferido para comer?',
             labels={'count': 'Frecuencia', 'day': 'Día', 'time': 'Comida'},
             color_discrete_map={'Dinner': 'blue', 'Lunch': 'green'},
             barmode='group')  # Use 'group' to group bars

# Update layout for a black background
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font_color='white',
    legend_title_font_color='white',
)

# Customize bars with rounded corners
fig.update_traces(marker=dict(line=dict(color='white', width=1.5), opacity=0.8))

# Add rounded corners to bars using cornerradius
for trace in fig.data:
    trace.marker.update(cornerradius=10)

preferido_perday = fig

################
# quién paga mejor
################

# Aggregate data by day and sex
day_sex_counts = df.groupby(['day', 'sex']).size().reset_index(name='count')

# Sort by day to have a consistent order
day_order = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
day_sex_counts['day'] = pd.Categorical(day_sex_counts['day'], categories=day_order, ordered=True)
day_sex_counts = day_sex_counts.sort_values('day')

# Create a stacked bar chart using Plotly
fig3 = px.bar(
    day_sex_counts, 
    x='day', 
    y='count', 
    color='sex', 
    title='¿Qué días de la semana hay más pagadores hombres que mujeres?', 
    labels={'count': 'Frequency', 'day': 'Day'},
    barmode='stack',
    color_discrete_map={'Male': 'blue', 'Female': 'pink'}
)

# Update layout for a black background
fig3.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font_color='white',
    legend_title_font_color='white',
)

# Customize bars with rounded corners and adjust opacity
fig3.update_traces(marker=dict(line=dict(color='white', width=1.5), opacity=0.8, cornerradius=10))

# Show the plot
paga_mejor = fig3

######################33

# Pagadores fumadores
#######################3
fig5 = px.box(df, x='smoker', y='total_bill', points='all', color='smoker',
             title='¿Cree que los importes de las facturas cambian considerablemente según se fume?',
             labels={'smoker': 'Smoker', 'total_bill': 'Total Bill ($)'})

# Customize layout
fig5.update_layout(
    plot_bgcolor='black',  # Set plot background color
    paper_bgcolor='black',  # Set paper background color
    font_color='white',  # Set font color
)

# Show plot
box = fig5


# Group by day and time, calculate average total_bill
heatmap_data = df.groupby(['time', 'smoker'])['total_bill'].sum().reset_index()

# Pivot the data to prepare for heatmap
heatmap_data_pivot = heatmap_data.pivot(index='time', columns='smoker', values='total_bill')

# Create a heatmap using Plotly
fig4 = px.imshow(
    heatmap_data_pivot,
    labels=dict(x="Somoke?", y="Tipo de comida", color="Total Bill"),
    x=['No', 'Yes'],
    y=['Dinner', 'Lunch'],  # Order of days as you prefer
    color_continuous_scale='Viridis'  # Choose a colorscale
)

# Customize layout
fig4.update_layout(
    title='Cuenta total por Día y Fumar',
    plot_bgcolor='black',  # Set background color
    paper_bgcolor='black',  # Set background color
    font_color='white'  # Set font color
)

# Show plot

fumadores_tips = fig4

##############3
# correlación
################
# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(df['total_bill'], df['tip'])

# Calculate predicted values using the regression equation
df['tip_predicted'] = intercept + slope * df['total_bill']

# Calculate R-squared
r_squared = r_value**2

# Create scatter plot using Plotly Express
fig6 = px.scatter(df, x='total_bill', y='tip', color='smoker',
                 title=f'¿Está la propina correlacionada con la factura_total? (R²={r_squared:.2f})',
                 labels={'total_bill': 'Total Bill ($)', 'tip': 'Tip ($)'})

# Add regression line as a trace
fig6.add_trace(go.Scatter(x=df['total_bill'], y=df['tip_predicted'], mode='lines', 
                         name='Regression Line', line=dict(color='yellow', width=3)))

# Add equation of the line
equation = f'y = {slope:.2f}x + {intercept:.2f}'
fig6.add_annotation(
    x=0.95, y=0.05,
    xref='paper', yref='paper',
    text=equation,
    showarrow=False,
    font=dict(size=14, color='yellow'),
    bgcolor='black',
)

# Customize layout
fig6.update_layout(
    plot_bgcolor='black',  # Set plot background color
    paper_bgcolor='black',  # Set paper background color
    font_color='white',  # Set font color
)

# Show plot
correla = fig6    

title_size = "24px"

# Dashboard Main Panel
st.markdown("<h3 style='text-align: center; font-size: " + title_size + ";'>Preguntas de Negocio</h3>", unsafe_allow_html=True)# calculos_df
# Define the tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["¿Cuál es el día preferido para comer (Any time)?","¿Cuál es el día preferido para comer?", "¿Qué días de la semana hay más pagadores hombres que mujeres?","¿Cree que los importes de las facturas cambian considerablemente según se fume?", '¿Está la propina correlacionada con la factura_total?'])

# El histograma
with tab1:
    with st.expander('Respuesta', expanded=False):
        # st.markdown(f'La población de <span style="color:#C2185B">{variable_seleccionada}</span> seguirá enfrentando cambios radicales. La tasa de crecimiento anual en <span style="color:#C2185B">{}</span> es de <span style="color:#C2185B">{calculos_df.Crecimiento.iloc[0]:,.1f}%</span>.', unsafe_allow_html=True)
        st.markdown(f'La frecuencia con la que los comensales visitan el restaurante indica que el día preferido es <span style="color:#C2185B"> el sábado</span>, seguido por el domingo.', unsafe_allow_html=True)
    st.plotly_chart(dia_todos, use_container_width=True, height=500)

# El diagrama de caja
with tab2:
    with st.expander('Respuesta', expanded=False):
        # st.markdown(f'La población de <span style="color:#C2185B">{variable_seleccionada}</span> seguirá enfrentando cambios radicales. La tasa de crecimiento anual en <span style="color:#C2185B">{}</span> es de <span style="color:#C2185B">{calculos_df.Crecimiento.iloc[0]:,.1f}%</span>.', unsafe_allow_html=True)
        st.markdown(f'Si nos concentramos exclusivamente en el lunch time, los días preferidos son el <span style="color:#C2185B"> martes y el viernes </span>. Los días preferidos para ir a cenar por parte de los comensales son el sábado y domingo.', unsafe_allow_html=True)
        st.markdown(f'En general, el tipo de comensal que estamos analizando prefiere las cenas los fines de semana, como se puede ver en la gráfica.', unsafe_allow_html=True)
 
    st.plotly_chart(preferido_perday, use_container_width=True, height=500)

# La correlacion
with tab3:
    with st.expander('Respuesta', expanded=False):
        # st.markdown(f'La población de <span style="color:#C2185B">{variable_seleccionada}</span> seguirá enfrentando cambios radicales. La tasa de crecimiento anual en <span style="color:#C2185B">{}</span> es de <span style="color:#C2185B">{calculos_df.Crecimiento.iloc[0]:,.1f}%</span>.', unsafe_allow_html=True)
        st.markdown(f'<span style="color:#C2185B">Los sábados y domingos</span> son los que registran el mayor número de hombres que pagan la cuenta. El viernes podríamos decir que es balanceado aunque los hombres son 10 y las mujeres 9 comensales pagadores.', unsafe_allow_html=True)
        st.markdown(f'Como se puede ver en la gráfica apilada, las mujeres superan a los hombres como quienes pagan la cuenta los días martes y viernes.', unsafe_allow_html=True)
    st.plotly_chart(paga_mejor, use_container_width=True, height=500)

with tab4:
    with st.expander('Respuesta', expanded=False):
        st.markdown(f'Los comensales que fuman tienen una mayor dispersión en el importe de las facturas pagadas. Tomando en cuenta la mediana de la distribución, se puede ver que sus facturas son 33 centavos mayores en el caso de los fumadores (una diferencia marginal)', unsafe_allow_html=True)
        st.markdown(f'<span style="color:#C2185B">Los fumadores se van a los extremos más altos <span style="color:#C2185B">. Así como se registra la facturación máxima, también tienen la menor facturación.</span>', unsafe_allow_html=True)
        st.markdown(f'No obstante, observese el diagrama de calor.', unsafe_allow_html=True)

    st.plotly_chart(box, use_container_width=True, height=500)
    st.plotly_chart(fumadores_tips, use_container_width=True, height=500)

with tab5:
    with st.expander('Respuesta', expanded=False):
        # st.markdown(f'La población de <span style="color:#C2185B">{variable_seleccionada}</span> seguirá enfrentando cambios radicales. La tasa de crecimiento anual en <span style="color:#C2185B">{}</span> es de <span style="color:#C2185B">{calculos_df.Crecimiento.iloc[0]:,.1f}%</span>.', unsafe_allow_html=True)
        st.markdown(f'Hay una correlación positiva sin duda...', unsafe_allow_html=True)
    st.plotly_chart(correla, use_container_width=True, height=500)

