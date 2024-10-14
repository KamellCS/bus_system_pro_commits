# main.py – version completa con cerrar sesion, modificar pasaje, boleta, validaciones
import tkinter as tk
from tkinter import ttk, messagebox
import calendar, datetime, datos
from ordenamiento import burbuja, seleccion, insercion, merge_sort, quick_sort

BG="#1a1f2e"; CARD="#242938"; ACCENT="#4f8ef7"; SIDEBAR="#141824"
TEXT="#e8eaf0"; SUBTEXT="#8892a4"; SUCCESS="#2ecc71"; DANGER="#e74c3c"
WHITE="#ffffff"; BORDER="#2d3348"; ACCENT2="#6c63ff"; WARN="#f39c12"

OPCIONES_ORDEN = {
    "Por nombre (A-Z)":           ("nombre",  burbuja,    "Burbuja"),
    "Por DNI":                    ("dni",     insercion,  "Insercion"),
    "Por destino (A-Z)":          ("destino", seleccion,  "Seleccion"),
    "Por numero de asiento":      ("asiento", quick_sort, "Quick Sort"),
    "Por fecha de viaje":         ("fecha",   merge_sort, "Merge Sort"),
    "Por precio (menor a mayor)": ("precio",  quick_sort, "Quick Sort"),
}

HOY = datetime.date.today()

# ─── Validaciones ─────────────────────────────────────────────────────────────
def _solo_numeros(val, max_len):
    return (val.isdigit() or val == "") and len(val) <= max_len

def _solo_letras(val, max_len):
    return (all(c.isalpha() or c in " .-'" for c in val) or val == "") and len(val) <= max_len

def _registrar_validaciones(widget, modo, max_len):
    if modo == "num":
        vcmd = widget.register(lambda v: _solo_numeros(v, max_len))
    else:
        vcmd = widget.register(lambda v: _solo_letras(v, max_len))
    widget.config(validate="key", validatecommand=(vcmd, "%P"))

# ─── DatePicker (solo fechas >= hoy) ─────────────────────────────────────────
class DatePicker(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=kw.pop("bg", CARD))
        self._var = tk.StringVar(value=HOY.strftime("%d/%m/%Y"))
        self._entry = ttk.Entry(self, textvariable=self._var, width=12, font=("Segoe UI",10))
        self._entry.pack(side="left")
        tk.Button(self, text="v", bg=ACCENT, fg=WHITE, bd=0, padx=4, cursor="hand2",
                  font=("Segoe UI",8), command=self._abrir).pack(side="left", padx=(2,0))
    def get(self): return self._var.get()
    def set(self, val): self._var.set(val)
    def _abrir(self):
        top = tk.Toplevel(self); top.overrideredirect(True); top.configure(bg=CARD)
        x = self.winfo_rootx(); y = self.winfo_rooty() + self.winfo_height()
        top.geometry(f"+{x}+{y}")
        try:
            parts = self._var.get().split("/"); dia,mes,anio=int(parts[0]),int(parts[1]),int(parts[2])
        except Exception:
            dia,mes,anio=HOY.day,HOY.month,HOY.year
        self._cal=top; self._mes_actual=mes; self._anio_actual=anio
        self._cal_frame=tk.Frame(top,bg=CARD); self._cal_frame.pack(padx=5,pady=5)
        self._render_cal(dia)
    def _render_cal(self, dia_sel=None):
        for w in self._cal_frame.winfo_children(): w.destroy()
        meses=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
        nav=tk.Frame(self._cal_frame,bg=CARD); nav.grid(row=0,column=0,columnspan=7,sticky="ew")
        tk.Button(nav,text="<",bg=CARD,fg=TEXT,bd=0,cursor="hand2",
                  command=lambda:self._nav(-1,dia_sel)).pack(side="left")
        tk.Label(nav,text=f"{meses[self._mes_actual-1]} {self._anio_actual}",
                 bg=CARD,fg=TEXT,font=("Segoe UI",9,"bold")).pack(side="left",expand=True)
        tk.Button(nav,text=">",bg=CARD,fg=TEXT,bd=0,cursor="hand2",
                  command=lambda:self._nav(1,dia_sel)).pack(side="right")
        for col,dia in enumerate(["Lu","Ma","Mi","Ju","Vi","Sa","Do"]):
            tk.Label(self._cal_frame,text=dia,bg=CARD,fg=SUBTEXT,
                     font=("Segoe UI",8,"bold"),width=3).grid(row=1,column=col)
        for fila,semana in enumerate(calendar.monthcalendar(self._anio_actual,self._mes_actual)):
            for col,d in enumerate(semana):
                if d==0: tk.Label(self._cal_frame,text="",bg=CARD,width=3).grid(row=fila+2,column=col); continue
                fecha_btn = datetime.date(self._anio_actual, self._mes_actual, d)
                es_pasado = fecha_btn < HOY
                bg_color = ACCENT if d==dia_sel else (BORDER if es_pasado else CARD)
                state = "disabled" if es_pasado else "normal"
                fg_color = SUBTEXT if es_pasado else WHITE
                tk.Button(self._cal_frame,text=str(d),width=3,bg=bg_color,fg=fg_color,bd=0,
                          cursor="arrow" if es_pasado else "hand2",font=("Segoe UI",9),
                          state=state,
                          command=lambda n=d:self._pick(n)).grid(row=fila+2,column=col,pady=1)
    def _nav(self,delta,dia_sel):
        nuevo_mes = self._mes_actual + delta
        nuevo_anio = self._anio_actual
        if nuevo_mes > 12: nuevo_mes=1; nuevo_anio+=1
        elif nuevo_mes < 1: nuevo_mes=12; nuevo_anio-=1
        # No retroceder antes del mes actual
        if (nuevo_anio, nuevo_mes) < (HOY.year, HOY.month): return
        self._mes_actual=nuevo_mes; self._anio_actual=nuevo_anio
        self._render_cal(dia_sel)
    def _pick(self,dia):
        self._var.set(f"{dia:02d}/{self._mes_actual:02d}/{self._anio_actual}"); self._cal.destroy()

# ─── Login ────────────────────────────────────────────────────────────────────
class VentanaLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BUS SYSTEM PRO"); self.geometry("420x480")
        self.resizable(False,False); self.configure(bg=BG)
        tk.Label(self,text="BUS SYSTEM PRO",font=("Segoe UI",18,"bold"),bg=BG,fg=TEXT).pack(pady=(50,10))
        tk.Label(self,text="Usuario:",bg=BG,fg=SUBTEXT,font=("Segoe UI",10)).pack()
        self.ent_u=ttk.Entry(self,font=("Segoe UI",11)); self.ent_u.pack(pady=4); self.ent_u.insert(0,"admin")
        tk.Label(self,text="Contrasena:",bg=BG,fg=SUBTEXT,font=("Segoe UI",10)).pack()
        self.ent_c=ttk.Entry(self,font=("Segoe UI",11),show="*"); self.ent_c.pack(pady=4); self.ent_c.insert(0,"admin123")
        self.lbl_e=tk.Label(self,text="",bg=BG,fg=DANGER,font=("Segoe UI",9)); self.lbl_e.pack()
        tk.Button(self,text="Ingresar",bg=ACCENT,fg=WHITE,bd=0,font=("Segoe UI",11,"bold"),
                  pady=8,cursor="hand2",command=self._login).pack(pady=10,fill="x",padx=60)
    def _login(self):
        for u in datos.USUARIOS:
            if u["usuario"]==self.ent_u.get() and u["clave"]==self.ent_c.get():
                self.destroy(); VentanaPrincipal(u).mainloop(); return
        self.lbl_e.config(text="Credenciales incorrectas")

if __name__ == "__main__":
    VentanaLogin().mainloop()
