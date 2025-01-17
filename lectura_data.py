from conexion import obtener_conexion
import pandas as pd


conexion =  obtener_conexion() # Obtener la conexión
if conexion is not None:
    try:
        consulta = """
        SELECT 
            em.co_emplea, 
            em.no_emplea, 
            cl.no_carlab, 
            ar.no_arelab, 
            (
                CASE
                    WHEN ho.hr_ingman IS NULL THEN ho.hr_ingtar
                    ELSE ho.hr_ingman
                END
            ) AS ho_inglab, 
            (
                CASE
                    WHEN ho.hr_salman IS NULL THEN ho.hr_saltar
                    ELSE ho.hr_salman
                END
            ) AS ho_sallab, 
            ca.fe_regist,
            ca.fe_entasi::time,
            ca.fe_salasi::time,(
				case
					when pe.ti_permis = 'H' then 'Permiso por Horas'
					when pe.ti_permis = 'D' then 'Permiso por Día'
				end
			) ti_permis,
			mp.no_motper,
			jd.no_emplea no_jefdir
        FROM 
            wfgeshum.tbconasi ca
        JOIN 
            wfgeshum.tbemplea em ON ca.co_emplea = em.co_emplea
		LEFT JOIN 
			wfgeshum.tbpermis pe on em.co_emplea = pe.co_emplea and ca.fe_regist >= pe.fe_iniper and ca.fe_regist <= pe.fe_finper
		LEFT JOIN 
			wfgeshum.tcmotper mp on pe.co_motper = mp.co_motper
        JOIN 
            wfgeshum.tccarlab cl ON em.co_carlab = cl.co_carlab
        JOIN 
            wfgeshum.tcarelab ar ON em.co_arelab = ar.co_arelab
        JOIN 
            wfgeshum.tchorari ho ON em.co_horari = ho.co_horari
		JOIN
			wfgeshum.tbemplea jd ON em.co_jefdir = jd.co_emplea
        WHERE 
            ca.fe_entasi::date = '2023-11-24'
            AND em.il_estado = true;
        """
        
        # Leer la consulta en un DataFrame de pandas
        df = pd.read_sql_query(consulta, conexion)

        df = df.rename(columns={'co_emplea': 'Código'})
        df = df.rename(columns={'no_emplea': 'Nombre'})
        df = df.rename(columns={'no_carlab': 'Cargo'})
        df = df.rename(columns={'no_arelab': 'Área'})
        df = df.rename(columns={'ho_inglab': 'Hora de Ingreso'})
        df = df.rename(columns={'ho_sallab': 'Hora de Salida'})
        df = df.rename(columns={'fe_regist': 'Fecha Marcación'})
        df = df.rename(columns={'fe_entasi': 'Hora Marcación Entrada'})
        df = df.rename(columns={'fe_salasi': 'Hora Marcación Salida'})
        df = df.rename(columns={'ti_permis': 'Tipo de Permiso'})
        df = df.rename(columns={'no_motper': 'Motivo de Permiso'})
        df = df.rename(columns={'no_jefdir': 'Jefe Directo'})
        
        
        # Guardar el DataFrame en un archivo CSV
        df.to_csv('resultado_consulta.csv', index=False, encoding='utf-8')
        # Guardar el DataFrame en un archivo EXCEL
        #df.to_excel('resultado_consulta.xlsx', index=False, engine='openpyxl')

        print("Consulta guardada en 'resultado_consulta.csv'")

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")

    finally:
        conexion.close()  # Asegúrate de cerrar la conexión