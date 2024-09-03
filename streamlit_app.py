import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
import base64

# 2. Desplegar el logotipo de la empresa centrado y redimensionado
def display_image(image_path, width=200):
    # Abrir la imagen y convertirla a base64
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
        img_b64 = base64.b64encode(img_bytes).decode()
    
    # Mostrar la imagen centrada y redimensionada usando st.markdown
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{img_b64}' style='width:{width}px;'>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Llama a la función para mostrar la imagen
display_image('socialize-people-logo.png', width=200)


# Función para centrar texto en Streamlit
def center_text(text, font_size='16px', is_title=False):
    """
    Centra el texto en Streamlit usando Markdown y un cuadro vacío.

    Args:
    - text (str): El texto a mostrar.
    - font_size (str): Tamaño de la fuente (opcional).
    - is_title (bool): Si es un título (h1) o no.
    """
    if is_title:
        st.write(f"<h1 style='text-align: center; font-size: {font_size};'>{text}</h1>", unsafe_allow_html=True)
    else:
        st.write(f"<h3 style='text-align: center; font-size: {font_size};'>{text}</h3>", unsafe_allow_html=True)

# 1. Despliegue del título y la breve descripción de la aplicación web
center_text('Desempeño de empleados', font_size='36px', is_title=True)
center_text('Aplicación web para análisis de desempeño, así como los KPI’s de los empleados, con la finalidad de que sean consultados por los colaboradores de manera práctica y sencilla, lo que permitirá identificar sus fortalezas y áreas de oportunidad, y así lograr mejorar su rendimiento y obtener mayor calidad en sus servicios.', font_size='16px')

# 3. Carga de datos
empleados = pd.read_csv('Employee_data.csv')
empleados = empleados[['name_employee', 'birth_date', 'age', 'gender', 'marital_status', 'hiring_date', 'position',
                       'salary', 'performance_score', 'last_performance_date', 'average_work_hours', 'satisfaction_level', 'absences']]

# 4. Control para seleccionar el género del empleado 
generos = ['Todos'] + empleados['gender'].unique().tolist()
genero_seleccionado = st.sidebar.radio('Seleccionar género:', options=generos, index=0)

if genero_seleccionado != 'Todos':
    empleados_filtrados = empleados[empleados['gender'] == genero_seleccionado]
else:
    empleados_filtrados = empleados

# 5. Control para seleccionar un rango del puntaje de desempeño del empleado
minScore = empleados_filtrados['performance_score'].min()
maxScore = empleados_filtrados['performance_score'].max()
rango_puntuacion = st.sidebar.slider('Seleccionar rango de puntaje de desempeño:', 
                                     min_value=int(minScore), max_value=int(maxScore), 
                                     value=[int(minScore), int(maxScore)])
empleados_filtrados = empleados_filtrados[(empleados_filtrados['performance_score'] >= rango_puntuacion[0]) & 
                                          (empleados_filtrados['performance_score'] <= rango_puntuacion[1])]

# 6. Control para seleccionar el estado civil del empleado 
estados_civiles = ['Todos'] + empleados_filtrados['marital_status'].unique().tolist()
estado_civil_seleccionado = st.sidebar.radio('Seleccionar estado civil:', options=estados_civiles, index=0)

if estado_civil_seleccionado != 'Todos':
    empleados_filtrados = empleados_filtrados[empleados_filtrados['marital_status'] == estado_civil_seleccionado]

# 7. Control para aplicar o no los filtros (Aplica a todos los controles de filtro)
filtros_aplicados = st.sidebar.checkbox('Aplicar filtros', key="filtros")
if filtros_aplicados:
    st.dataframe(empleados_filtrados)
else:
    st.dataframe(empleados)

# 8. Grafico: Distribución de los puntajes de desempeño 
chart1 = alt.Chart(empleados_filtrados).mark_bar().encode(
    x=alt.X('performance_score:O', axis=alt.Axis(title='Puntaje de Desempeño', labelAngle=0)),
    y=alt.Y('count()', axis=alt.Axis(title='Cantidad de Empleados')),
).properties(
    title='Distribución de Puntajes de Desempeño (1-4)'
)
st.altair_chart(chart1, use_container_width=True)

# 9. Gráfico: Promedio de horas trabajadas por género
hrs_empleado = empleados_filtrados.groupby(['gender'], as_index=False)['average_work_hours'].mean()
chart2 = alt.Chart(hrs_empleado).mark_arc().encode(
    theta=alt.Theta(field="average_work_hours", type="quantitative"),
    color=alt.Color(field="gender", type="nominal"),
    tooltip=[alt.Tooltip("gender:N", title="Género"), alt.Tooltip("average_work_hours:Q", title="Horas Promedio")]
).properties(
    title='Promedio de Horas Trabajadas por Género'
)
st.altair_chart(chart2, use_container_width=True)

# 10. Gráfico: Relación entre edad y salario
chart3 = alt.Chart(empleados_filtrados).mark_point(filled=True).encode(
    x='age',
    y='salary'
).properties(
    title='Relación Edad vs Salario'
)
st.altair_chart(chart3, use_container_width=True)

# 11. Gráfico: Relación entre horas trabajadas y desempeño
chart4 = alt.Chart(empleados_filtrados).mark_point(filled=True).encode(
    x=alt.X('performance_score:O', axis=alt.Axis(title='Puntaje de Desempeño', values=[1, 2, 3, 4])),  # Asegura valores enteros en el eje X
    y='average_work_hours'
).properties(
    title='Relación Horas Trabajadas vs Puntaje de Desempeño'
)
st.altair_chart(chart4, use_container_width=True)

# 12. Conclusión sobre el análisis mostrado
st.markdown('**CONCLUSIÓN**')
st.text('Unicamente 37 empleados de 311 obtuvieron un desempeño de 4. Las mujeres \n'
        'trabajan en promedio 26 horas más que los hombres. En general no se observo \n'
        'una tendencia entre desempeño , ni edad, ni salario, aunque si existen \n'
        'mayores salarios en promedio a los hombres que a las mujeres. Por ultimo  \n'
        'se observa que los que tienen desempeño de 3 llegan a trabajar mas que \n'
        'los de mayor desempeño por lo que las horas trabajadas no es lo mas importante.')

# Información adicional del autor
st.text('Reto: Conociendo el desempeño de los colaboradores del Área de Marketing \n' 
        'de Socialize your Knowledge \n'
        'Autor: Eduardo Frias Rosales')
