from mendeleev import element
import molecule_set as ms
from vpython import *

class MolVisual:


    def clear(b, molecules):
        for molecule in molecules:
            if molecule.visible:
                molecule.visible = False


    def displaymolecule(m, molecules):
        molecules[m.index].visible = True


    def T(s, molecules):
        molecules[s.number].visible = True


    def __init__(self, width, height, resizable, visible, color, moleculenames):
        scene=canvas(width=width, height=height, resizable=resizable, visible=visible, background=vector(0.65,0.5,1))
        self.molecules=[]
        opt=True
        for x in moleculenames:
            self.molecules.append(ms.Molecule_Set( x + ".log", x + ".txt", opt))

        def B(b):
            for molecule in scene.objects:
                molecule.visible=False

        button(bind=B, text='Clear Molecule')
        scene.append_to_caption('\n\n')

        def M(m):
            atomlist=[]
            for molecule in scene.objects:
                molecule.visible=False
            for x in range(self.molecules[m.index].molecules):
                a = vector(self.molecules[m.index].standard_coordinates[x][0],
                           self.molecules[m.index].standard_coordinates[x][1],
                           self.molecules[m.index].standard_coordinates[x][2])
                el = element(int(self.molecules[m.index].atomic_numbers[x]))
                h = el.molcas_gv_color.lstrip('#')
                color = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
                colorvec = vector(color[0] / 200, color[1] / 200, color[2] / 200)
                atomlist.append(sphere(pos=a, radius=(el.vdw_radius / 200), color=colorvec, visible= False))
            mol = compound(atomlist)
            mol.visible=True

        menu(choices=moleculenames, bind=M)
        scene.append_to_caption('\n\n')


moleculenames=["benzene", "fosfina", "H2S2", "lih", "peroxide"]

scene=MolVisual(1100, 600, True, True, None, moleculenames)

