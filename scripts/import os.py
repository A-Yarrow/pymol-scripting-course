import os
import sys
from pymol import cmd, util

# ==== Logging Setup ====
#Uncomment if you want to troubleshoot with logging
"""
log_path = os.path.expanduser("~/tmp/pymol_custom_log.txt")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logfile = open(log_path, "w")
sys.stdout = logfile
sys.stderr = logfile
"""
def pymol_display_settings():
    """
    Function to set up custom PyMOL settings.
    This function is called when the script is executed.
    """
    print("Loading custom PyMOL settings...", flush=True)

    # ==== PyMOL Settings ====
    cmd.set('use_shaders', 0) # Disable shaders
    cmd.set('cartoon_gap_cutoff', 0) # Don't show dashes in cartoon)
    cmd.set('seq_view', 1) #Turn on the sequence view
    cmd.set('valence', 0) #Don't explicitly show double bonds
    cmd.set('stick_radius', 0.3) #Set stick radius to 0.3
    cmd.set('stick_ball', 'on')
    cmd.set('stick_ball_ratio', 1.7)
    cmd.set('bg_rgb', 'light_grey')
    cmd.set('cartoon_fancy_helices', 1)
    cmd.set('cartoon_side_chain_helper', 1)
    cmd.set('label_font_id', 7)
    cmd.set('label_size', 14)
    cmd.set('label_color', 'black')
    cmd.set('ambient', 0.4) #Make visuals lighter
    cmd.set('two_sided_lighting', 1)
    cmd.set('depth_cue', 0)
    cmd.set('orthoscopic', 70) #Set orthographic projection

#https://www.blopig.com/blog/2021/01/making-pretty-pictures-with-pymol/
def pymol_render_settings():
    cmd.set('ray_trace_mode', 0)
    cmd.set('ray_shadows', 1)
    cmd.set('ray_trace_gain', 0.1)
    cmd.set('antialias', 2)

# Set up Custom Color Palette
# https://color.adobe.com/color-name_LG-color-theme-19646985/
# https://pmc.ncbi.nlm.nih.gov/articles/PMC9377702/#j_jib-2022-0016_fig_001
def pymol_colors():
    cmd.set_color('light_grey', [211/255.0, 211/255.0, 211/255.0])
    cmd.set_color('LG1', [247/255.0, 207/255.0, 150/255.0])
    cmd.set_color('LG2', [226/255.0, 176/255.0, 106/255.0])
    cmd.set_color('LG3', [198/255.0, 187/255.0, 201/255.0])
    cmd.set_color('LG4', [36/255.0,  160/255.0, 152/255.0])
    cmd.set_color('LG5', [91/255.0,  211/255.0, 203/255.0])

#Custom color protein chains
def get_protein_chains(obj_name):
    """
    Function to get the protein chains from a given object name.
    Args:
        obj_name (str): Name of the object.
    Returns:
        list: List of protein chain IDs.
    """
    
    selection = f"{obj_name} and polymer.protein"
    chains = cmd.get_chains(selection)
    print("Chains in selection:", chains, flush=True)
    return chains
# Get the protein chains from the selection
def color_protein_chains(obj_name):
    """
    Function to color protein chains in a given object.
    Args:
        obj_name (str): Name of the object.
    """
    print("Coloring protein chains for object:", obj_name, flush=True)
    chains = get_protein_chains(obj_name)
    
    pymol_colors = [
        "red", "green", "blue", "yellow", "cyan", "magenta",
        "orange", "slate", "teal", "violet", "salmon", "lime",
        "pink", "marine", "wheat", "white", "grey", "black"
    ]
    for i, chain in enumerate(chains):
        if len(chains) < 5:
            color = f"LG{i+1}"
        else:
            color = pymol_colors[(i - 5) % len(pymol_colors)]
        
        cmd.create(name=f"{obj_name}_{chain}", selection=f"{obj_name} and polymer.protein and chain {chain}") # Create a new object for each chain
        cmd.show(representation="cartoon", selection=f"{obj_name}_{chain}") # Show the cartoon representation of the chain
        cmd.set("cartoon_color", color, f"{obj_name}_{chain}") #Set the color of eac chain
        cmd.hide("everything", f"{obj_name}")  # Hide everything from the original object
        print(f"Colored chain {chain} with color {color}", flush=True) 

# ==== Callback ====
def after_load_callback(object_names):
    """
    Callback function to be executed after a PDB file is loaded.
    This function can be used to apply specific settings or modifications
    to the loaded structure.
    Args:
        object_names (list): List of names of the loaded objects.
    """
    for name in object_names: 
        cmd.hide("everything", f"{name} and resname HOH")  # Hide water
        cmd.hide("everything", f"{name} and organic")  # Hide organics
        cmd.hide("everything", f"{name} and inorganic")
        cmd.create(name=f"{name}_active_site_water", selection="resname HOH within 3.5 of organic") # Create a new object for active site water
        cmd.show(representation="spheres", selection=f"{name}_active_site_water")  # Show selected water
        cmd.create(name=f"{name}_inorganics", selection="inorganic within 3.5 of organic") # Create a new object for inorganics
        cmd.show(representation="spheres", selection=f"{name}_inorganics")  # Show selected inorganics
        cmd.color("LG3", f"{name}_inorganics")  # Color inorganics
        cmd.show(representation="spheres", selection=f"{name}_inorganics")  # Show active site water
        cmd.create(name=f"{name}_organics", selection=f"{name} and organic") # Create a new object for organics
        cmd.show(representation="spheres", selection=f"{name}_organics")
        cmd.color("White", f"{name}_organics")  # Color organics white to stand out.
        cmd.color("LG1", f"{name} and polymer.protein")  # Color protein molecule
        cmd.create(name=f"{name}_active_site_residues", selection=f"byres ({name} and polymer.protein or name CA within 3.5 of {name}_organics)") # Select residues near to organic
        util.cbay(f"{name}_active_site_residues")  # Color active site residues
        cmd.show(representation="sticks", selection=f"{name}_active_site_residues and not name n+c+o")  # Show active site residues
        cmd.hide(representation="cartoon", selection=f"{name}_active_site_residues")  # Hide cartoon representation of protein

        color_protein_chains(name)  # Color protein chains


_original_load = cmd.load  # Backup the original load function
_original_fetch = cmd.fetch  # Backup the original fetch function

def custom_load(*args, **kwargs):
    """
    Calls the original load function with the same arguments
    Looks for the object name under the key "object". If
    not found, it checks the second argument of the load function.
    If still not found, it returns None.
    Calls the after_load_callback function with the object name.
    Args:
        *args: Positional arguments passed to the load function.
        **kwargs: Keyword arguments passed to the load function.
    Returns:
        original load function result
    """
    print("custom_load() called with:", args, kwargs, flush=True)
    result = _original_load(*args, **kwargs) # Call the original load function with the same arguments
        
    obj_name = kwargs.get("object")
    if not obj_name:
        if len(args) > 1 and isinstance(args[1], str):
            obj_name = args[1] #Use the second argument as the object name
        if not obj_name:
        # If no explicit object name, fallback to the file name
            obj_name = os.path.basename(args[0]).split('.')[0] if len(args) > 0 and isinstance(args[0], str) else None
            
    if obj_name:
        print("Object loaded:", obj_name, flush=True)
        after_load_callback([obj_name]) # Call the callback function with the object name
    else:
        print("No object name found in load arguments.", flush=True)
    
    
    return result

def custom_fetch(*args, **kwargs):
    """
    Calls the original fetch function with the same arguments
    Looks for the object name under the key "name". If
    not found, it checks the first argument of the fetch function.
    """
    print("custom_fetch() called with:", args, kwargs, flush=True)
    result = _original_fetch(*args, **kwargs) # Call the original fetch function with the same arguments
        
    #Fetch returns a list of object names
    object_names = result if isinstance(result, list) else [result]
    print("Fetched objects:", object_names, flush=True)
    after_load_callback(object_names) # Call the callback function with the object name
    return result

cmd.load = custom_load # Override the original load function with the custom one
cmd.fetch = custom_fetch #Override the original fetch function with the custom one
print("Hooked cmd.load and cmd.fetch successfully")


# ==== Main Execution ====
pymol_colors()
print("Custom PyMOL colors loaded successfully!", flush=True)
pymol_display_settings()
print("Custom PyMOL settings loaded successfully!", flush=True)
pymol_render_settings()

print("Custom PyMOL render settings loaded successfully!", flush=True)

#Uncomment if you want to troubleshoot with logging
#print("Log file created at:", log_path, flush=True)
#print("To view the log, run: tail -f ~/tmp/pymol_custom_log.txt", flush=True)



