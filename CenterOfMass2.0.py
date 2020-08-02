###Calculadora del centro de masa en 3 dimensiones
###Escrito por: Jorge García Ponce el VIERNES 07 DE JUNIO DEL 2019

import numpy as np
from mendeleev import element

def extract_info():

	file = open("/Users/jorgegarcia/Desktop/chemicalreactivity/coordinates.xyz", "r")### abre el archivon que escribe en el otro programa (lo cambiare en el futuro pero para probra archivos aqui lo cambias)
	lines=file.readlines()
	###line = ""
	file.close()
	strval,data=list(), list()

	for i in lines:
		if i[0].isdigit():
			strval.append(i.strip())
	###print(strval)

	Ma=len(strval)
	###print(Ma)
	coord = np.zeros((Ma, 3))
	mass = np.zeros(Ma)
	contador_coord=0
	contador_atomo=0

	for k in range(len(strval)):
		val = strval[k]+ " " 
		###print(len(val))
		for j in range(len(val)):
			stringvalues=""
			if val[j] == " ":
			
				while True:

					stringvalues=stringvalues+val[j]
					stringvalues=stringvalues.strip()
					if j < len(val)-1:
						j= j+1
					if val[j] == " ":
						if stringvalues != "" and  stringvalues != "0":

							if contador_coord == 0:
								mass[contador_atomo]=float(stringvalues)

							if contador_coord>0:
								coord[contador_atomo][contador_coord-1]=float(stringvalues)

							contador_coord = contador_coord + 1

							if contador_coord > 3:
								contador_coord = contador_coord -4
								contador_atomo = contador_atomo + 1

							data.append(stringvalues)
						break
	return Ma, mass, coord


def main():
	Ma = 1
	coord = np.zeros((Ma, 3))
	mass = np.zeros(Ma)
	centervect=np.zeros(3)
	mtot=0
	el=element(1)

	"""mass[0]=1
	mass[1]=1
	mass[2]=1
	coord[0]=[3,5,0]
	coord[1]=[-1,-1,0]
	coord[2]=[4,4,0]"""

	Ma, mass, coord = extract_info()
	print("the following coordinates were extracted from file: /Users/jorgegarcia/Desktop/chemicalreactivity/coordinates.xyz"+"\n", coord)
	###input()

	for n in range(len(mass)):
		el=element(int(mass[n]))
		mass[n]=el.mass

	###print(mass)

	###print(coord, mass)
	for i in range(Ma):###  Ma es el length de mass y de los arrays dentro de coord
		for j in range(3):
			coord[i][j]= mass[i] * coord[i][j]		
	###print(coord)

	for j in range(Ma):###  igualo l a j para usar la resta como un contador indirecto
		mtot += mass[j]###  calculo masa total
		l = j
		for k in range(3):
			centervect[l-j] += coord[j][k]
			l += 1 ###  aumento l y así sirve de contador, pues l-j será 0 al principio y le sumo a 0 un 1 tres veces
	###print(centervect, mtot)

	print("Center of mass coordinates: ")
	for i in range(3):
		centervect[i]=centervect[i]/mtot
		if i == 0:
			print("X: " + str(centervect[i]))
		if i == 1:
			print("Y: " + str(centervect[i]))
		if i == 2:
			print("Z: " + str(centervect[i]))
	###print(centervect)

main()



