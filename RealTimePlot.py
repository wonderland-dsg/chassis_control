# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 19:48:54 2013

@author: Mauricio
"""
import sys
from PyQt4 import QtGui,QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import Serial_KL25Z as serial

"""
Classe responsavel pela criação do objeto de plotagem 
"""
class MplCanvas(FigureCanvas):
    
    def __init__(self):    
        self.fig = Figure()
        FigureCanvas.__init__(self,self.fig)                            #Instancia o Canvas para a renderização
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,   #Configura a politica de tamanho 
                                       QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
"""
Classe responsavel pela criacao da aplicacao (widget)
"""    
MAXY=10
MAXITERS = 500                                                           #Define o alcance em tempo real do eixo X na tela
class CPUMonitor(QtGui.QWidget):
    def __init__(self, parent = None):
        super(CPUMonitor, self).__init__(parent)
        #Set's Iniciais e Criação dos Objetos
        self.xlimit = MAXITERS             
        if self.prepare_serial_axis_data() is not None:                  #Inicializa os valores iniciais   
            self.before =self.prepare_serial_axis_data()
        else:
            self.before=[0,0,0,0]
        self.mpl_real = MplCanvas()                                     #Objeto fig.canvas
        self.Kp=0
        self.Ki=0
        self.Kd=0

        # 从而创建开关按钮。
        redb = QtGui.QPushButton('change param', self)
        redb.setCheckable(True)
        redb.move(10, 10)

        # 将按钮点击信号与自定义方法关联。We use the 'clicked'
        # signal that operates with Boolean value.
        # （备注：不太清楚该如何翻译。）
        redb.clicked[bool].connect(self.changeParam)


        #Set's dos eixos     
        self.ax = self.mpl_real.fig.add_subplot(111)                    #Criação dos Eixos     
        self.ax.set_xlim(0,self.xlimit)
        self.ax.set_ylim(-MAXY,MAXY)
        self.ax.set_autoscale_on(False)
        self.ax.grid()
    
        # 创建水平的滑块
        self.sld_Kp = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld_Kp.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld_Kp.setGeometry(30, 40, 100, 30)
        self.sld_Kp.setMaximum(1500)
        # 将valueChanged信号与自定义方法关联。
        self.sld_Kp.valueChanged[int].connect(self.changeKp)
        
        self.label_Kp = QtGui.QLabel(self)
        self.label_Kp.setText(str(0))
        self.label_Kp.setGeometry(160, 40, 80, 30)
        
        # 创建水平的滑块
        self.sld_Ki = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld_Ki.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld_Ki.setGeometry(30, 40, 100, 30)
        self.sld_Ki.setMaximum(1000)
        # 将valueChanged信号与自定义方法关联。
        self.sld_Ki.valueChanged[int].connect(self.changeKi)
        
        self.label_Ki = QtGui.QLabel(self)
        self.label_Ki.setText(str(0))
        self.label_Ki.setGeometry(160, 40, 80, 30)

                # 创建水平的滑块
        self.sld_Kd = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.sld_Kd.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld_Kd.setGeometry(30, 40, 100, 30)
        self.sld_Kd.setMaximum(1000)
        # 将valueChanged信号与自定义方法关联。
        self.sld_Kd.valueChanged[int].connect(self.changeKd)
        
        self.label_Kd = QtGui.QLabel(self)
        self.label_Kd.setText(str(0))
        self.label_Kd.setGeometry(160, 40, 80, 30)
        
        self.ald_speed = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.ald_speed.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ald_speed.setGeometry(30, 40, 100, 30)
        self.ald_speed.setMaximum(4000)
        # 将valueChanged信号与自定义方法关联。
        self.ald_speed.valueChanged[int].connect(self.changeSpeed)
        
        self.label_speed = QtGui.QLabel(self)
        self.label_speed.setText(str(0))
        self.label_speed.setGeometry(160, 40, 80, 30)
        
        
        #Criação do QtLayout    
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.mpl_real)                                 #Adiciona o objeto mpl_real ao layout
        layout.addWidget(self.sld_Kp)
        layout.addWidget(self.label_Kp)
        layout.addWidget(self.sld_Ki)
        layout.addWidget(self.label_Ki)
        layout.addWidget(self.sld_Kd)
        layout.addWidget(self.label_Kd)
        layout.addWidget(self.ald_speed)
        layout.addWidget(self.label_speed)
        layout.addWidget(redb)
        
        self.setLayout(layout)                                          #Define o objeto layout como layout principal
        
        #Criação das Listas para a atualização Dinamica dos Plot's
        self.x, self.y, self.z,self.m = [], [], [], []
        self.l_x, = self.ax.plot([], self.x,'r', label = 'X %')
        self.l_y, = self.ax.plot([], self.y,'g', label = 'Y %')
        self.l_z, = self.ax.plot([], self.z,'b', label = 'Z %')
        self.l_m, = self.ax.plot([], self.z,'pink', label = 'M %')
        self.ax.legend()
        
        #Metodo de rendeziracao
        self.mpl_real.fig.canvas.draw()
        
        #Função de despacho de eventos por tempo do Qt
        self.cnt = 0
        self.timerEvent(None)   
        self.timer = self.startTimer(1)                                 #Definição da freq. inicial
        self.show()
    
    #Metodo para a aquisição dos dados seriais
    def prepare_serial_axis_data(self):             
        data = serial.SerialData()
        return data
    
    def changeKp(self,value):
        self.Kp=value
        self.label_Kp.setText(str(value))
      
    def changeSpeed(self,value):
        value=value-2000
        serial.sendSpeed(value)
        self.label_speed.setText(str(value))

    def changeKi(self,value):
        self.Ki=value
        self.label_Ki.setText(str(value))

    def changeKd(self,value):
        self.Kd=value
        self.label_Kd.setText(str(value))

    def changeParam(self,pressed):
        serial.sendParam(self.Kp,self.Ki,self.Kd)
                
    #Função que Captura os Eventos Gerados pelo timer
    def timerEvent(self, evento):
        
        result = self.prepare_serial_axis_data()
        if result is None:
            return
        self.x.append(result[0])                                        #Atualização das listas
        self.y.append(result[1])
        self.z.append(result[2])
        self.m.append(result[3]) 
        
        #Metodo de Atualização dos eixos do Plot
        self.l_x.set_data(range(len(self.x)), self.x)                   #Atualiza os eixos
        self.l_y.set_data(range(len(self.y)), self.y)
        self.l_z.set_data(range(len(self.z)), self.z)
        self.l_m.set_data(range(len(self.m)), self.m)
        
        #Renderização do plot
        self.mpl_real.fig.canvas.draw()
        
        #Comparação com o numero total de Pontos
        if self.cnt == MAXITERS:

            self.ax.clear()                                             #Limpa o eixo
            self.ax.set_xlim(0,self.xlimit)
            self.ax.set_ylim(-MAXY,MAXY)
            self.ax.set_autoscale_on(False)
            self.ax.grid()
            
            #Criação das Novas Listas
            self.x, self.y, self.z ,self.m= [], [], [], []
            self.l_x, = self.ax.plot([], self.x,'r', label = 'X %')
            self.l_y, = self.ax.plot([], self.y,'g', label = 'Y %')
            self.l_z, = self.ax.plot([], self.z,'b', label = 'Z %')
            self.l_m, = self.ax.plot([], self.z,'pink', label = 'M %')
            self.ax.legend()

    
            self.cnt = 0                                                #reinicia o contador
        
        else:
            self.cnt += 1


#Criação da App
app = QtGui.QApplication(sys.argv)
widget = CPUMonitor()
widget.show()
sys.exit(app.exec_())        
            
            
        
        
                
