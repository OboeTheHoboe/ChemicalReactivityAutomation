import os
from mendeleev import element
import molecule_set as ms
from vpython import *
import numpy as np
import molvis as mv


def energy_extractor(gaussfile):
	file=open(gaussfile, "r")
	lines=file.readlines()
	file.close()
	senergy=""
	for l in lines:
		l=l.strip()
		if l[0:5] == "Total" and l[6:12] == "Energy":
			count=len(l)-1
			while l[count] != " ":
				senergy=l[count]+senergy
				count-=1
	energy=float(senergy)
	print(energy)
	return energy


def input_creator(name, processors, functional, basis, title, charge0, mult0, charge1, mult1, charge2, mult2, opt, freq):
	file = open(name, "r")
	info=file.readlines()
	file.close()
	name=os.path.splitext(name)[0]
	info.pop(0)
	gaussian_input=open(name+".com", "w+")
	gaussian_input.write("%NProcShared="+ processors + "\n")
	gaussian_input.write("%Chk="+ name + ".chk \n")
	gaussian_input.write("#t "+ functional + "/" + basis + " ")

	if opt == True:
		gaussian_input.write("opt ")

	if freq == True:
		gaussian_input.write("freq \n \n")

	else:
		gaussian_input.write("\n \n")

	gaussian_input.write(title+"\n \n")
	gaussian_input.write(str(charge0) + " " + str(mult0))

	for i in range(len(info)):
		gaussian_input.write(info[i])

	gaussian_input.write("\n\n")
	gaussian_input.write("--Link1--\n")
	gaussian_input.write("%OldChk="+ name + ".chk \n")
	gaussian_input.write("%Chk="+ name + "_1e+.chk \n")
	gaussian_input.write("#t "+ functional + "/" + basis + " geom=check guess=read \n\n")
	gaussian_input.write(title+" 1e+"+"\n \n")
	gaussian_input.write(str(charge1) + " " + str(mult1))
	gaussian_input.write("\n\n")
	gaussian_input.write("--Link1--\n")
	gaussian_input.write("%OldChk="+ name + ".chk \n")
	gaussian_input.write("%Chk="+ name + "_1e-.chk \n")
	gaussian_input.write("#t "+ functional + "/" + basis + " geom=check guess=read \n\n")
	gaussian_input.write(title+" 1e-"+"\n \n")
	gaussian_input.write(str(charge2) + " " + str(mult2) + "\n\n")
	gaussian_input.close()


def print_data(title, IE, EA, chemical_potential, hardness, electrophilicity, elecprocess, nucprocess, partitioning):
	convf=27.2116
	print(title + ": \n\n")
	print("\n\n Ionization Energy: " + str(round(IE, 4))+ " A.U.")
	print(" Ionization Energy: " + str(round(IE*convf, 4))+ " eV")
	print("\n\n Electron Affinity: " + str(round(EA,4))+ " A.U.")
	print(" Electron Affinity: " + str(round(EA*convf,4))+ " eV \n\n")
	print(" Chemical Potential: " + str(round(chemical_potential, 4)) + " A.U.")
	print(" Chemical Potential: " + str(round(chemical_potential*convf, 4)) + " eV\n\n")
	print(" Hardness: " + str(round(hardness, 4)) + " A.U.")
	print(" Hardness: " + str(round(hardness*convf, 4)) + " eV\n\n")
	print(" Electrophilicity: " + str(round(electrophilicity, 4)) + " A.U.")
	print(" Electrophilicity: " + str(round(electrophilicity*convf, 4)) + " eV\n\n")
	if elecprocess != None:
		print("\n\n Electrophilic process on "+ title +": " + str(elecprocess))
	if nucprocess != None:
		print(" Nucleophilic process on "+ title +": " + str(nucprocess))
	if partitioning != None:
		print(" Charge partitioning on "+ title +": " + str(nucprocess)+"\n\n")

"""def M(m):
    print(m.selected, m.index)


def molecule_plotter(Molecules):

	atomList = []
	for x in range(Molecules[m].molecules):

		a=vector(Molecules[m].standard_coordinates[x][0],Molecules[m].standard_coordinates[x][1], Molecules[m].standard_coordinates[x][2])
		###print("Position vector: ",a)
		el=element(int(Molecules[m].atomic_numbers[x]))
		###print("Van der Waals radius: ", el.vdw_radius/100)
		###https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
		h = el.molcas_gv_color.lstrip('#')
		color=tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
		colorvec=vector(color[0]/200, color[1]/200, color[2]/200)
		atomList.append(sphere(pos=a, radius=(el.vdw_radius/200),color=colorvec))"""
	




print("\n\n DO YOU ALREADY HAVE A SUBSTRATE OR SHALL IT´S CALCULATION BE PERFORMED?")
substrate=input(" Write 1 if it shall be performed or 0 if it has already been done: ")
print("\n\n")
k = True
energy=[]
Moleculesnames=[]
Molecules=[]
if int(substrate) == 0:
	chk0=input(" Enter the name of the neutral molecule´s checkpoint file: ")
	chk0=os.path.splitext(chk0)[0]
	chka=input(" Enter the name of the anion´s checkpoint file: ")
	chka=os.path.splitext(chka)[0]
	chkc=input(" Enter the name of the cations´s checkpoint file: ")
	chkc=os.path.splitext(chkc)[0]
	os.system("formchk " + chk0 + ".chk " +  chk0 + ".fchk")
	os.system("formchk " + chka + ".chk " +  chka + ".fchk")
	os.system("formchk " + chkc + ".chk " +  chkc + ".fchk")
	energy.append(energy_extractor(chk0 + ".fchk"))
	energy.append(energy_extractor(chka + ".fchk"))
	energy.append(energy_extractor(chkc + ".fchk"))

	energy1=np.array(energy)
	EA1=energy1[0]-energy1[1]
	IE1=energy1[2]-energy1[0]
	chemical_potential1=-(IE1+EA1)/2
	hardness1=IE1-EA1
	electrophilicity1=chemical_potential1**2 / hardness1

	print_data("SUBSTRATE", IE1, EA1, chemical_potential1, hardness1, electrophilicity1, None, None, None)

	k = False


for x in range(int(input(" Enter the number of molecules counting the substrate: "))):
	del energy[:]
	freq=False
	opt=False

	if x==0 and k:
		name0=input(" Enter the avogadro .xyz file name for the Substrate: ")
		name=name0
	else:
		name1=input(" Enter the avogadro .xyz file name for the Molecule: ")
		name=name1

	Moleculesnames.append(name)
	processors=input(" Enter the number of processors for the desired calculations: ")
	functional=input(" Enter the functional for the calculations: ")
	basis=input(" Enter the basis set for the calculations: ")
	basis=  basis + " " + input(" If any, write additional keywords here: ")

	if input(" Do you want to optimize the geometry first? [y/n]: ") == "y":
		opt=True

	if input(" Do you want to calculate the frequencies? [y/n]: ") == "y":
		freq=True

	title=input(" Enter the job title (a title is always required): ")
	charge0=int(input(" Enter the charge of the system: "))
	mult0=int(input(" Enter the multiplicity: "))
	charge1=int(input(" Enter the charge of the anion: "))
	mult1=int(input(" Enter the anion: "))
	charge2=int(input(" Enter the charge of the cation: "))
	mult2=int(input(" Enter the cation: "))

	input_creator(name, processors, functional, basis, title, charge0, mult0, charge1, mult1, charge2, mult2, opt, freq)

	name=os.path.splitext(name)[0]
	os.system("g16 < " + name + ".com" + " > " + name + ".log ")
	os.system("formchk " + name + ".chk " +  name + ".fchk")
	os.system("formchk " + name + "_1e+.chk " +  name + "_1e+.fchk")
	os.system("formchk " + name + "_1e-.chk " +  name + "_1e-.fchk")

	energy.append(energy_extractor(name + ".fchk"))
	energy.append(energy_extractor(name + "_1e+.fchk"))
	energy.append(energy_extractor(name + "_1e-.fchk"))
	Molecules.append(ms.Molecule_Set(name + ".log", name + ".txt", opt))

	if x == 0 and k:
		energy1=np.array(energy)
		EA1=energy1[0]-energy1[1]
		IE1=energy1[2]-energy1[0]
		chemical_potential1=-(IE1+EA1)/2
		hardness1=IE1-EA1
		electrophilicity1=chemical_potential1**2 / hardness1
		print_data("SUBSTRATE", IE1, EA1, chemical_potential1, hardness1, electrophilicity1, None, None, None)

	else:

		energy2=np.array(energy)
		EA2=energy2[0]-energy2[1]
		IE2=energy2[2]-energy2[0]
		chemical_potential2=-(IE2+EA2)/2
		hardness2=IE2-EA2
		electrophilicity2=chemical_potential2**2 / hardness2
		elecprocess2= - (EA1-IE2)/(2*(hardness2+hardness1))
		nucprocess2= (EA2-IE1)/(2*(hardness2+hardness1))
		partitioning2 = elecprocess2 + nucprocess2
		print_data(name, IE2, EA2, chemical_potential2, hardness2, electrophilicity2, elecprocess2, nucprocess2, partitioning2)

		if input(" Do you want to visualize the molecules? [y/n]: ") == "y":

			scene = mv.MolVisual(1100, 600, True, True, None, Moleculesnames)


"""if input(" Do you want to visualize the molecules? [y/n]: ")=="y":

	while True:
		print(" Select which one you´d like to see:")
		for x in range(len(Moleculesnames)):
			print(str(x) + ".- " + Moleculesnames[x])
		mol=int(input("Molecule: "))
		scene=canvas(title=Moleculesnames[x], caption=Moleculesnames[x], width=1200, height=1200, resizable=True, visible=True)
		for i in range(3):
			if i == 0:
				print("X: " + str(Molecules[mol].center_of_mass[i]))
			if i == 1:
				print("Y: " + str(Molecules[mol].center_of_mass[i]))
			if i == 2:
				print("Z: " + str(Molecules[mol].center_of_mass[i]))

		menu( choices=Moleculesnames, bind=molecule_plotter(Molecules))
		scene.append_to_caption('\n\n')



		atomList = []
		for x in range(Molecules[mol].molecules):

			a=vector(Molecules[mol].standard_coordinates[x][0],Molecules[mol].standard_coordinates[x][1], Molecules[mol].standard_coordinates[x][2])
			###print("Position vector: ",a)
			el=element(int(Molecules[mol].atomic_numbers[x]))
			###print("Van der Waals radius: ", el.vdw_radius/100)
			###https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
			h = el.molcas_gv_color.lstrip('#')
			color=tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
			colorvec=vector(color[0]/200, color[1]/200, color[2]/200)
			atomList.append(sphere(pos=a, radius=(el.vdw_radius/200),color=colorvec))

		if input(" Do you want to visualize the molecules? [y/n]: ")=="n":
			break"""



