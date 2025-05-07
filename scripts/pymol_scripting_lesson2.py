from pymol import cmd
import os
import sys

#https://pymol.org/dokuwiki/doku.php?id=setting:ray
def ray_trace():

    cmd.set('ray_trace_mode', 2) #Black and white
    cmd.set('ray_shadows', 0) #Remove shadows
    cmd.set('fog', 0) #Remove fog
    cmd.set('ray_trace_gain', 20) #Create a dark outline
    cmd.set('ray_trace_slope_factor', 5) #Remove some shadow constrast

def quality(anti_alias: int=4):
    cmd.set('antialias', anti_alias)#Set the anti-aliasing level to highest available

def protein_figure(protein:str, resi_list:list):
    """
    Arguments: Protein object and list of selected residues

    """
    residue_string = "+".join(sorted(str(r) for r in resi_list))
    min_resi = max(1, resi_list[0]-2)
    max_resi = resi_list[-1] + 2

    padded_resi = list(range(min_resi, max_resi + 1))
    expanded_residue_string = "+".join(sorted(str(r) for r in padded_resi))
    
    cmd.hide('everything')
    cmd.show('cartoon', f'{protein} and not resi {residue_string}')
    cmd.create('hide', f'{protein} and resi {expanded_residue_string}')
    cmd.set('ray_opaque_background', 1)
    cmd.set('bg_rgb', [1,1,1])
    cmd.png(f'{protein}_4', width=800, height=600, dpi=300, ray=1)

def get_selection_residues(protein:str, selection_name:str):
    """
    Expands the selection to hide and creates an object that overlaps
    """
    selection = cmd.get_model(selection_name)
    residue_set = set()
    for atom in selection.atom:
        residue_set.add(int(atom.resi))
    resi_list = sorted(residue_set)
    
    print(f"resi {resi_list}")
    
    return resi_list

def select_objects(protein:str, active_site:list):
    """
    Checks that the objects can be found in Pymol. 
    Exits if criteria are not met.
    Input: Protein string and active_site list
    Returns: Protein string and active site list
    """
    objects = cmd.get_object_list()
    
    #check active site objects
    if set(active_site).issubset(objects):
        print(f"Found active site molecule objects: {active_site}")

    else:
        missing = set(active_site) - set(objects)
        print(f"Unable to find all active site molecules {missing}, exiting")
        sys.exit()

    #Check protein object
    if protein in objects:
        print (f"Found protein molecule object: {protein}")
        return protein, active_site
    
    else:
        print (f"Protein molecule object {protein} not found, exiting")
        sys.exit()


# ==== Main Execution ====
#Pymol recieves all arguments as a string so need to parse it.
def run_selection(arg_string:str, _self=None):
    """
    Checks the selection
    Input: string of protein, ligand, and residues (if entered) 
    Returns: Protein String, list of active site. Ligand and active site residues
    """
    args = arg_string.split()
    if len(args) < 2 or len(args) > 3:
        print("Usage: run_selection protein_name ligand residues ....")
        return
    protein = args[0]
    active_sites = args[1:]
    print(f"Looking for {protein} and {active_sites}", flush=True)
    protein, active_site = select_objects(protein, active_sites)
    residue_list = get_selection_residues(protein, selection_name='sele')
   
cmd.extend("run_selection", run_selection)
cmd.extend("get_selection_residues", get_selection_residues)
cmd.extend("protein_figure", protein_figure)
