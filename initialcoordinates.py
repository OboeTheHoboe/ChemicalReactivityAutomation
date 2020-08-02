import os
from mendeleev import element
import molecule_set as ms
from vpython import *
import numpy as np

def energy_finder(gaussfile):
	file=open(gaussfile, "r")
	info=file.readlines()
	file.close()
	line=""

	for x in range(len(info)):
		if "HF=" in info[x]:
			line=info[x].strip() + info[x+1].strip()
			break

	energy=""
	count = line.find("HF=")+3
	while line[count] != "\\":
		energy=energy+line[count]
		count=count+1
	return energy

def charge_extractor(gaussfile, opt):
	charges=[]
	###def charge_extractor(outfile):
	file=open(gaussfile, "r")
	lines=file.readlines()
	file.close()
	for i in range(len(lines)):
		line=lines[i]
		if opt:
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
			if line.strip() == "Mulliken charges and spin densities:":
				i+=1
				line=lines[i+1]
				while line.strip()[0].isdigit():
					i+=1
					charges.append(line.strip())
					line=lines[i+1]
				print(charges)
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







energy=[]
freq=False
opt=False
name=input("Enter the avogadro .xyz file name: ")
file = open(name, "r")
info=file.readlines()
file.close()

name=os.path.splitext(name)[0]
info.pop(0)

gaussian_input=open(name+".com", "w+")
processors=input("Enter the number of processors for the desired calculations: ")
gaussian_input.write("%NProcShared="+ processors + "\n")
functional=input("Enter the functional for the calculations: ")
basis=input("Enter the basis set for the calculations: ")
gaussian_input.write("#t "+ functional + "/" + basis + " ")
print("Do you want to optimize the geometry first? [y/n]: ")

if input() == "y":
	gaussian_input.write("opt ")
	opt=True
###else:
	###gaussian_input.write("sp ")

print("Do you want to calculate the frequencies? [y/n]: ")
if input() == "y":
	gaussian_input.write("freq \n \n")
	freq=True
else:
	gaussian_input.write("\n \n")

title=input("Enter the job title (a title is always required): ")
gaussian_input.write(title+"\n \n")
charge=input("Enter the charge of the system: ")
multiplicity=input("Enter the multiplicity: ")
gaussian_input.write(charge + " " + multiplicity)

for i in range(len(info)):
	gaussian_input.write(info[i])

gaussian_input.write("\n")

###info=gaussian_input.readlines()

gaussian_input.close()

os.system("g16 < " + name + ".com" + " > " + name + ".log ")
###os.system("tail -f " +  name + ".log")

energy.append(float(energy_finder(name + ".log")))
charge_extractor(name + ".log", opt)

Set_1=ms.Molecule_Set(name + ".log", name + ".txt", opt)

gaussian_input_neg=open(name+"_1e+.com", "w+")
gaussian_input_neg.write("%NProcShared="+ processors + "\n")
gaussian_input_neg.write("#t "+ functional + "/" + basis + " sp \n \n")
gaussian_input_neg.write(title+" 1e+"+"\n \n")
gaussian_input_neg.write(str(int(charge)-1) + " " + str(int(multiplicity)+1) + "\n")
for i in range(Set_1.molecules):
	gaussian_input_neg.write( str(int(Set_1.atomic_numbers[i]))+ "     " + str(format(Set_1.standard_coordinates[i][0], "f")) + "  " + str(format(Set_1.standard_coordinates[i][1], "f")) + "     " + str(format(Set_1.standard_coordinates[i][2],"f")) + "\n")

gaussian_input_neg.write("\n")
gaussian_input_neg.close()

os.system("g16 < " + name+"_1e+.com" + " > " + name + "_1e+.log ")
###os.system("tail -f " + name + "_1e+.log ")

energy.append(float(energy_finder(name + "_1e+.log")))
charge_extractor(name + "_1e+.log", False)


gaussian_input_pos=open(name+"_1e-.com", "w+")
gaussian_input_pos.write("%NProcShared="+ processors + "\n")
gaussian_input_pos.write("#t "+ functional + "/" + basis + " sp \n \n")
gaussian_input_pos.write(title+" 1e-"+"\n \n")
gaussian_input_pos.write(str(int(charge)+1) + " " + str(int(multiplicity)+1) + "\n")
for i in range(Set_1.molecules):
	gaussian_input_pos.write( str(int(Set_1.atomic_numbers[i]))+ "     " + str(format(Set_1.standard_coordinates[i][0], "f")) + "  " + str(format(Set_1.standard_coordinates[i][1], "f")) + "     " + str(format(Set_1.standard_coordinates[i][2],"f")) + "\n")

gaussian_input_pos.write("\n")
gaussian_input_pos.close()

os.system("g16 < " + name+"_1e-.com" + " > " + name + "_1e-.log ")
###os.system("tail -f " + name + "_1e-.log ")

energy.append(float(energy_finder(name + "_1e-.log")))
charge_extractor(name + "_1e-.log", False)


if freq:
	###freq_tester(name + ".log" , name + "freqs.txt")
	print("done")


EA=energy[0]-energy[1]
IE=energy[2]-energy[0]
chemical_potential=-(IE+EA)/2
hardness=IE-EA
electrophilicity=chemical_potential**2 / hardness



print("\n \n Electron Affinity: " + str(EA)+ " A.U.")
print("\n Ionization Energy: " + str(IE)+ " A.U." + "\n\n")
print("Chemical Potential: " + str(chemical_potential) + " A.U.")
print("Hardness: " + str(hardness) + " A.U.")
print("Electrophilicity: " + str(electrophilicity) + " A.U.\n\n")


###Set_1=ms.Molecule_Set(name + ".log", name + ".txt")
print("Center of mass coordinates: ")
for i in range(3):
	if i == 0:
			print("X: " + str(Set_1.center_of_mass[i]))
	if i == 1:
		print("Y: " + str(Set_1.center_of_mass[i]))
	if i == 2:
		print("Z: " + str(Set_1.center_of_mass[i]))
if input("Do you want to display the 3D molecule? [y/n]: ") == "y":
	atomList = []
	for x in range(Set_1.molecules):

		a=vector(Set_1.standard_coordinates[x][0],Set_1.standard_coordinates[x][1], Set_1.standard_coordinates[x][2])
		###print("Position vector: ",a)
		el=element(int(Set_1.atomic_numbers[x]))
		###print("Van der Waals radius: ", el.vdw_radius/100)
		###https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
		h = el.molcas_gv_color.lstrip('#')
		color=tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
		colorvec=vector(color[0]/200, color[1]/200, color[2]/200)
		atomList.append(sphere(pos=a, radius=(el.vdw_radius/200),color=colorvec))





