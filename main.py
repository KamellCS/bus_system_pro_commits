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

# ─── Ventana Principal ────────────────────────────────────────────────────────
class VentanaPrincipal(tk.Tk):
    def __init__(self, usuario):
        super().__init__(); self.usuario=usuario
        self.title("BUS SYSTEM PRO"); self.geometry("1100x680"); self.configure(bg=BG)
        self._sidebar(); self._mostrar("venta")
    def _sidebar(self):
        sb=tk.Frame(self,bg=SIDEBAR,width=200); sb.pack(side="left",fill="y"); sb.pack_propagate(False)
        tk.Label(sb,text="BUS SYSTEM PRO",font=("Segoe UI",11,"bold"),bg=SIDEBAR,fg=TEXT).pack(pady=(20,2))
        tk.Label(sb,text=f"Hola, {self.usuario['usuario']}",bg=SIDEBAR,fg=SUBTEXT,
                 font=("Segoe UI",8)).pack(pady=(0,15))
        self.area=tk.Frame(self,bg=BG); self.area.pack(side="left",fill="both",expand=True)
        for clave,texto in [("venta","Vender Pasaje"),("pasajeros","Pasajeros"),
                             ("rutas","Rutas"),("reporte","Reportes")]:
            tk.Button(sb,text=texto,font=("Segoe UI",10),bg=SIDEBAR,fg=TEXT,bd=0,
                      anchor="w",padx=15,pady=10,cursor="hand2",
                      command=lambda c=clave:self._mostrar(c)).pack(fill="x")
        # Boton cerrar sesion al fondo
        tk.Frame(sb,bg=BORDER,height=1).pack(fill="x",pady=(20,0))
        tk.Button(sb,text="Cerrar sesion",font=("Segoe UI",10),bg=SIDEBAR,fg=DANGER,bd=0,
                  anchor="w",padx=15,pady=10,cursor="hand2",
                  command=self._cerrar_sesion).pack(fill="x",side="bottom")
    def _mostrar(self,clave):
        for w in self.area.winfo_children(): w.destroy()
        {"venta":VistaVenta,"pasajeros":VistaPasajeros,
         "rutas":VistaRutas,"reporte":VistaReporte}[clave](self.area,self.usuario).pack(fill="both",expand=True)
    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesion","¿Deseas cerrar sesion?"):
            self.destroy(); VentanaLogin().mainloop()

# ─── Boleta ───────────────────────────────────────────────────────────────────
class VentanaBoleta(tk.Toplevel):
    def __init__(self, parent, pasajero):
        super().__init__(parent)
        self.title("Boleta de Pasaje"); self.geometry("420x520")
        self.resizable(False,False); self.configure(bg=WHITE)
        p = pasajero; ruta = datos.ruta_por_id(p["ruta_id"])
        # Encabezado
        tk.Label(self,text="BUS SYSTEM PRO",font=("Segoe UI",16,"bold"),bg=WHITE,fg="#1a1f2e").pack(pady=(20,2))
        tk.Label(self,text="BOLETA DE PASAJE",font=("Segoe UI",11),bg=WHITE,fg="#555").pack()
        tk.Frame(self,bg="#ccc",height=1).pack(fill="x",padx=30,pady=10)
        # Numero de boleta
        tk.Label(self,text=f"N° Boleta: BSP-{p['id']:05d}",font=("Segoe UI",10,"bold"),bg=WHITE).pack()
        tk.Label(self,text=datetime.datetime.now().strftime("Emitida: %d/%m/%Y %H:%M"),
                 font=("Segoe UI",9),bg=WHITE,fg="#777").pack(pady=(0,10))
        tk.Frame(self,bg="#ccc",height=1).pack(fill="x",padx=30,pady=(0,10))
        # Datos del pasajero
        frame=tk.Frame(self,bg=WHITE); frame.pack(padx=30,fill="x")
        campos = [
            ("Pasajero",   p["nombre"]),
            ("DNI",        p["dni"]),
            ("Telefono",   p.get("telefono","—")),
            ("Origen",     ruta["origen"] if ruta else "Lima"),
            ("Destino",    p["destino"]),
            ("Fecha",      p["fecha"]),
            ("Hora salida",ruta["hora"] if ruta else "—"),
            ("Asiento N°", str(p["asiento"])),
        ]
        for lbl,val in campos:
            fila=tk.Frame(frame,bg=WHITE); fila.pack(fill="x",pady=3)
            tk.Label(fila,text=lbl+":",font=("Segoe UI",9,"bold"),bg=WHITE,
                     fg="#555",width=14,anchor="w").pack(side="left")
            tk.Label(fila,text=val,font=("Segoe UI",10),bg=WHITE,anchor="w").pack(side="left")
        tk.Frame(self,bg="#ccc",height=1).pack(fill="x",padx=30,pady=15)
        # Total
        tk.Label(self,text=f"TOTAL:   S/ {p['precio']:.2f}",
                 font=("Segoe UI",14,"bold"),bg=WHITE,fg="#1a1f2e").pack()
        tk.Frame(self,bg="#ccc",height=1).pack(fill="x",padx=30,pady=15)
        tk.Label(self,text="Gracias por viajar con nosotros",
                 font=("Segoe UI",9,"italic"),bg=WHITE,fg="#888").pack()
        tk.Button(self,text="Cerrar",bg="#1a1f2e",fg=WHITE,bd=0,
                  font=("Segoe UI",10,"bold"),pady=8,cursor="hand2",
                  command=self.destroy).pack(pady=15,padx=60,fill="x")

# ─── Formulario pasajero (compartido entre venta y modificacion) ───────────────
class FormularioPasajero(tk.Frame):
    """Formulario reutilizable con validaciones."""
    def __init__(self, parent, bg=CARD):
        super().__init__(parent, bg=bg)
        self.v_nombre=tk.StringVar(); self.v_dni=tk.StringVar()
        self.v_telefono=tk.StringVar(); self.v_ruta=tk.StringVar()
        # Nombre
        tk.Label(self,text="Nombre completo",bg=bg,fg=SUBTEXT,font=("Segoe UI",9,"bold")).pack(anchor="w",pady=(6,1))
        e_nombre=ttk.Entry(self,textvariable=self.v_nombre,font=("Segoe UI",10),width=28)
        e_nombre.pack(anchor="w"); _registrar_validaciones(e_nombre,"letra",60)
        # DNI (8 digitos)
        tk.Label(self,text="DNI (8 digitos)",bg=bg,fg=SUBTEXT,font=("Segoe UI",9,"bold")).pack(anchor="w",pady=(6,1))
        e_dni=ttk.Entry(self,textvariable=self.v_dni,font=("Segoe UI",10),width=28)
        e_dni.pack(anchor="w"); _registrar_validaciones(e_dni,"num",8)
        # Telefono (9 digitos)
        tk.Label(self,text="Telefono (9 digitos)",bg=bg,fg=SUBTEXT,font=("Segoe UI",9,"bold")).pack(anchor="w",pady=(6,1))
        e_tel=ttk.Entry(self,textvariable=self.v_telefono,font=("Segoe UI",10),width=28)
        e_tel.pack(anchor="w"); _registrar_validaciones(e_tel,"num",9)
        # Fecha
        tk.Label(self,text="Fecha de viaje",bg=bg,fg=SUBTEXT,font=("Segoe UI",9,"bold")).pack(anchor="w",pady=(6,1))
        self.dp=DatePicker(self,bg=bg); self.dp.pack(anchor="w")
        # Ruta
        tk.Label(self,text="Ruta:",bg=bg,fg=SUBTEXT,font=("Segoe UI",9,"bold")).pack(anchor="w",pady=(6,1))
        self.combo=ttk.Combobox(self,textvariable=self.v_ruta,state="readonly",width=30)
        self._actualizar_rutas(); self.combo.pack(anchor="w")
    def _actualizar_rutas(self):
        opts=[f"{r['id']} - Lima->{r['destino']} {r['hora']} S/{r['precio']}" for r in datos.RUTAS]
        self.combo["values"]=opts
        if opts: self.combo.current(0)
    def ruta_actual(self): return datos.RUTAS[self.combo.current()]
    def validar(self):
        if not self.v_nombre.get().strip():
            messagebox.showwarning("Aviso","Ingresa el nombre completo"); return False
        if len(self.v_dni.get()) != 8:
            messagebox.showwarning("Aviso","El DNI debe tener exactamente 8 digitos"); return False
        if self.v_telefono.get() and len(self.v_telefono.get()) not in (0,9):
            messagebox.showwarning("Aviso","El telefono debe tener 9 digitos"); return False
        return True

# ─── Vender Pasaje ────────────────────────────────────────────────────────────
class VistaVenta(tk.Frame):
    def __init__(self,parent,usuario):
        super().__init__(parent,bg=BG); self.asiento_sel=None; self.botones_asiento={}
        tk.Label(self,text="Vender Pasaje",font=("Segoe UI",15,"bold"),bg=BG,fg=TEXT).pack(pady=12)
        panes=tk.Frame(self,bg=BG); panes.pack(fill="both",expand=True,padx=20)
        # Formulario izquierdo
        izq=tk.Frame(panes,bg=CARD,padx=12,pady=12); izq.pack(side="left",fill="y",padx=(0,12))
        self.form=FormularioPasajero(izq,bg=CARD); self.form.pack(fill="x")
        self.form.combo.bind("<<ComboboxSelected>>",lambda e:self._mapa())
        self.lbl_asiento=tk.Label(izq,text="Asiento: —",bg=CARD,fg=TEXT,font=("Segoe UI",10,"bold"))
        self.lbl_asiento.pack(pady=8)
        tk.Button(izq,text="Confirmar venta",bg=SUCCESS,fg=WHITE,bd=0,
                  font=("Segoe UI",10,"bold"),pady=8,cursor="hand2",command=self._vender).pack(fill="x")
        # Mapa derecho
        der=tk.Frame(panes,bg=CARD,padx=10,pady=10); der.pack(side="left",fill="both",expand=True)
        tk.Label(der,text="Mapa de Asientos",bg=CARD,fg=TEXT,font=("Segoe UI",11,"bold")).pack(pady=(0,6))
        ley=tk.Frame(der,bg=CARD); ley.pack()
        for color,txt in [(SUCCESS,"Libre"),(ACCENT,"Seleccionado"),(DANGER,"Ocupado")]:
            tk.Frame(ley,bg=color,width=14,height=14).pack(side="left",padx=(8,2))
            tk.Label(ley,text=txt,bg=CARD,fg=TEXT,font=("Segoe UI",8)).pack(side="left",padx=(0,8))
        self.frame_mapa=tk.Frame(der,bg=CARD); self.frame_mapa.pack(pady=8)
        self._mapa()
    def _mapa(self):
        for w in self.frame_mapa.winfo_children(): w.destroy()
        self.asiento_sel=None; self.lbl_asiento.config(text="Asiento: —"); self.botones_asiento={}
        ruta=self.form.ruta_actual(); ocup=datos.asientos_ocupados(ruta["id"]); total=ruta["asientos"]; filas=(total+3)//4
        cab=tk.Frame(self.frame_mapa,bg=CARD); cab.pack(fill="x",pady=(0,4))
        tk.Label(cab,text="Conductor",bg=BORDER,fg=TEXT,font=("Segoe UI",8),
                 padx=8,pady=3).pack(side="right",padx=4)
        for fila in range(filas):
            row=tk.Frame(self.frame_mapa,bg=CARD); row.pack(pady=2)
            for col in range(4):
                num=fila*4+col+1
                if num>total: tk.Frame(row,width=34,height=28,bg=CARD).pack(side="left",padx=2); continue
                if col==2: tk.Frame(row,width=20,bg=CARD).pack(side="left")
                lib=num not in ocup
                b=tk.Button(row,text=str(num),width=3,height=1,
                            bg=SUCCESS if lib else DANGER,fg=WHITE,bd=0,
                            font=("Segoe UI",8,"bold"),
                            state="normal" if lib else "disabled",
                            cursor="hand2" if lib else "arrow",
                            command=lambda n=num:self._sel(n))
                b.pack(side="left",padx=2); self.botones_asiento[num]=b
    def _sel(self,n):
        ocup=datos.asientos_ocupados(self.form.ruta_actual()["id"])
        if self.asiento_sel and self.asiento_sel not in ocup:
            self.botones_asiento[self.asiento_sel].config(bg=SUCCESS)
        self.asiento_sel=n; self.botones_asiento[n].config(bg=ACCENT)
        self.lbl_asiento.config(text=f"Asiento: {n}")
    def _vender(self):
        if not self.form.validar(): return
        if not self.asiento_sel:
            messagebox.showwarning("Aviso","Selecciona un asiento en el mapa"); return
        ruta=self.form.ruta_actual()
        try:
            p=datos.agregar_pasajero(self.form.v_nombre.get().strip(),
                                     self.form.v_dni.get(),
                                     self.form.v_telefono.get(),
                                     ruta["id"],self.asiento_sel,self.form.dp.get())
            VentanaBoleta(self, p)
            self.form.v_nombre.set(""); self.form.v_dni.set(""); self.form.v_telefono.set("")
            self._mapa()
        except ValueError as e: messagebox.showerror("Error",str(e))

# ─── Dialogo Ordenar ──────────────────────────────────────────────────────────
class DialogoOrdenar(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent); self.title("Ordenar Pasajeros")
        self.geometry("360x420"); self.resizable(False,False); self.configure(bg=BG)
        self.grab_set(); self.callback=callback
        tk.Label(self,text="Ordenar por:",font=("Segoe UI",12,"bold"),bg=BG,fg=TEXT).pack(pady=(20,10))
        self.var=tk.StringVar(value=list(OPCIONES_ORDEN.keys())[0])
        self.lbl_algo=tk.Label(self,text="",bg=BG,fg=ACCENT,font=("Segoe UI",9,"italic"))
        self.lbl_algo.pack(pady=(0,8))
        for desc in OPCIONES_ORDEN:
            tk.Radiobutton(self,text=desc,variable=self.var,value=desc,
                           bg=BG,fg=TEXT,selectcolor=CARD,activebackground=BG,
                           font=("Segoe UI",10),anchor="w",
                           command=self._actualizar_info).pack(fill="x",padx=30,pady=3)
        self._actualizar_info()
        tk.Button(self,text="Ordenar",bg=ACCENT,fg=WHITE,bd=0,
                  font=("Segoe UI",11,"bold"),pady=8,cursor="hand2",
                  command=self._ok).pack(fill="x",padx=40,pady=15)
    def _actualizar_info(self):
        _,_,nombre_algo=OPCIONES_ORDEN[self.var.get()]
        complejidad="O(n2)" if nombre_algo in ("Burbuja","Seleccion","Insercion") else "O(n log n)"
        self.lbl_algo.config(text=f"Algoritmo: {nombre_algo}  ({complejidad})")
    def _ok(self):
        clave_dict,fn,nombre_algo=OPCIONES_ORDEN[self.var.get()]
        datos.registrar_uso_metodo(nombre_algo)
        self.callback(clave_dict,fn); self.destroy()

# ─── Dialogo Modificar Pasaje ─────────────────────────────────────────────────
class DialogoModificar(tk.Toplevel):
    def __init__(self, parent, pasajero, on_guardado):
        super().__init__(parent); self.title(f"Modificar Pasaje N° {pasajero['id']}")
        self.geometry("480x580"); self.resizable(False,False); self.configure(bg=BG)
        self.grab_set(); self.p=pasajero; self.on_guardado=on_guardado
        self.asiento_sel=pasajero["asiento"]; self.botones_asiento={}
        tk.Label(self,text=f"Modificar Pasaje  N° {pasajero['id']}",
                 font=("Segoe UI",13,"bold"),bg=BG,fg=TEXT).pack(pady=(15,10))
        scroll_frame=tk.Frame(self,bg=BG); scroll_frame.pack(fill="both",expand=True,padx=20)
        self.form=FormularioPasajero(scroll_frame,bg=CARD)
        # Pre-cargar datos actuales
        self.form.v_nombre.set(pasajero["nombre"])
        self.form.v_dni.set(pasajero["dni"])
        self.form.v_telefono.set(pasajero.get("telefono",""))
        self.form.dp.set(pasajero["fecha"])
        # Seleccionar ruta actual
        for idx,r in enumerate(datos.RUTAS):
            if r["id"]==pasajero["ruta_id"]: self.form.combo.current(idx); break
        self.form.pack(fill="x")
        self.form.combo.bind("<<ComboboxSelected>>",lambda e:self._mapa())
        # Mapa compacto
        tk.Label(scroll_frame,text="Cambiar asiento:",bg=BG,fg=SUBTEXT,
                 font=("Segoe UI",9,"bold")).pack(anchor="w",pady=(10,2))
        self.lbl_asiento=tk.Label(scroll_frame,text=f"Asiento actual: {self.asiento_sel}",
                                  bg=BG,fg=ACCENT,font=("Segoe UI",9,"bold"))
        self.lbl_asiento.pack(anchor="w")
        self.frame_mapa=tk.Frame(scroll_frame,bg=BG); self.frame_mapa.pack(pady=5)
        self._mapa()
        tk.Button(self,text="Guardar cambios",bg=WARN,fg=WHITE,bd=0,
                  font=("Segoe UI",11,"bold"),pady=8,cursor="hand2",
                  command=self._guardar).pack(fill="x",padx=20,pady=(10,5))
        tk.Button(self,text="Cancelar",bg=BORDER,fg=TEXT,bd=0,
                  font=("Segoe UI",10),pady=6,cursor="hand2",
                  command=self.destroy).pack(fill="x",padx=20)
    def _mapa(self):
        for w in self.frame_mapa.winfo_children(): w.destroy()
        self.botones_asiento={}
        ruta=self.form.ruta_actual()
        ocup=datos.asientos_ocupados(ruta["id"], excluir_pasajero_id=self.p["id"])
        total=ruta["asientos"]; filas=(total+3)//4
        for fila in range(filas):
            row=tk.Frame(self.frame_mapa,bg=BG); row.pack(pady=1)
            for col in range(4):
                num=fila*4+col+1
                if num>total: tk.Frame(row,width=28,height=22,bg=BG).pack(side="left",padx=1); continue
                if col==2: tk.Frame(row,width=14,bg=BG).pack(side="left")
                lib=num not in ocup
                es_actual=(num==self.asiento_sel)
                bg_c=ACCENT if es_actual else (SUCCESS if lib else DANGER)
                b=tk.Button(row,text=str(num),width=2,height=1,
                            bg=bg_c,fg=WHITE,bd=0,font=("Segoe UI",7,"bold"),
                            state="normal" if lib or es_actual else "disabled",
                            cursor="hand2" if (lib or es_actual) else "arrow",
                            command=lambda n=num:self._sel(n))
                b.pack(side="left",padx=1); self.botones_asiento[num]=b
    def _sel(self,n):
        ruta=self.form.ruta_actual()
        ocup=datos.asientos_ocupados(ruta["id"], excluir_pasajero_id=self.p["id"])
        if self.asiento_sel in self.botones_asiento and self.asiento_sel not in ocup:
            self.botones_asiento[self.asiento_sel].config(bg=SUCCESS)
        self.asiento_sel=n; self.botones_asiento[n].config(bg=ACCENT)
        self.lbl_asiento.config(text=f"Asiento seleccionado: {n}")
    def _guardar(self):
        if not self.form.validar(): return
        ruta=self.form.ruta_actual()
        try:
            datos.modificar_pasajero(self.p["id"],
                                     self.form.v_nombre.get().strip(),
                                     self.form.v_dni.get(),
                                     self.form.v_telefono.get(),
                                     ruta["id"], self.asiento_sel,
                                     self.form.dp.get())
            messagebox.showinfo("Listo","Pasaje modificado correctamente.")
            self.on_guardado(); self.destroy()
        except ValueError as e: messagebox.showerror("Error",str(e))

# ─── Pasajeros ────────────────────────────────────────────────────────────────
class VistaPasajeros(tk.Frame):
    def __init__(self,parent,usuario):
        super().__init__(parent,bg=BG); self._lista_actual=None
        encabezado=tk.Frame(self,bg=BG); encabezado.pack(fill="x",padx=20,pady=(15,5))
        tk.Label(encabezado,text="Lista de Pasajeros",font=("Segoe UI",15,"bold"),bg=BG,fg=TEXT).pack(side="left")
        bframe=tk.Frame(encabezado,bg=BG); bframe.pack(side="right")
        tk.Button(bframe,text="Ordenar",bg=ACCENT,fg=WHITE,bd=0,
                  font=("Segoe UI",9,"bold"),padx=12,pady=5,cursor="hand2",
                  command=self._ordenar).pack(side="left",padx=4)
        tk.Button(bframe,text="Modificar",bg=WARN,fg=WHITE,bd=0,
                  font=("Segoe UI",9,"bold"),padx=12,pady=5,cursor="hand2",
                  command=self._modificar).pack(side="left",padx=4)
        tk.Button(bframe,text="Ver boleta",bg=ACCENT2,fg=WHITE,bd=0,
                  font=("Segoe UI",9,"bold"),padx=12,pady=5,cursor="hand2",
                  command=self._ver_boleta).pack(side="left",padx=4)
        tk.Button(bframe,text="Anular",bg=DANGER,fg=WHITE,bd=0,
                  font=("Segoe UI",9,"bold"),padx=12,pady=5,cursor="hand2",
                  command=self._anular).pack(side="left")
        cols=("ID","Nombre","DNI","Telefono","Destino","Asiento","Fecha","Precio")
        anchos=(40,150,80,90,100,65,90,70)
        style=ttk.Style(); style.configure("T.Treeview",background=CARD,foreground=TEXT,fieldbackground=CARD,rowheight=26)
        frame=tk.Frame(self,bg=CARD); frame.pack(fill="both",expand=True,padx=20,pady=(0,20))
        self.tv=ttk.Treeview(frame,columns=cols,show="headings",style="T.Treeview")
        sb=ttk.Scrollbar(frame,orient="vertical",command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        for c,a in zip(cols,anchos): self.tv.heading(c,text=c); self.tv.column(c,width=a,anchor="center")
        self.tv.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")
        self._refrescar(datos.PASAJEROS)
    def _refrescar(self,lista):
        self._lista_actual=lista; self.tv.delete(*self.tv.get_children())
        for p in lista:
            self.tv.insert("","end",iid=str(p["id"]),
                           values=(p["id"],p["nombre"],p["dni"],
                                   p.get("telefono","—"),p["destino"],
                                   p["asiento"],p["fecha"],f"S/ {p['precio']:.2f}"))
    def _seleccionado(self):
        sel=self.tv.selection()
        if not sel: messagebox.showwarning("Aviso","Selecciona un pasajero de la lista"); return None
        pid=int(sel[0])
        for p in datos.PASAJEROS:
            if p["id"]==pid: return p
        return None
    def _ordenar(self):
        DialogoOrdenar(self,lambda clave,fn:self._refrescar(fn(datos.PASAJEROS,lambda p:str(p[clave]))))
    def _modificar(self):
        p=self._seleccionado()
        if p: DialogoModificar(self,p,lambda:self._refrescar(datos.PASAJEROS))
    def _ver_boleta(self):
        p=self._seleccionado()
        if p: VentanaBoleta(self,p)
    def _anular(self):
        p=self._seleccionado()
        if not p: return
        if messagebox.askyesno("Confirmar",f"¿Anular pasaje N° {p['id']} de {p['nombre']}?"):
            datos.anular_pasajero(p["id"]); self._refrescar(datos.PASAJEROS)

# ─── Rutas ────────────────────────────────────────────────────────────────────
class VistaRutas(tk.Frame):
    def __init__(self,parent,usuario):
        super().__init__(parent,bg=BG)
        tk.Label(self,text="Gestion de Rutas",font=("Segoe UI",15,"bold"),bg=BG,fg=TEXT).pack(pady=12)
        contenedor=tk.Frame(self,bg=BG); contenedor.pack(fill="both",expand=True,padx=20)
        tframe=tk.Frame(contenedor,bg=CARD); tframe.pack(side="left",fill="both",expand=True)
        cols=("ID","Origen","Destino","Hora","Precio","Asientos"); anchos=(40,80,100,70,70,80)
        style=ttk.Style(); style.configure("R.Treeview",background=CARD,foreground=TEXT,fieldbackground=CARD,rowheight=26)
        self.tv=ttk.Treeview(tframe,columns=cols,show="headings",style="R.Treeview")
        for c,a in zip(cols,anchos): self.tv.heading(c,text=c); self.tv.column(c,width=a,anchor="center")
        self.tv.pack(fill="both",expand=True,padx=5,pady=5)
        self._refrescar()
        form=tk.Frame(contenedor,bg=CARD,padx=12,pady=12); form.pack(side="left",fill="y",padx=(12,0))
        tk.Label(form,text="Nueva Ruta",bg=CARD,fg=TEXT,font=("Segoe UI",11,"bold")).pack(pady=(0,10))
        self.v_origen=tk.StringVar(value="Lima"); self.v_destino=tk.StringVar()
        self.v_hora=tk.StringVar(); self.v_precio=tk.StringVar(); self.v_asientos=tk.StringVar(value="40")
        for lbl,var,modo,maxl in [("Origen",self.v_origen,"letra",50),
                                   ("Destino",self.v_destino,"letra",50),
                                   ("Hora (HH:MM)",self.v_hora,"num",5),
                                   ("Precio (S/)",self.v_precio,"num",6),
                                   ("Asientos",self.v_asientos,"num",3)]:
            tk.Label(form,text=lbl,bg=CARD,fg=SUBTEXT,font=("Segoe UI",9,"bold")).pack(anchor="w",pady=(6,1))
            e=ttk.Entry(form,textvariable=var,font=("Segoe UI",10),width=22); e.pack(anchor="w")
            if modo=="num": _registrar_validaciones(e,"num",maxl)
        tk.Button(form,text="+ Agregar ruta",bg=ACCENT,fg=WHITE,bd=0,
                  font=("Segoe UI",10,"bold"),pady=8,cursor="hand2",
                  command=self._agregar).pack(fill="x",pady=(14,0))
    def _refrescar(self):
        self.tv.delete(*self.tv.get_children())
        for r in datos.RUTAS:
            self.tv.insert("","end",values=(r["id"],r["origen"],r["destino"],
                           r["hora"],f"S/ {r['precio']:.2f}",r["asientos"]))
    def _agregar(self):
        try:
            datos.agregar_ruta(self.v_origen.get(),self.v_destino.get(),
                               self.v_hora.get(),float(self.v_precio.get()),int(self.v_asientos.get()))
            self._refrescar(); self.v_destino.set(""); self.v_hora.set(""); self.v_precio.set("")
        except Exception as e: messagebox.showerror("Error",str(e))

# ─── Reporte ──────────────────────────────────────────────────────────────────
def _grafico_barras(canvas, datos_dict, titulo, color_barra=ACCENT, invertido=False):
    canvas.delete("all"); w=canvas.winfo_width() or 500; h=canvas.winfo_height() or 300
    if not datos_dict: canvas.create_text(w//2,h//2,text="Sin datos aun",fill=SUBTEXT,font=("Segoe UI",10)); return
    items=sorted(datos_dict.items(),key=lambda x:x[1],reverse=invertido)
    max_val=max(datos_dict.values()) or 1
    margen_izq=160; margen_der=20; margen_sup=40; margen_inf=20
    ancho_grafico=w-margen_izq-margen_der; alto_grafico=h-margen_sup-margen_inf
    n=len(items); alto_barra=min(28,(alto_grafico-10*(n-1))//max(n,1)); separacion=10
    if titulo: canvas.create_text(w//2,18,text=titulo,fill=TEXT,font=("Segoe UI",10,"bold"))
    for idx,(etiqueta,valor) in enumerate(items):
        y=margen_sup+idx*(alto_barra+separacion)
        canvas.create_text(margen_izq-8,y+alto_barra//2,text=str(etiqueta)[:22],
                           fill=TEXT,font=("Segoe UI",8),anchor="e")
        largo=int(valor/max_val*ancho_grafico)
        canvas.create_rectangle(margen_izq,y,margen_izq+largo,y+alto_barra,fill=color_barra,outline="")
        canvas.create_text(margen_izq+largo+5,y+alto_barra//2,
                           text=str(valor),fill=TEXT,font=("Segoe UI",8,"bold"),anchor="w")

class VistaReporte(tk.Frame):
    def __init__(self,parent,usuario):
        super().__init__(parent,bg=BG)
        tk.Label(self,text="Reportes y Estadisticas",font=("Segoe UI",15,"bold"),bg=BG,fg=TEXT).pack(pady=(12,8))
        nb=ttk.Notebook(self); nb.pack(fill="both",expand=True,padx=15,pady=(0,15))
        t1=tk.Frame(nb,bg=BG); t2=tk.Frame(nb,bg=BG); t3=tk.Frame(nb,bg=BG)
        nb.add(t1,text="  Ventas por destino  ")
        nb.add(t2,text="  Ranking pasajeros  ")
        nb.add(t3,text="  Uso de algoritmos  ")
        self._tab_ventas(t1); self._tab_ranking(t2); self._tab_algoritmos(t3)
    def _tab_ventas(self,parent):
        conteo={}
        for p in datos.PASAJEROS: conteo[p["destino"]]=conteo.get(p["destino"],0)+1
        pares=merge_sort([{"dest":k,"cnt":v} for k,v in conteo.items()],lambda x:x["cnt"])
        pares.reverse(); datos.registrar_uso_metodo("Merge Sort")
        cards=tk.Frame(parent,bg=BG); cards.pack(fill="x",padx=20,pady=10)
        total_ventas=len(datos.PASAJEROS)
        total_ingresos=sum(p["precio"] for p in datos.PASAJEROS)
        for titulo,valor in [("Total ventas",str(total_ventas)),
                              ("Ingresos (S/)",f"{total_ingresos:.2f}"),
                              ("Rutas activas",str(len(datos.RUTAS)))]:
            c=tk.Frame(cards,bg=CARD,padx=20,pady=15); c.pack(side="left",fill="x",expand=True,padx=5)
            tk.Label(c,text=valor,font=("Segoe UI",18,"bold"),bg=CARD,fg=ACCENT).pack()
            tk.Label(c,text=titulo,font=("Segoe UI",9),bg=CARD,fg=SUBTEXT).pack()
        tk.Label(parent,text="Pasajes vendidos por destino (Merge Sort)",
                 bg=BG,fg=SUBTEXT,font=("Segoe UI",8,"italic")).pack()
        canvas=tk.Canvas(parent,bg=CARD,highlightthickness=0,height=220)
        canvas.pack(fill="x",padx=20,pady=5)
        datos_grafico={p["dest"]:p["cnt"] for p in pares}
        canvas.after(50,lambda:_grafico_barras(canvas,datos_grafico,"",ACCENT,invertido=True))
    def _tab_ranking(self,parent):
        tk.Label(parent,text="Top pasajeros por precio pagado (Quick Sort descendente)",
                 bg=BG,fg=SUBTEXT,font=("Segoe UI",9,"italic")).pack(pady=8)
        ordenados=quick_sort(datos.PASAJEROS,lambda p:p["precio"])
        ordenados.reverse(); datos.registrar_uso_metodo("Quick Sort")
        cols=("Pos","Nombre","Destino","Precio","Fecha"); anchos=(40,180,110,80,90)
        style=ttk.Style(); style.configure("K.Treeview",background=CARD,foreground=TEXT,fieldbackground=CARD,rowheight=26)
        frame=tk.Frame(parent,bg=CARD); frame.pack(fill="both",expand=True,padx=20,pady=(0,15))
        tv=ttk.Treeview(frame,columns=cols,show="headings",style="K.Treeview")
        for c,a in zip(cols,anchos): tv.heading(c,text=c); tv.column(c,width=a,anchor="center")
        for pos,p in enumerate(ordenados,1):
            tv.insert("","end",values=(pos,p["nombre"],p["destino"],f"S/ {p['precio']:.2f}",p["fecha"]))
        sb=ttk.Scrollbar(frame,orient="vertical",command=tv.yview); tv.configure(yscrollcommand=sb.set)
        tv.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")
    def _tab_algoritmos(self,parent):
        tk.Label(parent,text="Veces que se uso cada algoritmo de ordenamiento",
                 bg=BG,fg=SUBTEXT,font=("Segoe UI",9,"italic")).pack(pady=8)
        canvas=tk.Canvas(parent,bg=CARD,highlightthickness=0,height=200)
        canvas.pack(fill="x",padx=20,pady=5)
        canvas.after(50,lambda:_grafico_barras(canvas,datos.USO_METODOS,"",ACCENT2,invertido=True))
        cols=("Algoritmo","Complejidad","Usos"); anchos=(150,120,80)
        style=ttk.Style(); style.configure("A.Treeview",background=CARD,foreground=TEXT,fieldbackground=CARD,rowheight=26)
        frame=tk.Frame(parent,bg=CARD); frame.pack(fill="x",padx=20,pady=8)
        tv=ttk.Treeview(frame,columns=cols,show="headings",style="A.Treeview",height=5)
        for c,a in zip(cols,anchos): tv.heading(c,text=c); tv.column(c,width=a,anchor="center")
        complejidades={"Burbuja":"O(n2)","Seleccion":"O(n2)","Insercion":"O(n2)",
                       "Merge Sort":"O(n log n)","Quick Sort":"O(n log n)"}
        for alg,usos in datos.USO_METODOS.items():
            tv.insert("","end",values=(alg,complejidades.get(alg,""),usos))
        tv.pack(fill="x")

if __name__ == "__main__":
    VentanaLogin().mainloop()
