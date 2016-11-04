from urllib2 import urlopen, quote
import requests

#peticion = 'http://sci-hub.io/10.1016/j.bbrc.2016.01.082'
#peticion = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-84990240104&origin=inward&txGid=2689025B55C8D857323CF414538C282C.wsnAw8kcdt7IPYLO0V48gA%3a26'
#~ peticion = 'http://ac.els-cdn.com/S1566253516300641/1-s2.0-S1566253516300641-main.pdf?_tid=190a2696-9b33-11e6-b5b5-00000aacb362&acdnat=1477455625_484d91e3a4bda95d789e9b8b107e3eae'
#~ url = (peticion)
#~ respuesta = urlopen(url)
#~ descarga = respuesta.read()
#~ #print descarga
#~ filename = 'prueba'+'.pdf'
#~ ruta = '/home/master/doc_pruebas/a.1/'
#~ f=open(ruta+filename, "w")
#~ f.write(descarga)
#~ f.close()


resp = requests.get('http://api.elsevier.com/content/article/eid/1-s2.0-S0006291X16300821',headers={'Accept': 'application/pdf', 'X-ELS-APIKey': 'b50e60b193e884e6d78948e916d816a0'})
ruta = '/home/master/doc_pruebas/a.1/'
filename = 'prueba'+'.pdf'
f=open(ruta+filename, "w")
f.write(resp.content)
f.close()
