from urllib2 import urlopen, quote
import xml.etree.ElementTree as ET
import traceback
import copy
import requests


# Esta clase sirve para conectarse con scopus y obtener datos de alli
class Descarga:
    # COnstructor con valores por defecto para una busqueda
    def __init__(self):
        #print "1"
        self.url = "http://api.elsevier.com/content/search/scopus"
        self.consulta = self.codificar_a_url("heart")
        self.parametros = "&view=COMPLETE&httpAccept=application/xml&apiKey=b50e60b193e884e6d78948e916d816a0&count=100"

    def __init__(self, query, start=0):
        #print "2"
        self.url = "http://api.elsevier.com/content/search/index:scopus"
        self.consulta = self.codificar_a_url(query)
        self.raw_consulta = query
        self.parametros = "&view=COMPLETE&httpAccept=application/xml&apiKey=b50e60b193e884e6d78948e916d816a0&count=100&start=" + str(
            start)
        self.parametros = "&httpAccept=application/xml&apiKey=b50e60b193e884e6d78948e916d816a0&count=25&start=" + str(
            start)
        self.construir_peticion()

    # Construye, a partir de los atributos de la clase, la url para hacer la peticion a scopus
    def buscar_por_doi(self):
        self.url = 'http://api.elsevier.com/content/article/'
        # self.peticion = self.url+'DOI:'+self.codificar_a_url('['+self.consulta+']')+ '?httpAccept=application/pdf'
        self.peticion = self.url + 'DOI:[' + self.consulta + ']?httpAccept=application/pdf'
        self.peticionXML = self.url + 'DOI:[' + self.consulta + ']?httpAccept=text/xml'

    def construir_peticion(self):
        self.peticion = self.url + "?query=" + self.consulta + self.parametros
        return self.peticion

    # Codifica la consulta en bruto(string) a la forma que puede entender la url
    def codificar_a_url(self, consulta):
        consulta_formateada = quote(consulta.encode("utf8"))
        return consulta_formateada

    # Hace la peticion al url y devuelve la respuesta
    def obtener_respuesta(self, peticion):
        #print "peticion"
        #print peticion
        url = (peticion)
        #print "url"
        #print url[0:100]
        # Archivo web

        respuesta = urlopen(url)

        return respuesta

    def descargar_xml(self, xml, filename):
        #print "descarga xml"
        f = open(filename + '.xml', "w")
        respuesta = xml.read()
        f.write(respuesta)
        f.close

    # Escribe la respuesta del url en un archivo
    def descargar(self, ruta):
        #print "descarga xml"
        titulo = ''
        eid = ''
        try:
            # r = self.obtener_respuesta(self.peticionXML)
            # titulo = self.obtener_metadatos(r, '{http://purl.org/dc/elements/1.1/}title')[0]
            #print "before peticion"
            r = self.obtener_respuesta(self.peticion)
            # Nombre del archivo a partir del URL
            # filename = self.raw_consulta.replace('/','s').replace('.','p')+".pdf"

            #print "before answer"
            respuesta = r.read()
            #print "respuesta"
            xml = self.obtener_respuesta(self.peticionXML)
            titulo_eid = self.obtener_metadatos(xml, ['{http://purl.org/dc/elements/1.1/}title',
                                                      '{http://www.elsevier.com/xml/svapi/article/dtd}eid'])
            titulo = titulo_eid[0]
            eid = titulo_eid[1]
            filename = titulo + '.pdf'

            # Verificar si es un xml
            if (not '<full-text-retrieval' in respuesta):
                #print "begining download"
                # f = open(filename, "w")
                # f=open("/home/administrador/ManejoVigtech/ArchivosProyectos/" + filename, "w")
                f = open(ruta + filename, "w")
                # Escribir en un nuevo fichero local los datos obtenidos via HTTP.
                f.write(respuesta)
                # Cerrar ambos
                f.close()
                print "%s descargado correctamente." % filename
                #print titulo
            else:
                # ~ try:
                #print "doi"
                doi = self.consulta
                #print doi
                JOURNAL_RESOURCES_URL = {'journal_key': 'http://link.springer.com/content/pdf/{doi}.pdf'}
                #print "jou"
                pdf_url = JOURNAL_RESOURCES_URL['journal_key'].format(doi=doi)
                #print pdf_url
                resp = requests.get(pdf_url,
                                    headers={'Accept': 'application/pdf'})
                pdf_file_path = ruta + filename

                if resp:
                    if '<!DOCTYPE html>' not in resp.text and '</html>' not in resp.text:
                        #print "open"
                        with open(pdf_file_path, 'w') as file_:
                            file_.write(resp.content)
                            file_.close()

            return (titulo, eid)
            r.close()

        except Exception:
            print "excepcion capturada intentando obtener el articulo de sprinnger"
            doi = self.consulta
            print doi
            JOURNAL_RESOURCES_URL = {'journal_key': 'http://link.springer.com/content/pdf/{doi}.pdf'}
            print "jou"
            pdf_url = JOURNAL_RESOURCES_URL['journal_key'].format(doi=doi)
            print pdf_url
            resp = requests.get(pdf_url,
                                headers={'Accept': 'application/pdf'})
            doi_name = doi.replace('/','-')
            print doi_name
            pdf_file_path = ruta + doi_name + '.pdf'
            print  pdf_file_path

            if resp:
                if '<!DOCTYPE html>' not in resp.text and '</html>' not in resp.text:
                    print "open"
                    with open(pdf_file_path, 'w') as file_:
                        file_.write(resp.content)
                        file_.close()
        return (titulo, eid)

    def obtener_metadatos(self, xml, campos):
        respuesta = []
        tree = ET.parse(xml)
        root = tree.getroot()
        for child in root:
            for campito in child:
                for campo in campos:
                    # print campito.tag
                    if campito.tag == campo:
                        # print campito.text, campito.tag
                        respuesta.append(campito.text)
        return respuesta


'''
def main():
	d = Descarga("Hola( a")
	print d.construir_peticion()

main()'''
# d = Descarga('AUTHOR-NAME ( aranda,  AND  j )')
# d.descargar_xml(d.obtener_respuesta(d.peticion))
