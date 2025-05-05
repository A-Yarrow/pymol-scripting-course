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

def select_objects(protein:str, active_site: list):
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
#Pymol recieves all arguments as a string so need to parse it.
def run_selection(arg_string, _self=None):
    args = arg_string.split()
    if len(args) < 2:
        print("Usage: run_selection protein_name active_site1 active_site2 ...")
        return
    protein = args[0]
    active_sites = args[1:]
    print(f"Looking for {protein} and {active_sites}", flush=True)
    select_objects(protein, active_sites)

cmd.extend("run_selection", run_selection)