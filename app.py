"""
=====================================================================
 Calculadora de Duración de Citas
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_calculadora_duracion_citas_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Calculadora de Duración de Citas."""

    def __init__(self, c1, c2, c3, c4, c5):
        self.c1 = float(c1)
        self.c2 = float(c2)
        self.c3 = float(c3)
        self.c4 = float(c4)
        self.c5 = float(c5)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        total = self.c1 + self.c2 + self.c3 + self.c4 + self.c5
        horas = int(total // 60)
        mins = int(total % 60)
        return {"total_min": total, "horas": horas, "mins": mins}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["total_min"] == 0:
            return "⚠️ Ingresa al menos una duración."
        if resultados["horas"] >= 8:
            return "⚠️ Jornada larga (>8h). Considera distribuir las citas en varios días."
        return "✅ Jornada razonable."



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("c1"),input_float("c2"),input_float("c3"),input_float("c4"),input_float("c5"))
    r = c.calcular()
    html = f"""
      <div class="result-value">⏱️ {fmt_num(r["total_min"])} minutos</div>
      <p class="result-detail">Equivalente a <strong>{r["horas"]}h {r["mins"]}min</strong>.</p>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "c1": input_float("c1"),
            "c2": input_float("c2"),
            "c3": input_float("c3"),
            "c4": input_float("c4"),
            "c5": input_float("c5"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "c1" in datos:
            document.querySelector("#c1").value = datos["c1"]
        if "c2" in datos:
            document.querySelector("#c2").value = datos["c2"]
        if "c3" in datos:
            document.querySelector("#c3").value = datos["c3"]
        if "c4" in datos:
            document.querySelector("#c4").value = datos["c4"]
        if "c5" in datos:
            document.querySelector("#c5").value = datos["c5"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
