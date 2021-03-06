from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QCheckBox
import sqlite3
from PyQt5.QtCore import Qt, QRect
import sys
import subprocess as sp
import requests
import json
import time

def listar_vacas(pesquisar):
   request = requests.get("http://localhost:8080/vacas?cor="+pesquisar)
   todos = json.loads(request.content)
   montaTabela(todos)

def lista_vacas_inicial(pesquisar):
    aux = 50
    progresso.carregar.setVisible(False)
    while True:
        try:
            request = requests.get("http://localhost:8080/vacas?cor="+pesquisar)
            break
        except:
            progresso.progresso.setValue(aux)
            aux += 30
    progresso.progresso.setValue(100)
    time.sleep(1)
    progresso.close()
    todos = json.loads(request.content)
    montaTabela(todos)
    interface.show()


def montaTabela(todos):
    i = 0;
    interface.tabela.setRowCount(len(todos))
    interface.tabela.setColumnCount(9)
    campos = ['nome', 'numero', 'ensiminacao', 'secagem', 'parto', 'novaEnsiminacao', 'nCrias', 'repeticao', 'diasLactacao']
    for j in todos:
        aux = str(j['cor']).split()
        cor = QtGui.QColor(int(aux[0]), int(aux[1]), int(aux[2]))
        for z in range(9):
            aux = str(j[campos[z]])
            interface.tabela.setItem(i, z, QtWidgets.QTableWidgetItem(aux))
            interface.tabela.item(i, z).setBackground(cor)
        i+=1
    interface.tabela.resizeColumnsToContents()

def pesquisar():
    nome = interface.pesquisar_3.text()
    if nome == "":
        listar_vacas("");
    else:
        if "/" in nome:
           nome = nome.replace("/", "-")
        res = requests.get(f"http://localhost:8080/vacas/pesquisa?str="+nome)
        todos = json.loads(res.content)
        montaTabela(todos)

def calcular():
    if not verifica_valor_numero():
       return
    linha = interface.tabela.currentRow()
    numero = interface.tabela.item(linha, 1).text()
    valor = calc.data.date()
    dia = str(valor.day())
    mes = str(valor.month())
    ano = str(valor.year())
    if len(dia) < 2:
        dia = "0" + dia
    if len(mes) < 2:
        mes = "0" + mes
    data = dia + "-" + mes + "-" + ano
    res = requests.get(f"http://localhost:8080/vacas/calcular/{numero}/{data}")
    calc.close()
    valor = 0
    listar_vacas('')

def cadastrar():
    nome = nova.nome.text()
    numero = nova.numero.text()
    crias = nova.crias.text()
    res = requests.get(f"http://localhost:8080/vacas/cadastrar/{numero}/{nome}?n="+crias)
    if res.status_code == 200:
        mostraMsgm("Iforma????o", f"A vaca {nome} foi cadastrada no sistema!")
        nova.nome.setText("")
        nova.numero.setText("")
        if crias != 0:
            nova.crias.setText("0")
        listar_vacas('')
    else:
        mostraMsgm("Erro", "O numero digitade pertence a outra vaca!")

def deletar():
   if not verifica_valor_numero():
      return
   linha = interface.tabela.currentRow()
   if mostraMsgmBtn("Tem certeza", "Voce deseja deletar a vaca '"
                    +interface.tabela.item(linha, 0).text()+"'?") == QMessageBox.Ok:
      numero = interface.tabela.item(linha, 1).text()
      try:
         request = requests.get("http://localhost:8080/vacas/deletar/"+numero)
         mostraMsgm("Vaca deletada!", f"A vaca '{interface.tabela.item(linha, 0).text()}' foi deletada do sistema")
         listar_vacas('')
      except:
         mostraMsgm("Erro", f"N??o foi poss??vel deletar a vaca {interface.tabela.item(linha, 0).text()}")

def alterarFunc():
   if not verifica_valor_numero():
      return
   linha = interface.tabela.currentRow()
   numero = interface.tabela.item(linha, 1).text()
   nome = alterar.editAlterar.text()
   try:
      request = requests.get("http://localhost:8080/vacas/alterar/"+numero+"/"+nome)
      mostraMsgm("Vaca deletada!", f"A vaca {interface.tabela.item(linha, 0).text()} foi alterada no sistema")
      listar_vacas('')
   except:
      mostraMsgm("Erro", f"N??o foi poss??vel alterar a vaca {interface.tabela.item(linha, 0).text()}")
   alterar.editAlterar.setText("")
   alterar.close()

def mostra_alterar():
   alterar.show()

def secar():
   if not verifica_valor_numero():
      return
   linha = interface.tabela.currentRow()
   if mostraMsgmBtn("Tem certeza", "Voce deseja secar a vaca '"
                   +interface.tabela.item(linha, 0).text()+"'?") == QMessageBox.Ok:
      numero = interface.tabela.item(linha, 1).text()
      try:
         request = requests.get("http://localhost:8080/vacas/secar/"+numero)
         mostraMsgm("Vaca Secada!", f"A vaca {interface.tabela.item(linha, 0).text()} foi secada no sistema")
         listar_vacas('')
      except:
         mostraMsgm("Erro", f"N??o foi poss??vel secar a vaca {interface.tabela.item(linha, 0).text()}")


def parto():
   if not verifica_valor_numero():
      return
   linha = interface.tabela.currentRow()
   if mostraMsgmBtn("Tem certeza", "Voce deseja mudar a data do parto da vaca '"
                    +interface.tabela.item(linha, 0).text()+"' para hoje?") == QMessageBox.Ok:
      numero = interface.tabela.item(linha, 1).text()
      try:
         request = requests.get("http://localhost:8080/vacas/parto/"+numero)
         mostraMsgm("Parto Modificado!", f"A vaca {interface.tabela.item(linha, 0).text()} teve seu parto cadastrado no sistema")
         listar_vacas('')
      except:
         mostraMsgm("Erro", f"N??o foi poss??vel cadastrar o parto da a vaca {interface.tabela.item(linha, 0).text()}")


def zerar():
   if not verifica_valor_numero():
      return
   linha = interface.tabela.currentRow()
   
   if mostraMsgmBtn("Tem certeza", "Voce deseja zerar as datas da vaca '"
                    +interface.tabela.item(linha, 0).text()+"'?") == QMessageBox.Ok:
      numero = interface.tabela.item(linha, 1).text()
      try:
         request = requests.get("http://localhost:8080/vacas/zerar/"+numero)
         mostraMsgm("Data Zerada!", f"A vaca {interface.tabela.item(linha, 0).text()} teve suas datas zeradas no sistema")
         listar_vacas('')
      except:
         mostraMsgm("Erro", f"N??o foi poss??vel zerar as datas da a vaca {interface.tabela.item(linha, 0).text()}")


def verifica_btn_alterar():
   if alterar.editAlterar.text() != "":
      alterar.alterar.setEnabled(True)
   else:
      alterar.alterar.setEnabled(False)

def verifica_nova():
   if nova.nome.text() != "" and len(nova.numero.text()) == 6 and nova.numero.text().isdigit() and nova.crias.text().isdigit() and len(nova.crias.text()) >= 1:
      nova.cadastrar.setEnabled(True)
   else:
      nova.cadastrar.setEnabled(False)

def mostraMsgmBtn(titulo, mensagem):
   msg = QMessageBox()
   msg.setWindowTitle(titulo)
   msg.setText(mensagem)
   msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
   msg.setWindowIcon(QtGui.QIcon("vacas.ico"))
   msg.setDefaultButton(QMessageBox.Cancel)
   return msg.exec_()

def mostraMsgm(titulo, msgm):
    msg = QMessageBox()
    msg.setWindowTitle(titulo)
    msg.setText(msgm)
    msg.setWindowIcon(QtGui.QIcon("vacas.ico"))
    msg.setStyleSheet("background-color: darkGray;")
    #msg.show()
    return msg.exec_()
        

def nova_func():    
    nova.show()

def calcularMostrar():
    calc.show()

        #Criando a aplica????o
app = QtWidgets.QApplication([])

class VacasFront(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("interface.ui", self)

    def closeEvent(self, event):
        url = 'http://localhost:8080/actuator/shutdown'
        x = requests.post(url)

def verifica_valor_numero():
   try:
      linha = interface.tabela.currentRow()
      numero = interface.tabela.item(linha, 1).text()
      return True
   except:
      mostraMsgm("Erro", "Selecione uma vaca primeiro")
      return False
   

        #importando as interfaces
interface = VacasFront()
#interface = uic.loadUi("interface.ui")
nova = uic.loadUi("nova.ui")
calc = uic.loadUi("calcular.ui")
progresso = uic.loadUi("progresso.ui")
alterar = uic.loadUi("alterar.ui")


        #Definindo alguns estilos
interface.setWindowTitle("Cadastro de Vacas")
interface.setWindowIcon(QtGui.QIcon("vacas.ico"))
nova.setWindowIcon(QtGui.QIcon("vacas.ico"))
calc.setWindowIcon(QtGui.QIcon("vacas.ico"))
progresso.setWindowIcon(QtGui.QIcon("vacas.ico"))
alterar.setWindowIcon(QtGui.QIcon("vacas.ico"))
interface.centralwidget.setStyleSheet("QWidget#tab{background-color: black;}QWidget#tab_2{background-color: black;}QTableWidget::item#tabela{ selection-background-color: blue; selection-color: black;}")                                    

        #Configurando Bot??es De Pesquisa
interface.todas_2.clicked.connect(lambda:listar_vacas(''))
interface.nova_vaca_2.clicked.connect(lambda:listar_vacas('255 255 0'))
interface.todas.clicked.connect(lambda:listar_vacas('128 128 128'))
interface.calcular_3.clicked.connect(lambda:listar_vacas('0 255 0'))
interface.pesquisar_2.clicked.connect(lambda:listar_vacas('255 0 0'))
interface.pesquisar_3.textChanged.connect(pesquisar)

        #Configurando Bot??es De CRUD
interface.nova_vaca.clicked.connect(nova_func)
nova.cadastrar.clicked.connect(cadastrar)
nova.nome.textChanged.connect(verifica_nova)
nova.numero.textChanged.connect(verifica_nova)
nova.crias.textChanged.connect(verifica_nova)
interface.calcular.clicked.connect(calcularMostrar)
calc.calc.clicked.connect(calcular)
interface.deletar.clicked.connect(lambda: deletar())
interface.alterar.clicked.connect(lambda: mostra_alterar())
interface.secar.clicked.connect(lambda: secar())
alterar.alterar.clicked.connect(lambda: alterarFunc())
interface.parto.clicked.connect(lambda: parto())
alterar.editAlterar.textChanged.connect(lambda: verifica_btn_alterar())
interface.zarar.clicked.connect(lambda: zerar())
progresso.carregar.clicked.connect(lambda: lista_vacas_inicial(''))

##try:
##    sp.Popen([".\\vacas.jar"],
##             shell=True)
##except:
##    mostraMsgm("Falha ao subir o servidor", "Certifique-se de que o arquivo 'vacas.jar'"+
##              "esteja na mesma pasta que esse .exe !!!!")
##    sys.exit ()

try:
    progresso.show()
    app.exec()
finally:
   try:
      time.sleep(25)
      print("Try finally")
      url = 'http://localhost:8080/actuator/shutdown'
      requests.post(url)
   except:
      sys.exit ()
