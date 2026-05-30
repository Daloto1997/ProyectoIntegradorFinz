"""
Servidor Flask - API de Analítica FinzPlus
Genera gráficas en memoria y las devuelve como imágenes base64 para el frontend React.
Puerto: 5001
"""

import io
import re
import base64

# matplotlib.use('Agg') debe ir ANTES de importar pyplot (modo sin pantalla, para servidores)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS

# Funciones de datos: consumo real de la API de Spring Boot
from notebook.consumir_metas import consumir_metas
from notebook.consumir_deudas import consumir_deudas
from notebook.consumir_transacciones import consumir_transacciones
from notebook.consumir_usuarios import consumir_usuarios

# Fallback de simulación si el backend no responde
from utils.simularcuentas import generar_metas, generar_deudas
from utils.simulacion_transacciones import generar_transacciones
from utils.simular_usuarios import generar_usuarios

# Funciones de limpieza y transformación del pipeline existente
from notebook.limpiezaMetas import limpiar_datos_metas
from notebook.limpiezaDeudas import limpiar_datos_deudas
from notebook.transformarMetas import transformar_datos as transformar_metas
from notebook.transformarDeudas import transformar_datos as transformar_deudas
from notebook.limpieza_transacciones import limpiar_transacciones
from notebook.transformacion_transacciones import transformar_transacciones


# ============================================================
# CONFIGURACIÓN DE LA APP
# ============================================================
app = Flask(__name__)
CORS(app)  # Permite que React (puerto 5173) llame a este servidor (puerto 5001)

# Paleta de colores corporativos Finz+
VERDE_FINZ = "#25c974"
AZUL_TEXTO = "#1e293b"
GRIS_TEXTO = "#64748b"
ROJO_ALERTA = "#ef4444"

plt.rcParams['figure.facecolor'] = '#f8fafc'
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.rcParams['font.family'] = 'sans-serif'


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def figura_a_base64(figura):
    """Convierte una figura de matplotlib a string base64 listo para usar en <img src=...>"""
    buffer = io.BytesIO()
    figura.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                   facecolor=figura.get_facecolor())
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(figura)
    return f"data:image/png;base64,{b64}"


def camel_a_snake(nombre):
    """Convierte 'montoTotal' -> 'monto_total' para compatibilidad con la limpieza."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', nombre).lower()


def normalizar_columnas(df):
    df.columns = [camel_a_snake(col) for col in df.columns]
    return df


def obtener_df_transacciones(usuario_email=None):
    """
    Retorna DataFrame con datos reales del usuario.
    Simulación SOLO si el backend está completamente offline (excepción de red).
    Si el usuario no tiene datos, retorna DataFrame vacío → gráfica muestra "sin datos".
    """
    try:
        datos = consumir_transacciones(usuario_email)
        return pd.DataFrame(datos) if datos else pd.DataFrame()
    except Exception:
        # Backend offline → simulación solo cuando no se filtra por usuario
        if not usuario_email:
            return pd.DataFrame(generar_transacciones(200))
        return pd.DataFrame()


def obtener_df_metas(usuario_email=None):
    """
    Retorna DataFrame con metas reales del usuario.
    Simulación SOLO si el backend está offline y no se filtra por usuario.
    """
    try:
        datos = consumir_metas(usuario_email)
        if datos:
            return normalizar_columnas(pd.DataFrame(datos))
        return pd.DataFrame()
    except Exception:
        if not usuario_email:
            return pd.DataFrame(generar_metas(100))
        return pd.DataFrame()


def obtener_df_deudas(usuario_email=None):
    """
    Retorna DataFrame con deudas reales del usuario.
    Simulación SOLO si el backend está offline y no se filtra por usuario.
    """
    try:
        datos = consumir_deudas(usuario_email)
        if datos:
            return normalizar_columnas(pd.DataFrame(datos))
        return pd.DataFrame()
    except Exception:
        if not usuario_email:
            return pd.DataFrame(generar_deudas(100))
        return pd.DataFrame()


def estilizar_ejes(ax, titulo):
    """Aplica estilo corporativo Finz+ a un eje de matplotlib."""
    ax.set_title(titulo, fontsize=14, color=AZUL_TEXTO, fontweight='bold', pad=15)
    ax.tick_params(colors=GRIS_TEXTO)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color('#e2e8f0')
    ax.spines['bottom'].set_color('#e2e8f0')


# ============================================================
# ENDPOINTS
# ============================================================

@app.route('/api/salud')
def salud():
    """Health check: verifica que el servidor está activo."""
    return jsonify({"estado": "activo", "servicio": "FinzPlus Analytics", "puerto": 5001})


@app.route('/api/graficas/usuarios')
def graficas_usuarios():
    """Gráficas de comportamiento de usuarios — exclusivo para Admin."""
    try:
        datos = consumir_usuarios()
        if not datos:
            raise ValueError("Sin datos")
        df_orig = pd.DataFrame(datos)
    except Exception:
        df_orig = pd.DataFrame(generar_usuarios(60))
        df_orig["rol"] = df_orig["rol"].astype(str).str.lower()
        df_orig["id"]  = range(1, len(df_orig) + 1)

    df = df_orig.copy()
    df["rol"]           = df["rol"].astype(str).str.strip().str.lower()
    df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"], errors='coerce')
    df = df.dropna(subset=["id"])

    imagenes = {}
    COLORES_ROLES = {"admin": "#dc2626", "premium": "#7c3aed", "cliente": "#25c974"}

    # Gráfica 1: Distribución de roles (torta)
    df1 = df.groupby("rol")["id"].count().reset_index(name="conteo")
    if not df1.empty:
        colores = [COLORES_ROLES.get(r, "#64748b") for r in df1["rol"]]
        fig, ax = plt.subplots(figsize=(7, 7), facecolor='#f8fafc')
        wedges, textos, pcts = ax.pie(
            df1["conteo"], labels=df1["rol"].str.capitalize(),
            autopct="%1.1f%%", colors=colores, startangle=140,
            wedgeprops={"edgecolor": "#f8fafc", "linewidth": 3}
        )
        circulo = plt.Circle((0, 0), 0.55, fc='#f8fafc')
        ax.add_artist(circulo)
        for t in textos: t.set_color(GRIS_TEXTO)
        ax.set_title("Distribución de Usuarios por Rol", fontsize=14,
                     color=AZUL_TEXTO, fontweight='bold', pad=20)
        plt.tight_layout()
        imagenes["roles"] = figura_a_base64(fig)

    # Gráfica 2: Crecimiento mensual de nuevos usuarios (barras)
    df2 = df.dropna(subset=["fecha_creacion"]).copy()
    if not df2.empty:
        df2["mes"] = df2["fecha_creacion"].dt.to_period("M").astype(str)
        agg2 = df2.groupby("mes")["id"].count().reset_index(name="conteo").sort_values("mes")
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#f8fafc')
        ax.bar(agg2["mes"].astype(str), agg2["conteo"], color=VERDE_FINZ, edgecolor='none', width=0.6)
        ax.bar_label(ax.containers[0], fontsize=9, color=AZUL_TEXTO, padding=4)
        estilizar_ejes(ax, "Crecimiento Mensual de Usuarios")
        ax.set_xlabel("Mes", color=GRIS_TEXTO)
        ax.set_ylabel("Nuevos usuarios", color=GRIS_TEXTO)
        plt.xticks(rotation=45)
        plt.tight_layout()
        imagenes["crecimiento"] = figura_a_base64(fig)

    # Gráfica 3: Cantidad por rol (barras horizontales con colores por rol)
    if not df1.empty:
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#f8fafc')
        colores = [COLORES_ROLES.get(r, "#64748b") for r in df1["rol"]]
        bars = ax.barh(df1["rol"].str.capitalize(), df1["conteo"], color=colores, edgecolor='none')
        ax.bar_label(bars, fontsize=11, color=AZUL_TEXTO, padding=6, fontweight='bold')
        estilizar_ejes(ax, "Total de Usuarios por Plan")
        ax.set_xlabel("Cantidad", color=GRIS_TEXTO)
        plt.tight_layout()
        imagenes["totales_rol"] = figura_a_base64(fig)

    # Gráfica 4: Usuarios registrados por día (últimos 30 días)
    df4 = df.dropna(subset=["fecha_creacion"]).copy()
    if not df4.empty:
        df4["dia"] = df4["fecha_creacion"].dt.date
        agg4 = df4.groupby("dia")["id"].count().reset_index(name="conteo")
        agg4 = agg4.sort_values("dia").tail(30)
        if not agg4.empty:
            fig, ax = plt.subplots(figsize=(12, 4), facecolor='#f8fafc')
            ax.fill_between(range(len(agg4)), agg4["conteo"], alpha=0.3, color=VERDE_FINZ)
            ax.plot(range(len(agg4)), agg4["conteo"], color=VERDE_FINZ, linewidth=2.5, marker='o', markersize=5)
            estilizar_ejes(ax, "Registros de Usuarios (Últimos 30 Días)")
            ax.set_xticks(range(len(agg4)))
            ax.set_xticklabels([str(d) for d in agg4["dia"]], rotation=45, fontsize=8)
            ax.set_ylabel("Registros", color=GRIS_TEXTO)
            plt.tight_layout()
            imagenes["actividad_diaria"] = figura_a_base64(fig)

    return jsonify(imagenes)


@app.route('/api/graficas/transacciones')
def graficas_transacciones():
    """Genera gráficas de transacciones personalizadas por usuario."""
    email = request.args.get('usuarioEmail')
    df_raw = obtener_df_transacciones(email)
    df = limpiar_transacciones(df_raw)
    if df.empty:
        return jsonify({"error": "Sin datos de transacciones"}), 404

    agrupaciones = transformar_transacciones(df)
    imagenes = {}

    # Gráfica 1: Torta — Distribución Ingresos vs Egresos
    df1 = agrupaciones["agrupacion1"]
    if not df1.empty:
        colores = [VERDE_FINZ if t == "ingreso" else ROJO_ALERTA for t in df1["tipo"]]
        fig, ax = plt.subplots(figsize=(7, 7), facecolor='#f8fafc')
        wedges, textos, pcts = ax.pie(
            df1["conteo"], labels=df1["tipo"].str.capitalize(),
            autopct="%1.1f%%", colors=colores, startangle=140,
            wedgeprops={"edgecolor": "#f8fafc", "linewidth": 3}
        )
        circulo = plt.Circle((0, 0), 0.55, fc='#f8fafc')
        ax.add_artist(circulo)
        for t in textos: t.set_color(GRIS_TEXTO)
        ax.set_title("Distribución: Ingresos vs Egresos", fontsize=14,
                     color=AZUL_TEXTO, fontweight='bold', pad=20)
        plt.tight_layout()
        imagenes["proporcion"] = figura_a_base64(fig)

    # Gráfica 2: Líneas — Volumen mensual de transacciones
    df2 = agrupaciones["agrupacion2"]
    if not df2.empty:
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#f8fafc')
        ax.plot(df2["fecha"].astype(str), df2["conteo"],
                marker='o', color=VERDE_FINZ, linewidth=2.5, markersize=6)
        for i, v in enumerate(df2["conteo"]):
            ax.annotate(str(v), xy=(i, v), xytext=(0, 8),
                        textcoords='offset points', ha='center', fontsize=9, color=GRIS_TEXTO)
        estilizar_ejes(ax, "Volumen de Transacciones por Mes")
        ax.set_xlabel("Mes", color=GRIS_TEXTO)
        ax.set_ylabel("Cantidad", color=GRIS_TEXTO)
        plt.xticks(rotation=45)
        plt.tight_layout()
        imagenes["tendencia"] = figura_a_base64(fig)

    # Gráfica 3: Barras — Egresos por categoría
    df3 = agrupaciones["agrupacion3"]
    if not df3.empty:
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#f8fafc')
        ax.bar(df3["categoria_id"].astype(str), df3["conteo"],
               color=VERDE_FINZ, edgecolor='none', width=0.6)
        ax.bar_label(ax.containers[0], fontsize=9, color=AZUL_TEXTO, padding=4)
        estilizar_ejes(ax, "Egresos por Categoría")
        ax.set_xlabel("Categoría", color=GRIS_TEXTO)
        ax.set_ylabel("Cantidad", color=GRIS_TEXTO)
        plt.xticks(rotation=30)
        plt.tight_layout()
        imagenes["egresos_categoria"] = figura_a_base64(fig)

    # Gráfica 4: Mapa de calor — Cuentas vs Categorías
    df4 = agrupaciones["agrupacion4"]
    if not df4.empty:
        tabla = df4.pivot_table(index="cuenta_id", columns="categoria_id",
                                values="conteo", aggfunc="sum", fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#f8fafc')
        sns.heatmap(tabla, annot=True, fmt=".0f", cmap="Greens", ax=ax,
                    linewidths=2, linecolor='#f8fafc',
                    annot_kws={"size": 10, "weight": "bold"})
        ax.set_title("Densidad de Egresos: Cuentas vs Categorías", fontsize=14,
                     color=AZUL_TEXTO, fontweight='bold', pad=15)
        plt.xticks(rotation=45, color=GRIS_TEXTO)
        plt.yticks(color=GRIS_TEXTO)
        plt.tight_layout()
        imagenes["mapa_calor"] = figura_a_base64(fig)

    # Gráfica 5: Barras — Transacciones de alto valor (> $1.5M)
    df5 = agrupaciones["agrupacion5"]
    if not df5.empty:
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#f8fafc')
        ax.bar(df5["descripcion"].astype(str), df5["conteo"],
               color=ROJO_ALERTA, edgecolor='none', width=0.6)
        ax.bar_label(ax.containers[0], fontsize=9, color=AZUL_TEXTO, padding=4)
        estilizar_ejes(ax, "Frecuencia de Transacciones de Alto Valor (> $1.5M)")
        ax.set_xlabel("Descripción", color=GRIS_TEXTO)
        ax.set_ylabel("Cantidad", color=GRIS_TEXTO)
        plt.xticks(rotation=30)
        plt.tight_layout()
        imagenes["alto_valor"] = figura_a_base64(fig)

    return jsonify(imagenes)


@app.route('/api/graficas/metas')
def graficas_metas():
    """Genera gráficas de metas personalizadas por usuario."""
    email = request.args.get('usuarioEmail')
    df = limpiar_datos_metas(obtener_df_metas(email))
    if df.empty:
        return jsonify({"error": "Sin datos de metas disponibles"}), 404

    agrupaciones = transformar_metas(df)
    imagenes = {}

    # --- Gráfica 1: Cronograma de metas (línea de tiempo) ---
    df1 = agrupaciones["agrupacion1"]
    if not df1.empty:
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#f8fafc')
        ax.plot(df1["fecha_limite"].astype(str), df1["conteo"],
                marker='o', color=VERDE_FINZ, linewidth=2.5, markersize=6)
        for i, val in enumerate(df1["conteo"]):
            ax.annotate(str(val), xy=(i, val), xytext=(0, 8),
                        textcoords='offset points', ha='center', fontsize=9, color=GRIS_TEXTO)
        estilizar_ejes(ax, "Cronograma de Cumplimiento de Metas")
        ax.set_xlabel("Fecha límite", color=GRIS_TEXTO)
        ax.set_ylabel("Cantidad de metas", color=GRIS_TEXTO)
        plt.xticks(rotation=45)
        plt.tight_layout()
        imagenes["cronograma"] = figura_a_base64(fig)

    # --- Gráfica 2: Metas ambiciosas por categoría (barras) ---
    df2 = agrupaciones["agrupacion2"]
    if not df2.empty:
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#f8fafc')
        ax.bar(df2["nombre"], df2["conteo"], color='#00ACC1', edgecolor='none', width=0.6)
        ax.bar_label(ax.containers[0], fontsize=9, color=AZUL_TEXTO, padding=4)
        estilizar_ejes(ax, "Metas de Gran Volumen (>= 5M) por Categoría")
        ax.set_xlabel("Categoría", color=GRIS_TEXTO)
        ax.set_ylabel("Cantidad", color=GRIS_TEXTO)
        plt.xticks(rotation=30)
        plt.tight_layout()
        imagenes["metas_ambiciosas"] = figura_a_base64(fig)

    # --- Gráfica 3: Metas sin iniciar (torta) ---
    df4 = agrupaciones["agrupacion4"]
    if not df4.empty:
        colores = [VERDE_FINZ, '#065f46', '#34d399', '#a7f3d0', '#00ACC1']
        fig, ax = plt.subplots(figsize=(7, 7), facecolor='#f8fafc')
        _, textos, porcentajes = ax.pie(
            df4["conteo"], labels=df4["nombre"],
            autopct="%1.1f%%", startangle=140,
            colors=colores[:len(df4)],
            wedgeprops={"edgecolor": '#f8fafc', "linewidth": 3}
        )
        for t in textos:
            t.set_color(GRIS_TEXTO)
        ax.set_title("Distribución de Metas Sin Iniciar", fontsize=14,
                     color=AZUL_TEXTO, fontweight='bold', pad=20)
        plt.tight_layout()
        imagenes["metas_sin_iniciar"] = figura_a_base64(fig)

    # --- Gráfica 4: Mapa de calor usuarios vs categorías (solo si hay usuario_id) ---
    df3 = agrupaciones["agrupacion3"]
    if not df3.empty and "usuario_id" in df3.columns:
        tabla = df3.pivot_table(index="usuario_id", columns="nombre",
                                values="conteo", aggfunc="sum", fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#f8fafc')
        sns.heatmap(tabla, annot=True, fmt=".0f", cmap="Greens", ax=ax,
                    linewidths=2, linecolor='#f8fafc',
                    annot_kws={"size": 11, "weight": "bold"})
        ax.set_title("Actividad de Ahorro por Usuario", fontsize=14,
                     color=AZUL_TEXTO, fontweight='bold', pad=15)
        plt.xticks(rotation=45, color=GRIS_TEXTO)
        plt.yticks(color=GRIS_TEXTO)
        plt.tight_layout()
        imagenes["mapa_usuarios"] = figura_a_base64(fig)

    return jsonify(imagenes)


@app.route('/api/graficas/deudas')
def graficas_deudas():
    """Genera gráficas de deudas personalizadas por usuario."""
    email = request.args.get('usuarioEmail')
    df = limpiar_datos_deudas(obtener_df_deudas(email))
    if df.empty:
        return jsonify({"error": "Sin datos de deudas disponibles"}), 404

    agrupaciones = transformar_deudas(df)
    imagenes = {}

    # --- Gráfica 1: Deudas de alto valor por tipo (barras) ---
    df2 = agrupaciones["agrupacion2"]
    if not df2.empty:
        fig, ax = plt.subplots(figsize=(8, 5), facecolor='#f8fafc')
        ax.bar(df2["tipo"], df2["conteo"], color=ROJO_ALERTA, edgecolor='none', width=0.5)
        ax.bar_label(ax.containers[0], fontsize=9, color=AZUL_TEXTO, padding=4)
        estilizar_ejes(ax, "Deudas de Alto Valor (>= 1M) por Tipo")
        ax.set_xlabel("Tipo de deuda", color=GRIS_TEXTO)
        ax.set_ylabel("Cantidad", color=GRIS_TEXTO)
        plt.xticks(rotation=15)
        plt.tight_layout()
        imagenes["deudas_por_tipo"] = figura_a_base64(fig)

    # --- Gráfica 2: Distribución de acreedores bancarios (torta) ---
    df4 = agrupaciones["agrupacion4"]
    if not df4.empty:
        colores = ['#1E88E5', '#43A047', ROJO_ALERTA, '#8E24AA', '#FDD835']
        fig, ax = plt.subplots(figsize=(7, 7), facecolor='#f8fafc')
        _, textos, _ = ax.pie(
            df4["conteo"], labels=df4["persona_entidad"],
            autopct="%1.1f%%", startangle=140,
            colors=colores[:len(df4)],
            wedgeprops={"edgecolor": '#f8fafc', "linewidth": 3}
        )
        for t in textos:
            t.set_color(GRIS_TEXTO)
        ax.set_title("Distribución de Acreedores (Deudas Bancarias)", fontsize=14,
                     color=AZUL_TEXTO, fontweight='bold', pad=20)
        plt.tight_layout()
        imagenes["acreedores"] = figura_a_base64(fig)

    # --- Gráfica 3: Mapa de calor deudas intactas (si hay datos) ---
    df3 = agrupaciones["agrupacion3"]
    if not df3.empty:
        tabla = df3.pivot_table(index="tipo", columns="persona_entidad",
                                values="conteo", aggfunc="sum", fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#f8fafc')
        sns.heatmap(tabla, annot=True, fmt=".0f", cmap="Reds", ax=ax,
                    linewidths=2, linecolor='#f8fafc',
                    annot_kws={"size": 11, "weight": "bold"})
        ax.set_title("Concentración de Deudas Sin Abonar", fontsize=14,
                     color=AZUL_TEXTO, fontweight='bold', pad=15)
        plt.xticks(rotation=45, color=GRIS_TEXTO)
        plt.yticks(color=GRIS_TEXTO)
        plt.tight_layout()
        imagenes["deudas_intactas"] = figura_a_base64(fig)

    return jsonify(imagenes)


# ============================================================
# ARRANQUE
# ============================================================
if __name__ == '__main__':
    print("=" * 55)
    print("  Servidor de Analítica FinzPlus corriendo en :5001")
    print("  Endpoints disponibles:")
    print("    GET /api/salud")
    print("    GET /api/graficas/usuarios       (solo Admin)")
    print("    GET /api/graficas/transacciones")
    print("    GET /api/graficas/metas")
    print("    GET /api/graficas/deudas")
    print("=" * 55)
    app.run(port=5001, debug=True)
