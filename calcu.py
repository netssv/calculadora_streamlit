#reglas de la calculadora de retenciones salariales
#ISSS
#Empleado: 3% (máximo $30.00)
#Empleador: 7.5%
###AFP
#Empleado: 7.25%
#Empleador: 7.75%
#Impuesto Sobre la Renta (ISR)
#Tramo I: $0.01 - $472.00 - Sin ret
#Tramo II: $472.01 - $895.24 - 10% sobre el exceso de $472.00
#Tramo III: $895.25 - $2,038.10 - 20% sobre el exceso de $895.24
#Tramo IV: $2,038.11 en adelante - 30% sobre el exceso de $2,038.10
#Ejemplo de cálculo
#Salario: $1,000.00
#ISSS Empleado: $30.00
#AFP Empleado: $72.50
#Salario aplicable ISR: $897.50
#ISR: $60.00
#Salario Líquido: $837.50

import streamlit as st #importar la libreria de streamlit para la interfaz
import pandas as pd #importar la libreria de pandas para el manejo de datos en tablas

# Configuración de página
st.set_page_config(
    page_title="Calculadora de Retenciones 2024",
    page_icon="💵",
    layout="wide"
)

# Inicializar el estado del campo de texto
if "salario_input" not in st.session_state:
    st.session_state.salario_input = ""  # Para el campo de salario
    st.session_state.resultados = None  # Para almacenar los resultados de los cálculos

def reset_form():
    """Restablece el formulario dejando el campo de salario en blanco y eliminando los resultados."""
    st.session_state.salario_input = "" # Restablecer el campo de salario
    st.session_state.resultados = None # Eliminar los resultados

# Funciones para cálculos
def determinar_tramo(salario_menos_afp): #funcion para determinar el tramo de renta
    """Determina el tramo de renta según el salario"""
    if salario_menos_afp <= 472.00:
        return "Tramo I (Sin Retención)"
    elif salario_menos_afp <= 895.24:
        return "Tramo II (10%)"
    elif salario_menos_afp <= 2038.10:
        return "Tramo III (20%)"
    else:
        return "Tramo IV (30%)"

def calcular_deducciones(salario): #funcion para calcular las deducciones
    """Calcula todas las deducciones y retorna un diccionario con los resultados"""
    afp_patronal = salario * 0.0775 #calculo de la afp patronal
    afp_laboral = salario * 0.0725 #calculo de la afp laboral
    
    isss_laboral = min(salario * 0.03, 30.00) #calculo del isss laboral
    isss_patronal = salario * 0.075 #calculo del isss patronal
    
    salario_menos_afp = salario - afp_laboral - isss_laboral #calculo del salario menos afp y isss
    
    tramo = determinar_tramo(salario_menos_afp) #determinar el tramo de renta al que pertenece el salario
    
    if salario_menos_afp <= 472.00: #calculo del isr segun el tramo
        isr = 0 #si el salario es menor o igual a 472.00 no se retiene isr 
    elif salario_menos_afp <= 895.24: #si el salario es menor o igual a 895.24 se retiene el 10% sobre el exceso de 472.00
        exceso = salario_menos_afp - 472.00 #
        isr = (exceso * 0.10) + 17.67
    elif salario_menos_afp <= 2038.10: #si el salario es menor o igual a 2038.10 se retiene el 20% sobre el exceso de 895.24
        exceso = salario_menos_afp - 895.24
        isr = (exceso * 0.20) + 60.00 
    else:
        exceso = salario_menos_afp - 2038.10 #si el salario es mayor a 2038.10 se retiene el 30% sobre el exceso de 2038.10
        isr = (exceso * 0.30) + 288.57
    
    descuento_total = afp_laboral + isss_laboral + isr #calculo del descuento total que se le hace al salario
    salario_liquido = salario - descuento_total #calculo del salario liquido que recibe el empleado
    
    return { #retorna un diccionario con los resultados de las deducciones
        'salario_base': salario,
        'afp_patronal': afp_patronal,
        'isss_patronal': isss_patronal,
        'isss_laboral': isss_laboral,
        'afp_laboral': afp_laboral,
        'salario_menos_afp': salario_menos_afp,
        'descuento_total': descuento_total,
        'isr': isr,
        'salario_liquido': salario_liquido,
        'tramo': tramo
    }

# Interfaz principal con tabs
st.write("## 💵 Calculadora de Retenciones Salariales 2024")

# Usar tabs en lugar de sidebar
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Calculadora",
    "📜 Legislación",
    "👨‍💻 Código",
    "📧 Contacto"
])

with tab1:
    st.header("📊 Calcula tu salario líquido")
    
    # form para solucionar submit con Enter
    with st.form(key='calculadora_form'): #formulario para ingresar el salario
        salario_input = st.text_input( #campo de texto para ingresar el salario
            "Ingresa tu salario mensual ($):",
            key="salario_input", #clave para guardar el valor del campo de texto
            placeholder="Ejemplo: 1000.00" #texto de ejemplo en el campo de texto
        )
        
        col_btn1, col_btn2 = st.columns(2) # Botones en dos columnas para centrar
        with col_btn1: #boton para calcular el salario
            submit_button = st.form_submit_button("💰 Calcular")
        with col_btn2: #boton para borrar el formulario
            clear_button = st.form_submit_button("🗑️ Borrar", on_click=reset_form) #al hacer click manda a la variable reset form

    # Errores personalizados 
    if submit_button:
        if not salario_input.strip(): #si no se ingresa nada en el campo de salario
            st.error("⚠️ Por favor, ingresa el salario a calcular")
        else:
            try:
                salario = float(salario_input) #convertir el salario ingresado a un numero flotante
                if salario < 0: #si el salario es negativo
                    st.error("⚠️ El salario no puede ser negativo") #mostrar un mensaje de error
                else:
                    resultados = calcular_deducciones(salario) #calcular las deducciones del salario
                    
                    # Mostrar el tramo de ISR al que pertenece el salario
                    st.info(f"📊 Tu salario está en el: **{resultados['tramo']}**")
                    
                    # Crear DataFrame con todos los resultados
                    datos = {
                        'Concepto': [
                            'Salario Base',
                            'AFP Patronal (7.75%)',
                            'ISSS Patronal (7.5%)',
                            'ISSS Laboral (3%)',
                            'AFP Laboral (7.25%)',
                            'Salario menos AFP y ISSS',
                            'Descuento Total',
                            'Impuesto sobre la Renta',
                            'Salario Líquido'
                        ],
                        'Monto': [
                            f"${resultados['salario_base']:.2f}",
                            f"${resultados['afp_patronal']:.2f}",
                            f"${resultados['isss_patronal']:.2f}",
                            f"${resultados['isss_laboral']:.2f}",
                            f"${resultados['afp_laboral']:.2f}",
                            f"${resultados['salario_menos_afp']:.2f}",
                            f"${resultados['descuento_total']:.2f}",
                            f"${resultados['isr']:.2f}",
                            f"${resultados['salario_liquido']:.2f}"
                        ]
                    }
                    
                    df = pd.DataFrame(datos)
                    st.dataframe(df, hide_index=True)
                                        
                    # Mostrar costo total para el empleador
                    costo_empleador = resultados['salario_base'] + resultados['afp_patronal'] + resultados['isss_patronal']
                    st.info(f"💼 **Costo total para el empleador:** ${costo_empleador:.2f}")
                    
            except ValueError:
                st.error("⚠️ Por favor, ingresa solo números y punto decimal")

    # Si se presiona borrar, recargar la página
    if clear_button:
        st.rerun()

with tab2:
    st.header("📜 Legislación")
    
    # Tabla completa de tramos ISR
    st.subheader("Tabla de Tramos ISR 2024")
    data_tramos = {
        'Tramo': ['I', 'II', 'III', 'IV'],
        'Desde': ['$0.01', '$472.01', '$895.25', '$2,038.11'],
        'Hasta': ['$472.00', '$895.24', '$2,038.10', 'En adelante'],
        'Porcentaje': ['Sin Retención', '10%', '20%', '30%'],
        'Sobre exceso de': ['-', '$472.00', '$895.24', '$2,038.10'],
        'Cuota Fija': ['$0.00', '$17.67', '$60.00', '$288.57']
    }
    df_tramos = pd.DataFrame(data_tramos)
    st.table(df_tramos)
    
    st.subheader("Porcentajes de Retención")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ISSS")
        st.write("- Empleado: 3% (máximo $30.00)")
        st.write("- Empleador: 7.5%")
    
    with col2:
        st.markdown("#### AFP")
        st.write("- Empleado: 7.25%")
        st.write("- Empleador: 7.75%")

with tab3:
    st.header("👨‍💻 Código")
    st.write("### Características principales:")
    st.write("- ✨ Cálculo preciso de retenciones")
    st.write("- 📊 Deteccion de tramos al que pertenece el salario")
    st.write("- 🔒 Validación de datos")
    st.write("- 📱 Diseño adaptable")
    st.write("- 📦 Fácil de usar")
    st.write("- 💻 Descaga de la tabla en CSV")

with tab4:
    st.header("📧 Contacto")
    st.write("### Información de contacto")
    st.write("👨‍💻 **Autor:** Rodrigo Martel")
    st.write("📧 **Email:** netss.sv@gmail.com")
    st.write("🌐 **GitHub:** [Repositorio en GitHub](https://github.com/netssv/calculadora_streamlit)")

st.markdown("---")
st.write("© 2024 Calculadora de Retenciones Salariales | Desarrollado por Rodrigo Martel")