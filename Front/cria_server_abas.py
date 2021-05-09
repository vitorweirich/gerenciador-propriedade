from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QCheckBox
import sqlite3
from PyQt5.QtCore import Qt, QRect
import sys
import requests
import requests
import json

def listar_vacas(pesquisar):
    request = requests.get("http://localhost:8080/vacas?cor="+pesquisar)
    todos = json.loads(request.content)
    montaTabela(todos)

def montaTabela(todos):
    i = 0;
    interface.tabela.setRowCount(len(todos))
    interface.tabela.setColumnCount(7)
    for j in todos:
        aux = j['cor']
        if aux == 'vermelho':
            cor = Qt.red
        elif aux == 'verde':
            cor = Qt.green
        elif aux == 'cinza':
            cor = Qt.gray
        elif aux == 'amarelo':
            cor = Qt.yellow
        else:
            cor = Qt.white
        aux = j['nome']
        interface.tabela.setItem(i,0,QtWidgets.QTableWidgetItem(aux))
        interface.tabela.item(i, 0).setBackground(cor)
        aux = j['numero']
        interface.tabela.setItem(i,1,QtWidgets.QTableWidgetItem(aux))
        interface.tabela.item(i, 1).setBackground(cor)
        aux = j['ensiminacao']
        interface.tabela.setItem(i,2,QtWidgets.QTableWidgetItem(aux))
        interface.tabela.item(i, 2).setBackground(cor)
        aux = j['secagem']
        interface.tabela.setItem(i,3,QtWidgets.QTableWidgetItem(aux))
        interface.tabela.item(i, 3).setBackground(cor)
        aux = j['parto']
        interface.tabela.setItem(i,4,QtWidgets.QTableWidgetItem(aux))
        interface.tabela.item(i, 4).setBackground(cor)
        aux = j['novaEnsiminacao']
        interface.tabela.setItem(i,5,QtWidgets.QTableWidgetItem(aux))
        interface.tabela.item(i, 5).setBackground(cor)
        aux = j['nCrias']
        interface.tabela.setItem(i,6,QtWidgets.QTableWidgetItem(str(aux)))
        interface.tabela.item(i, 6).setBackground(cor)
        i+=1
    interface.tabela.resizeColumnsToContents()

def pesquisar():
    nome = interface.pesquisar_3.text()
    if nome == "":
        listar_vacas("");
    else:
        if "/" in nome:
           nome = nome.replace("/", "-")
        print(nome)
        res = requests.get(f"http://localhost:8080/vacas/pesquisa?str="+nome)
        todos = json.loads(res.content)
        montaTabela(todos)

def calcular():
    linha = interface.tabela.currentRow()
    numero = interface.tabela.item(linha, 1).text()
    print(numero)
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
        mostrMsgm("Iformação", f"A vaca {nome} foi cadastrada no sistema!")
        nova.nome.setText("")
        nova.numero.setText("")
        if crias != 0:
            nova.crias.setText("0")
        listar_vacas('')
    else:
        mostrMsgm("Erro", "O numero digitade pertence a outra vaca!")

def mostrMsgm(titulo, msgm):
    msg = QMessageBox()
    msg.setWindowTitle(titulo)
    msg.setText(msgm)
    x = msg.exec_()
        

def nova_func():    
    nova.show()

def calcularMostrar():
    calc.show()

        #Criando a aplicação
app = QtWidgets.QApplication([])

        #importando as interfaces
interface = uic.loadUi("interface.ui")
nova = uic.loadUi("nova.ui")
calc = uic.loadUi("calcular.ui")


        #Definindo alguns estilos
interface.setWindowTitle("Cadastro de Vacas")
interface.setWindowIcon(QtGui.QIcon("vacas.ico"))
interface.centralwidget.setStyleSheet("QWidget#tab{background-color: black;}QWidget#tab_2{background-color: black;}QTableWidget::item#tabela{ selection-background-color: blue; selection-color: black;}")                                    

        #Configurando Botões De Pesquisa
interface.todas_2.clicked.connect(lambda:listar_vacas(''))
interface.nova_vaca_2.clicked.connect(lambda:listar_vacas('amarelo'))
interface.todas.clicked.connect(lambda:listar_vacas('cinza'))
interface.calcular_3.clicked.connect(lambda:listar_vacas('verde'))
interface.pesquisar_2.clicked.connect(lambda:listar_vacas('vermelho'))
interface.pesquisar_3.textChanged.connect(pesquisar)

        #Configurando Botões De CRUD
interface.nova_vaca.clicked.connect(nova_func)
nova.cadastrar.clicked.connect(cadastrar)
interface.calcular.clicked.connect(calcularMostrar)
calc.calc.clicked.connect(calcular)



listar_vacas('')
interface.show()
app.exec()
