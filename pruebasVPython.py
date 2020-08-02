import numpy as np
from mendeleev import element

### En esta clase junté los scripts que habia hechos para poder instanciar objetos y usarlos de manera mas eficiente. Los metodos son los scripts que habia hecho
class Molecule_Set:


	@classmethod

	def molecular_information_extractor(self, sourcef, outf, opt):
		file = open(sourcef, "r")### Aquí va el archivo de gaussian que se quiera escanear
		lines=file.readlines()### se guarda todo el texto linea por linea en una lista de strings
		file.close()
		info=list() ### lista auxiliar para hacer las 2 busquedas y extraer solo la info importante
		count=0

		if opt:
			for k in range(len(lines)):### empieza a leer todo el texto linea por linea
				line = lines[k]### hace que la linea cambie
				if line.strip()== "-- Stationary point found.":### le doy el string que identifica la info que busco para empezar a extraer los datos
					while line.strip() != "Standard orientation:":
						k = k+1
						line = lines[k]
					while count < 3:### le doy el string con el cual termiar la busqueda de los datos que quiero
						if line.strip()[0]=="-":
							count=count+1

						info.append(line.strip())
						k = k+1### aumento el contador en 1 para seguir buscando
						line = lines[k] ### cambia a la siguiente linea del texto
					break
		else:
			for k in range(len(lines)):### empieza a leer todo el texto linea por linea
				line = lines[k]### hace que la linea cambie
			###if line.strip()== "-- Stationary point found.":### le doy el string que identifica la info que busco para empezar a extraer los datos
				while line.strip() != "Standard orientation:":
					k = k+1
					line = lines[k]
				while count < 3:### le doy el string con el cual termiar la busqueda de los datos que quiero
					if line.strip()[0]=="-":
						count=count+1

					info.append(line.strip())
					k = k+1### aumento el contador en 1 para seguir buscando
					line = lines[k] ### cambia a la siguiente linea del texto
				break

		coordinates = open(outf, "w+") ### crea un archivo de nombre coordinates con permisos para escribir la info extraida 
		for x in info:
			coordinates.write(x + "\n")### escribe la info en el archivo creado
		coordinates.close()### cierra el archivo


	@classmethod

	def coordinates_extractor(self, outfile):

		file = open(outfile, "r")### abre el archivon que escribe en el otro programa (lo cambiare en el futuro pero para probra archivos aqui lo cambias)
		lines=file.readlines()
		file.close()
		strval,data=list(), list()

		for i in lines:
			if i[0].isdigit():
				strval.append(i.strip())

		molecules=len(strval)
		standard_coordinates = np.zeros((molecules, 3))
		atomic_numbers = np.zeros(molecules)
		molecular_masses = np.zeros(molecules)
		total_mass=0
		atoms_coordinates_count=0
		atom_count=0

		for k in range(len(strval)):
			val = strval[k]+ " " 
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

								if atoms_coordinates_count == 0:
									atomic_numbers[atom_count]=float(stringvalues)

								if atoms_coordinates_count>0:
									standard_coordinates[atom_count][atoms_coordinates_count-1]=float(stringvalues)

								atoms_coordinates_count = atoms_coordinates_count + 1

								if atoms_coordinates_count > 3:
									atoms_coordinates_count = atoms_coordinates_count -4
									atom_count = atom_count + 1

							break
		for n in range(molecules):
				el=element(int(atomic_numbers[n]))
				molecular_masses[n]=el.mass
				total_mass += molecular_masses[n]
		return molecules, atomic_numbers, molecular_masses, total_mass, standard_coordinates


	@classmethod

	def center_of_mass_calculator(self, molecules, molecular_masses, total_mass, standard_coordinates_):

		__standard_coordinates = np.zeros((molecules, 3))
		center_of_mass=np.zeros(3)
		for i in range(molecules):###  Ma es el length de mass y de los arrays dentro de coord
			for j in range(3):
				__standard_coordinates[i][j]= molecular_masses[i] * standard_coordinates_[i][j]		
				###print(coord)
		for j in range(molecules):###  igualo l a j para usar la resta como un contador indirecto
			total_mass += molecular_masses[j]###  calculo masa total
			l = j
			for k in range(3):
				center_of_mass[l-j] += __standard_coordinates[j][k]
				l += 1 ###  aumento l y así sirve de contador, pues l-j será 0 al principio y le sumo a 0 un 1 tres veces
		###print(centervect, mtot)
		return center_of_mass


	def __init__(self, sourcefile, outfile, optn):

		self.sourcef = sourcefile
		self.outf = outfile
		self.opt = optn
		self.molecular_information_extractor(self.sourcef, self.outf, self.opt)
		self.molecules, self.atomic_numbers, self.molecular_masses, self.total_mass, self.standard_coordinates = self.coordinates_extractor(self.outf)
		self.center_of_mass=self.center_of_mass_calculator(self.molecules, self.molecular_masses, self.total_mass, self.standard_coordinates)

	
	def bonding_criteria(self, center_atom, neighbour_atom):
		self.standard_coordinates[center_atom]




charges=[]
###def charge_extractor(outfile):
file=open(input(), "r")
lines=file.readlines()
file.close()
for i in range(len(lines)):
	line=lines[i]
	if True:
		if line.strip()== "-- Stationary point found.":### le doy el string que identifica la info que busco para empezar a extraer los datos
			while line.strip() != "Mulliken charges:":
				i = i+1
				line = lines[i]
			if line.strip() == "Mulliken charges:":
				i+=1
				line=lines[i+1]
				while line.strip()[0].isdigit():
					i+=1
					charges.append(line.strip())
					line=lines[i+1]
				break
	else:
		if line.strip() == "Mulliken charges:":
			i+=1
			line=lines[i+1]
			while line.strip()[0].isdigit():
				i+=1
				charges.append(line.strip())
				line=lines[i+1]
			break


###print(charges)
atomic_charges = np.zeros(len(charges))
count=0
atom_count=0

for k in range(len(charges)):
			val = charges[k]+ " " 
			for j in range(len(val)):
				stringvalues=""
				if val[j] == " ":
			
					while True:

						stringvalues=stringvalues+val[j]
						stringvalues=stringvalues.strip()
						if j < len(val)-1:
							j= j+1
						if val[j] == " ":
							if stringvalues != "":
								if count==1:
									atomic_charges[atom_count]=float(stringvalues)

								if count > 1:
									count = count -2
									atom_count = atom_count + 1
								count+=1

							break
print(atomic_charges)




