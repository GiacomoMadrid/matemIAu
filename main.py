from vista.frm_Principal import Ventana
from controlador.Controlador_Principal import Controlador_Principal

if __name__== "__main__" :
    vista = Ventana()
    controlador_principal = Controlador_Principal(vista)
    controlador_principal.run()