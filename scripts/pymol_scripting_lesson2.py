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

def select_objects(active_site: list, protein: str):
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
        return active_site, protein
    
    else:
        print (f"Protein molecule object {protein} not found, exiting")
        sys.exit()

# ==== Main Execution ====

def run_selection():
    active_site = ["1EMA_active_site_residues", "1EMA_organics"]
    protein = "1EMA_A"
    print(f'Looking for {active_site} and {protein}', flush=True)
    select_objects(active_site, protein)
    
cmd.extend("run_selection", run_selection)