import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from mpldatacursor import datacursor



med = pd.read_excel("med2graph.xlsx")
#se puede armar un vector que represente a las rectas de cargaaaaaaaaaa



plt.figure(1) #GRAFICO DE MAGNITUD Zin (E1 y E2 superpuestos)
plt.plot(med["Io"], med["Vo"], label='Caracteristica de Salida')
plt.plot()
plt.title("Característica de Salida")

plt.xlabel("Io (A)")
plt.ylabel("Vo (V)")
plt.grid(True)
plt.xticks()
plt.yticks()
plt.legend(loc = 'lower right')
datacursor(formatter="Io:{x:.2f} A\n Vo:{y:.2f} V".format, display='multiple', draggable=True)
plt.show()