import pandas as pd
import numpy as np
from colorama import Fore, Style
import emoji
from modulos.archivo import cargar_desde_csv

# Configuración de categorías
CATEGORIAS_IMC = {
    (0, 18.5): "Bajo peso",
    (18.5, 24.9): "Normal",
    (25, 29.9): "Sobrepeso",
    (30, 100): "Obesidad"
}

CATEGORIAS_PRESION = {
    (0, 120, 0, 80): "Óptima",
    (120, 129, 80, 84): "Normal",
    (130, 139, 85, 89): "Normal alta",
    (140, 1000, 90, 1000): "Hipertensión",
    (None, None, None, None): "No medida"
}

def _crear_dataframe(usuario):
    """Crea y retorna un DataFrame con los datos del usuario."""
    datos = cargar_desde_csv(usuario)
    if not datos:
        print(Fore.YELLOW + emoji.emojize("\U0001F50D No hay datos registrados."))
        return None
    
    columnas = [
        "ID", "Nombre", "Edad", "Peso (kg)", "Estatura (m)", 
        "IMC", "Presión Sistólica", "Presión Diastólica"
    ]
    return pd.DataFrame(datos, columns=columnas)

def _formatear_salida(df, columnas, titulo):
    """Formatea la salida para mejor visualización."""
    print(Fore.CYAN + emoji.emojize(f"\U0001F4C8 {titulo}"))
    print(Style.RESET_ALL)
    print(df[columnas].to_string(index=False))
    print("\n" + "="*50 + "\n")

def clasificar_imc(usuario):
    """Clasifica a los estudiantes según su IMC con estadísticas."""
    df = _crear_dataframe(usuario)
    if df is None: 
        return
    
    # Clasificación detallada
    condiciones = [
        (df['IMC'] < 18.5),
        (df['IMC'] < 24.9),
        (df['IMC'] < 29.9),
        (df['IMC'] >= 30)
    ]
    categorias = ["Bajo peso", "Normal", "Sobrepeso", "Obesidad"]
    df['Categoría IMC'] = pd.cut(df['IMC'], bins=[0, 18.5, 25, 30, 100], labels=categorias)
    
    # Estadísticas
    estadisticas = df['Categoría IMC'].value_counts().reset_index()
    estadisticas.columns = ['Categoría', 'Cantidad']
    estadisticas['Porcentaje'] = (estadisticas['Cantidad'] / len(df)) * 100
    
    # Salida formateada
    _formatear_salida(df, ['Nombre', 'IMC', 'Categoría IMC'], "Clasificación de IMC")
    
    print(Fore.GREEN + "Resumen estadístico:")
    print(estadisticas.to_string(index=False))
    print(f"\nIMC Promedio: {df['IMC'].mean():.1f}")

def altura_extremos(usuario):
    """Muestra los extremos de altura con análisis comparativo."""
    df = _crear_dataframe(usuario)
    if df is None: 
        return
    
    df = df.sort_values('Estatura (m)')
    promedio = df['Estatura (m)'].mean()
    
    print(Fore.CYAN + "\nANÁLISIS DE ALTURAS")
    print(f"Altura promedio: {promedio:.2f}m")
    print("-"*40)
    
    # Extremos
    mayor_idx = df['Estatura (m)'].idxmax()
    menor_idx = df['Estatura (m)'].idxmin()
    
    for extremo, idx in zip(["MAYOR ALTURA", "MENOR ALTURA"], [mayor_idx, menor_idx]):
        estudiante = df.loc[idx]
        diff = (estudiante['Estatura (m)'] - promedio) / promedio * 100
        print(Fore.YELLOW + f"\n{extremo}:")
        print(f"Nombre: {estudiante['Nombre']}")
        print(f"Altura: {estudiante['Estatura (m)']:.2f}m ({diff:+.1f}% vs promedio)")
        print(f"Edad: {estudiante['Edad']} años | Peso: {estudiante['Peso (kg)']}kg")

def peso_extremos(usuario):
    """Muestra los extremos de peso con contexto nutricional."""
    df = _crear_dataframe(usuario)
    if df is None: 
        return
    
    df = df.sort_values('Peso (kg)')
    promedio = df['Peso (kg)'].mean()
    
    print(Fore.CYAN + "\nANÁLISIS DE PESOS")
    print(f"Peso promedio: {promedio:.1f}kg")
    print("-"*40)
    
    # Extremos con IMC
    mayor_idx = df['Peso (kg)'].idxmax()
    menor_idx = df['Peso (kg)'].idxmin()
    
    for extremo, idx in zip(["MAYOR PESO", "MENOR PESO"], [mayor_idx, menor_idx]):
        estudiante = df.loc[idx]
        print(Fore.YELLOW + f"\n{extremo}:")
        print(f"Nombre: {estudiante['Nombre']}")
        print(f"Peso: {estudiante['Peso (kg)']}kg | IMC: {estudiante['IMC']:.1f}")
        print(f"Altura: {estudiante['Estatura (m)']:.2f}m | Edad: {estudiante['Edad']} años")

def analizar_presion_arterial(usuario):
    """Analiza presión arterial con clasificación clínica."""
    df = _crear_dataframe(usuario)
    if df is None: 
        return
    
    # Clasificación profesional
    condiciones = [
        (df['Presión Sistólica'] < 120) & (df['Presión Diastólica'] < 80),
        (df['Presión Sistólica'] < 130) & (df['Presión Diastólica'] < 85),
        (df['Presión Sistólica'] < 140) & (df['Presión Diastólica'] < 90),
        (df['Presión Sistólica'] >= 140) | (df['Presión Diastólica'] >= 90),
        (df['Presión Sistólica'].isna()) | (df['Presión Diastólica'].isna())
    ]
    categorias = ["Óptima", "Normal", "Normal alta", "Hipertensión", "No medida"]
    df['Estado presión'] = np.select(condiciones, categorias, default="Error")
    
    # Estadísticas
    stats = df['Estado presión'].value_counts(normalize=True).mul(100).round(1)
    
    # Salida
    _formatear_salida(df, ['Nombre', 'Presión Sistólica', 'Presión Diastólica', 'Estado presión'], 
                     "Estado de Presión Arterial")
    
    print(Fore.GREEN + "Distribución (%):")
    print(stats.to_string())
    print(f"\nPresión promedio: {df['Presión Sistólica'].mean():.0f}/{df['Presión Diastólica'].mean():.0f}")