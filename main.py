import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.ttk import Treeview

url = requests.get("https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx")

listaMonedas = []

class TipoDeCambio:

    def __init__(self,window):
        self.wind = window
        self.wind.title('Tipos de cambios sbs')
        self.wind.geometry('620x500')

        btnMostrar = Button(self.wind,text='Mostrar',command=self.scrapping_tipocambio)
        btnMostrar.grid(row=0,column=0,pady=10)

        self.TrvMonedas = Treeview(height=7,columns=("#0","#1"))
        self.TrvMonedas.grid(row=1,column=0,padx=10,pady=10)
        self.TrvMonedas.heading('#0',text='MONEDA',ancho=CENTER)
        self.TrvMonedas.heading('#1',text='COMPRA (S/)',ancho=CENTER)
        self.TrvMonedas.heading('#2',text='VENTA (S/)',ancho=CENTER)

        btnExportar = Button(self.wind,text='Exportar',command=self.Exportar)
        btnExportar.grid(row=2,column=0)


    def scrapping_tipocambio(self):
        if(url.status_code == 200):
            html = BeautifulSoup(url.text,'html.parser')
            
            for i in range(7):
                fila = html.find('tr',{'id':'ctl00_cphContent_rgTipoCambio_ctl00__'+str(i)}) 
                moneda = fila.find('td',{'class':'APLI_fila3'})
                compra = fila.find('td',{'class':'APLI_fila2'})
                venta = fila.find('td',{'class':'APLI_fila2'}).findNext('td')
                dictMoneda = {
                    'moneda': moneda.get_text(),
                    'compra': compra.get_text(),
                    'venta': venta.get_text()
                }
                listaMonedas.append(dictMoneda)
                self.TrvMonedas.insert('',END,text=moneda.get_text(),values=[compra.get_text(),venta.get_text()])

        else:
            print("error " + str(url.status_code))

    def Exportar(self):
        strMonedas = ""
        for l in listaMonedas:
            for clave,valor in l.items():
                strMonedas += valor
                if clave != 'venta':
                    strMonedas += ';'
                else:
                    strMonedas += '\n'

        fw = open('TipoDeCambio.csv','w')
        fw.write(strMonedas)
        fw.close()
        

if __name__ == "__main__":
    window = Tk()
    app = TipoDeCambio(window)
    window.mainloop()