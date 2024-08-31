import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QTableView, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main_window.ui', self)

        # Entradas
        self.lineEdit_Nombre = self.findChild(QLineEdit, 'lineEdit_Nombre')
        self.lineEdit_Edad = self.findChild(QLineEdit, 'lineEdit_Edad')
        self.lineEdit_Peso = self.findChild(QLineEdit, 'lineEdit_Peso')
        self.lineEdit_Altura = self.findChild(QLineEdit, 'lineEdit_Altura')

        # Botones
        self.btnAgregar = self.findChild(QPushButton, 'btnAgregar')
        self.btnAgregar.clicked.connect(self.agregarPersona)

        self.btnSiguiente = self.findChild(QPushButton, 'btnSiguiente')
        self.btnSiguiente.clicked.connect(self.mostrarSiguientePagina)

        self.btnAtras = self.findChild(QPushButton, 'btnAtras')
        self.btnAtras.clicked.connect(self.mostrarPaginaAnterior)
        self.btnAtras.setEnabled(False)  # Inicialmente desactivado

        # Table View
        self.tableView = self.findChild(QTableView, 'tableView')
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Nombre', 'Edad', 'Peso', 'Altura', 'IMC'])
        self.tableView.setModel(self.model)

        # Otras variables
        self.datos = []  # Lista para almacenar los datos
        self.pagina_actual = 0  # Página actual

        # Configurar la paginación inicial
        self.actualizarPaginacion()

    def agregarPersona(self):
        nombre = self.lineEdit_Nombre.text()
        edad_text = self.lineEdit_Edad.text()
        peso_text = self.lineEdit_Peso.text()
        altura_text = self.lineEdit_Altura.text()

        # Validaciones
        try:
            edad = int(edad_text)
            peso = float(peso_text)
            altura = float(altura_text)

            if edad <= 0 or peso <= 0 or altura <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Por favor, ingrese valores válidos para Edad, Peso y Altura.')
            return

        # Calcular el IMC
        imc = peso / ((altura / 100) ** 2)  # Convertir altura a metros

        # Añadir datos a la lista
        self.datos.append([nombre, str(edad), str(peso), str(altura), f'{imc:.2f}'])

        # Actualizar la paginación
        self.actualizarPaginacion()

        # Limpiar los campos
        self.lineEdit_Nombre.clear()
        self.lineEdit_Edad.clear()
        self.lineEdit_Peso.clear()
        self.lineEdit_Altura.clear()

    def mostrarSiguientePagina(self):
        self.pagina_actual += 1
        self.actualizarPaginacion()

    def mostrarPaginaAnterior(self):
        self.pagina_actual -= 1
        self.actualizarPaginacion()

    def actualizarPaginacion(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Nombre', 'Edad', 'Peso', 'Altura', 'IMC'])

        inicio = self.pagina_actual * 10
        fin = inicio + 10

        for datos in self.datos[inicio:fin]:
            rowPosition = self.model.rowCount()
            self.model.insertRow(rowPosition)
            for col, dato in enumerate(datos):
                self.model.setItem(rowPosition, col, QStandardItem(dato))

        self.btnSiguiente.setEnabled(fin < len(self.datos))
        self.btnAtras.setEnabled(self.pagina_actual > 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    print('Fin del programa')