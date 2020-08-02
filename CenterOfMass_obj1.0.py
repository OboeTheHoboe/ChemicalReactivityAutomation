###Utiliza la clase que cree para hacer el calculo del centro de masa
###Autor: Jorge Garcia Ponce DOMINGO 09 DE JUNIO DE 2019

from mendeleev import element
import molecule_set as ms
from vpython import *

def main():

	###Set=ms.Molecule_Set("/Users/jorge/Desktop/reactivos2.log", "/Users/jorge/Desktop/coordinates.xyz")
	Set_1=ms.Molecule_Set(input("Enter the Gaussian file path:"), input("Enter the desired path for the coordinates file:"))
	print("Center of mass coordinates: ")
	for i in range(3):
		if i == 0:
				print("X: " + str(Set_1.center_of_mass[i]))
		if i == 1:
			print("Y: " + str(Set_1.center_of_mass[i]))
		if i == 2:
			print("Z: " + str(Set_1.center_of_mass[i]))

	for i in range(Set_1.molecules):
		 print( str(int(Set_1.atomic_numbers[i]))+ "     " + str(Set_1.standard_coordinates[i][0]) + "  " + str(Set_1.standard_coordinates[i][1]) + "     " + str(Set_1.standard_coordinates[i][2]))




	coordinates = open(Set_1.outf+str(i)+".com", "w+") ### crea un archivo de nombre coordinates con permisos para escribir la info extraida 
	coordinates.write("#t hf/6-31g sp" + "\n")
	coordinates.write("\n")
	coordinates.write("test gaussian input" + "\n")
	coordinates.write("\n")
	coordinates.write("0 1" + "\n")

	for i in range(Set_1.molecules):
		coordinates.write( str(int(Set_1.atomic_numbers[i]))+ "     " + str(Set_1.standard_coordinates[i][0]) + "  " + str(Set_1.standard_coordinates[i][1]) + "     " + str(Set_1.standard_coordinates[i][2]) + "\n")

	coordinates.write("\n")
	coordinates.close()### cierra el archivo




	atomList = []
	for x in range(Set_1.molecules):

		a=vector(Set_1.standard_coordinates[x][0],Set_1.standard_coordinates[x][1], Set_1.standard_coordinates[x][2])
		print("Position vector: ",a)
		el=element(int(Set_1.atomic_numbers[x]))
		print("Van der Waals radius: ", el.vdw_radius/100)
		###https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
		h = el.molcas_gv_color.lstrip('#')
		color=tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
		colorvec=vector(color[0]/200, color[1]/200, color[2]/200)
		atomList.append(sphere(pos=a, radius=(el.vdw_radius/250),color=colorvec))


main()
