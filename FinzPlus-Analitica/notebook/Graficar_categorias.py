import os
import matplotlib.pyplot as plt


def graficar_categorias(categorias_transformadas, save=False, save_dir="outputs"):
    """Grafica las tres transformaciones de categorías."""
    os.makedirs(save_dir, exist_ok=True)
    df_gastos_fecha = categorias_transformadas.get("agrupacion1")
    df_alto_valor = categorias_transformadas.get("agrupacion2")
    df_ocio = categorias_transformadas.get("agrupacion3")

    if df_gastos_fecha is not None and not df_gastos_fecha.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(df_gastos_fecha["fecha"], df_gastos_fecha["total_gastado"], marker="o")
        plt.title("Gastos por Fecha")
        plt.xlabel("Fecha")
        plt.ylabel("Total gastado")
        plt.xticks(rotation=45)
        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(save_dir, "gastos_por_fecha.png"), bbox_inches="tight")
        plt.show()
    else:
        print("No hay datos para graficar Gastos por Fecha.")

    if df_alto_valor is not None and not df_alto_valor.empty:
        plt.figure(figsize=(6, 4))
        plt.bar(df_alto_valor["tipo"], df_alto_valor["conteo"], color="orange")
        plt.title("Transacciones de Alto Valor")
        plt.xlabel("Tipo")
        plt.ylabel("Conteo")
        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(save_dir, "transacciones_de_alto_valor.png"), bbox_inches="tight")
        plt.show()
    else:
        print("No hay datos para graficar Transacciones de Alto Valor.")

    if df_ocio is not None and not df_ocio.empty:
        plt.figure(figsize=(6, 6))
        plt.pie(df_ocio["total_ocio"], labels=df_ocio["nombre"], autopct="%1.1f%%", startangle=90)
        plt.title("Distribución de Ocio")
        plt.axis("equal")
        plt.tight_layout()
        if save:
            plt.savefig(os.path.join(save_dir, "distribucion_ocio.png"), bbox_inches="tight")
        plt.show()
    else:
        print("No hay datos para graficar Distribución de Ocio.")
