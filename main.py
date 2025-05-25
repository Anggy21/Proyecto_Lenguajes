import streamlit as st
from PIL import Image

st.set_page_config(page_title="Storytelling del Proyecto", layout="wide")

# Título
st.title("🧾 Storytelling del Proyecto: Digitalización Inteligente de Facturas")

# Presentación del equipo
with st.expander("👩‍💻 Integrantes del proyecto"):
    st.markdown("""
    **Anggy Michelle Marin Alfonso**  
    - 📘 Cod: `160004521`  
    - 🎓 Ingeniería de Sistemas

    **Jhonnathan Stiven Villarraga Ariza**  
    - 📘 Cod: `160004546`  
    - 🎓 Ingeniería de Sistemas

    **Luis Alfonso Medina Romero**  
    - 📘 Cod: `160004146`  
    - 🎓 Ingeniería de Sistemas
    """)

st.markdown("---")

# Sección 1 - Contexto emocional
st.subheader("👨‍👧 Un problema cotidiano, una solución tecnológica")
col1, col2 = st.columns([1, 1])

with col1:
    st.write("""
    Cada mañana, mi papá comienza su jornada anotando cuentas en su negocio.  
    Recibe facturas, las revisa y luego, **dato por dato**, las transcribe manualmente en una hoja de Excel.

    Un proceso que consume tiempo, esfuerzo y que está expuesto a errores humanos.

    Desde esa realidad cotidiana nace este proyecto:  
    **¿Y si una simple foto o PDF pudiera hacer todo ese trabajo por él?**
    """)

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/3515/3515333.png", width=300, caption="Ejemplo de digitalización")

st.markdown("---")

# Sección 2 - La idea
st.subheader("💡 La idea: Automatizar lo que mi papá hacía manualmente")
st.info("""
Que con una imagen o PDF de la factura, el sistema:
1. Extraiga el texto automáticamente.
2. Identifique la información clave.
3. Genere un script SQL para insertar todo en la base de datos.
""")

st.markdown("---")

# Sección 3 - ¿Cómo lo hicimos?
st.subheader("⚙️ ¿Cómo lo desarrollamos?")
st.write("Usamos tecnologías accesibles pero poderosas:")

tec1, tec2, tec3 = st.columns(3)
with tec1:
    st.markdown("🐍 **Python**  \nPara todo el procesamiento backend")
with tec2:
    st.markdown("📄 **pdfplumber**  \nPara extraer texto directamente desde archivos PDF")
with tec3:
    st.markdown("🔤 **EasyOCR**  \nPara leer texto desde imágenes (.png, .jpg)")

st.markdown("Además, usamos **Expresiones Regulares** para identificar campos clave y **Streamlit** para crear una interfaz web interactiva.")
st.success("✅ Soporta archivos: `.jpg`, `.png`, `.pdf`")

st.markdown("---")

# Sección 4 - ¿Qué hace el sistema?
st.subheader("🧠 ¿Qué hace el sistema paso a paso?")
with st.expander("🔍 Paso 1: Lectura del contenido"):
    st.write("El sistema detecta el tipo de archivo:")
    st.markdown("""
    - Si es **PDF**, usa `pdfplumber` para leer el texto directamente.  
    - Si es **imagen**, usa easyOCR para reconocer el texto.
    """)

with st.expander("🧩 Paso 2: Extracción de datos"):
    st.write("A través de expresiones regulares, identifica y extrae:")
    st.markdown("""
    - Cliente, Cédula, Dirección  
    - NIT de la empresa emisora  
    - Ítems vendidos con descripción, cantidad y precio  
    - Subtotal, IVA y Total
    """)

with st.expander("🧾 Paso 3: Generación del SQL"):
    st.write("Se genera un script SQL con:")
    st.markdown("""
    - `CREATE TABLE IF NOT EXISTS`  
    - `INSERT INTO` con los datos extraídos  
    - Listo para ser descargado y ejecutado en la base de datos
    """)

st.markdown("---")

# Sección final - Cierre
st.subheader("🌟 Impacto")
st.write("""
Este proyecto no solo resuelve un problema personal.  
Tiene el potencial de ser útil para cualquier negocio pequeño que maneje facturas físicas o PDFs.

**Digitalizar procesos puede transformar realidades cotidianas.**
""")

st.success("💙 Gracias por su atención.")

