import os
import sys
from pymol import cmd

# ==== Logging Setup ====
log_path = os.path.expanduser("~/tmp/pymol_custom_log.txt")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logfile = open(log_path, "w")
sys.stdout = logfile
sys.stderr = logfile

print("✅ Loading custom PyMOL settings...", flush=True)
# ==== PyMOL Settings ====
cmd.set('use_shaders', 0)
cmd.set('stick_radius', 0.2)
cmd.set('bg_rgb', [1, 1, 1])
cmd.set('cartoon_smooth_loops', 1)
cmd.set('cartoon_flat_sheets', 1)
cmd.set('cartoon_side_chain_helper', 1)
cmd.set('cartoon_fancy_helices', 1)
cmd.set('cartoon_transparency', 0.1)
cmd.set('label_font_id', 7)
cmd.set('label_size', 14)
cmd.set('label_color', 'black')
cmd.set('two_sided_lighting', 1)
cmd.set('ray_trace_mode', 2)
cmd.set('ray_shadows', 1)
cmd.set('ray_trace_gain', 0.1)
cmd.set('antialias', 2)
cmd.set('depth_cue', 0)

# Custom Colors
cmd.set_color('deep_sky', [0.0, 0.5, 1.0])
cmd.set_color('ocean_mist', [0.2, 0.6, 0.8])
cmd.set_color('coral_punch', [1.0, 0.4, 0.4])
cmd.set_color('forest_glow', [0.0, 0.8, 0.2])
cmd.set_color('nightshade', [0.4, 0.3, 0.6])
cmd.set_color('gold_leaf', [0.9, 0.7, 0.2])

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
        cmd.show("spheres", f"{name} and resname HOH near_to 3.5 of organic")  # Show selected water

# ==== Hook Setup ====
#def setup_custom_hooks():
    """
    Function to set up custom hooks for PyMOL commands.
    This function overrides the default behavior of certain commands
    to include additional functionality.
    """
#    print("Setting up custom hooks...")  # Debug print to confirm this function is being called.
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
    print("🌀 custom_fetch() called with:", args, kwargs, flush=True)
    result = _original_fetch(*args, **kwargs) # Call the original fetch function with the same arguments
        
    #Fetch returns a list of object names
    object_names = result if isinstance(result, list) else [result]
    print("Fetched objects:", object_names, flush=True)
    after_load_callback(object_names) # Call the callback function with the object name
    return result

cmd.load = custom_load # Override the original load function with the custom one
cmd.fetch = custom_fetch #Override the original fetch function with the custom one
print("Hooked cmd.load and cmd.fetch successfully")


#def pymol_ready():
#    setup_custom_hooks()

#cmd.do("python pymol_ready()")


print("✅ Custom PyMOL settings loaded successfully!", flush=True)
print("Log file created at:", log_path, flush=True)
print("To view the log, run: tail -f ~/tmp/pymol_custom_log.txt", flush=True)

