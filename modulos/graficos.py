import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from modulos.archivo import cargar_desde_csv
from colorama import Fore, Style
import emoji
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Configuración inicial de estilos (CORREGIDO)
sns.set_style("whitegrid")  # Estilo moderno equivalente
plt.style.use('default')    # Usamos el estilo por defecto y personalizamos con Seaborn
sns.set_palette("pastel")

def graficar_datos(usuario):
    """
    Genera visualizaciones profesionales de datos biomédicos.
    
    Args:
        usuario (str): Nombre de usuario para cargar los datos correspondientes
    """
    try:
        datos = cargar_desde_csv(usuario)
        if not datos:
            print(Fore.YELLOW + emoji.emojize("\U0001F50D No hay datos para generar gráficos."))
            return

        columnas = ["ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", "IMC", 
                    "Presión Sistólica", "Presión Diastólica"]
        df = pd.DataFrame(datos, columns=columnas)
        
        # Configurar tamaño de figura base
        plt.rcParams['figure.figsize'] = [12, 6]
        
        while True:
            print(Fore.CYAN + "\n=== MENÚ DE GRÁFICOS ===")
            print("1. Análisis de IMC")
            print("2. Comparación de Alturas")
            print("3. Distribución de Pesos")
            print("4. Presiones Arteriales")
            print("5. Gráfico Combinado")
            print("6. Salir")
            
            seleccion = input(Fore.YELLOW + "\nElija una opción: ").strip()
            
            if seleccion == "1":
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.histplot(data=df, x='IMC', bins=15, kde=True, color='royalblue')
                ax.set_title('Distribución de IMC', pad=20)
                ax.set_xlabel('IMC')
                ax.set_ylabel('Frecuencia')
                plt.axvline(x=18.5, color='red', linestyle='--', label='Bajo peso')
                plt.axvline(x=25, color='green', linestyle='--', label='Normal')
                plt.axvline(x=30, color='orange', linestyle='--', label='Sobrepeso')
                plt.legend()
                plt.tight_layout()
                plt.savefig(f'grafico_imc_{usuario}.png', dpi=300, bbox_inches='tight')
                
            elif seleccion == "2":
                plt.figure(figsize=(10, 6))
                barplot = sns.barplot(data=df, x='Nombre', y='Estatura (m)', palette='viridis')
                plt.title('Altura de Estudiantes', pad=20)
                plt.xlabel('Estudiante')
                plt.ylabel('Estatura (metros)')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(f'grafico_alturas_{usuario}.png', dpi=300, bbox_inches='tight')
                
            elif seleccion == "3":
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.boxplot(data=df, y='Peso (kg)', color='lightcoral')
                ax.set_title('Distribución de Pesos', pad=20)
                ax.set_ylabel('Peso (kg)')
                plt.tight_layout()
                plt.savefig(f'grafico_pesos_{usuario}.png', dpi=300, bbox_inches='tight')
                
            elif seleccion == "4":
                plt.figure(figsize=(12, 6))
                df_melt = df.melt(id_vars=['Nombre'], 
                                  value_vars=['Presión Sistólica', 'Presión Diastólica'],
                                  var_name='Tipo', 
                                  value_name='Presión')
                sns.barplot(data=df_melt, x='Nombre', y='Presión', hue='Tipo')
                plt.title('Presiones Arteriales', pad=20)
                plt.xlabel('Estudiante')
                plt.ylabel('Presión (mm Hg)')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(f'grafico_presiones_{usuario}.png', dpi=300, bbox_inches='tight')
                
            elif seleccion == "5":
                # Seleccionamos solo columnas numéricas para el análisis
                columnas_numericas = ['Edad', 'Peso (kg)', 'Estatura (m)', 'IMC', 
                                      'Presión Sistólica', 'Presión Diastólica']
                df_numerico = df[columnas_numericas]
                
                fig, axes = plt.subplots(2, 2, figsize=(14, 10))
                
                # Gráfico 1: Dispersión Peso vs Altura
                sns.scatterplot(data=df, x='Estatura (m)', y='Peso (kg)', 
                                hue='Edad', size='Edad', sizes=(20, 200),
                                palette='viridis', ax=axes[0, 0])
                axes[0, 0].set_title('Peso vs Estatura (Color por Edad)')
                
                # Gráfico 2: Distribución IMC
                sns.histplot(data=df, x='IMC', kde=True, bins=15, 
                             color='skyblue', ax=axes[0, 1])
                axes[0, 1].axvline(x=18.5, color='red', linestyle='--')
                axes[0, 1].axvline(x=25, color='green', linestyle='--')
                axes[0, 1].axvline(x=30, color='orange', linestyle='--')
                axes[0, 1].set_title('Distribución de IMC')
                
                # Gráfico 3: Boxplot de Presiones
                sns.boxplot(data=df[['Presión Sistólica', 'Presión Diastólica']], 
                            palette=['lightcoral', 'lightblue'], ax=axes[1, 0])
                axes[1, 0].set_title('Distribución de Presiones')
                axes[1, 0].set_ylabel('mm Hg')
                
                # Gráfico 4: Mapa de Correlación (solo datos numéricos)
                sns.heatmap(df_numerico.corr(), annot=True, cmap='coolwarm', 
                            fmt=".2f", center=0, ax=axes[1, 1])
                axes[1, 1].set_title('Correlación entre Variables')
                
                plt.tight_layout()
                plt.savefig(f'grafico_combinado_{usuario}.png', dpi=300, bbox_inches='tight')
                plt.show()

            elif seleccion == "6":
                break
                
            else:
                print(Fore.RED + "Opción no válida. Intente nuevamente.")
                continue
            
            plt.show()
            print(Fore.GREEN + f"\nGráfico generado: grafico_*.png")
            
    except Exception as e:
        print(Fore.RED + f"Error al generar gráficos: {str(e)}")
    finally:
        plt.close('all')
