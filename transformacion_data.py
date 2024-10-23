import pandas as pd
import datetime

# Ruta del archivo CSV intermedio
fecha_actual = datetime.datetime.now()
# Formatear la fecha en el formato _YYYYMMDD
fecha_desglosada = fecha_actual.strftime("%Y%m%d")

archivo_csv = 'resultado_consulta.csv'

try:
    # Leer el archivo CSV
    data = pd.read_csv(archivo_csv)
       
    data['Tardanza'] = data.apply(lambda row: 'Si' if row['Hora Marcación Entrada'] > row['Hora de Ingreso'] else '', axis=1)
    data['Minutos_tardanza'] = data.apply(
        lambda row: (pd.to_datetime(str(row['Hora Marcación Entrada'])) - pd.to_datetime(str(row['Hora de Ingreso']))).seconds // 60 
        if row['Tardanza'] == 'Si' else 0, axis=1
    )
    
    # Exportar a Excel
    archivo_excel = 'Reporte_asistencia_' + fecha_desglosada + '.xlsx'
    data.to_excel(archivo_excel, index=False)
    
    print(f"Datos exportados exitosamente a {archivo_excel}")
except Exception as e:
    print(f"Error al transformar los datos: {e}")