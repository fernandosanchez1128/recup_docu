from administradorConsultas import AdministradorConsultas

import threading
import os




def worker(query,tema,year,directorio):
    administrador = AdministradorConsultas()
    print query
    administrador.consulta(query,tema,year,directorio)


temas = ['astronomy', 'medicine', 'politics', 'robotics']
directory = "/home/master/doc_pruebas2/"
for tema in temas:
    for year in range (2010,2017):

        query = 'TITLE-ABS-KEY (' + tema + ')  AND  DOCTYPE (ar OR re ) AND  LANGUAGE ( english )  AND  PUBYEAR  = '+ str (year)
        ruta  = directory + tema + '.' + str (year)
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        try:
            t = threading.Thread(target=worker, args=(query,tema,year,directory))
            t.start()
        except:
            print "hilo finalizado"


