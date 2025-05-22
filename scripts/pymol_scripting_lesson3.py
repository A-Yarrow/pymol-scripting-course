from pymol import cmd, util
import os
import sys

"""
Global settings. These can go in setting file
For simplicity we will keep settings here
In the future they can go in a settings.py file.
"""

#Set Image Directory
IMAGE_DIRECTORY = None #Enter Directory you wnat to save images to e.g. "//wsl.localhost/Ubuntu-24.04/home/yarrow/projects/pymol-scripting-course/media/lesson-3-py-scripts"
#Image Settings
WIDTH = 800
HEIGHT = 600
DPI = 300
ANTIALIAS = 4
#Immediately get the current view for picture taking
CURRENT_VIEW = cmd.get_view()

#Set color for active site residues
LIGAND_COLOR = 'limegreen'
TRANSPARENT_OBJECT_COLOR = 'white'
TRANSPARENT_OBJECT_TRANSPARENCY = 0.5
SELECTION_NAME = 'sele'

def pymol_settings():
    #Ray trace and appearence settings
    cmd.set('ray_shadows', 0) #Remove shadows
    cmd.set('fog', 0) #Remove fog
    cmd.set('ray_trace_gain', 20) #Create a dark outline
    cmd.set('ray_trace_slope_factor', 5) #Remove some shadow constrast
    cmd.set('antialias', ANTIALIAS)#Set the anti-aliasing level to highest available

def transparent_figure(protein:str, transparent_object:str, image_dir:str, pymol_view:str):
    """
    Inputs: Takes in the transparent objects, image dir as string and current/
    /n view as a string
    Saves the transparent figure and the outline of the transparent figure.
    """
    cmd.hide("everything")
    cmd.enable(transparent_object)
    cmd.set('ray_trace_mode', 0) #In case you change the order of calling the figures.
    cmd.show('cartoon', transparent_object)
    cmd.set('cartoon_transparency', TRANSPARENT_OBJECT_TRANSPARENCY)
    cmd.color(TRANSPARENT_OBJECT_COLOR, transparent_object)

    image = os.path.join(image_dir, f'{protein}_1')
    cmd.set_view(pymol_view)
    cmd.png(image, width=WIDTH, height=HEIGHT, dpi=DPI, ray=1)
    
    image2 = os.path.join(image_dir, f'{protein}_2')
    cmd.set('cartoon_transparency', 0)
    cmd.set('ray_trace_mode', 2) #We don't need to set transparency on ray_trace_mode, 2
    cmd.set_view(pymol_view)
    cmd.png(image2, width=WIDTH, height=HEIGHT, dpi=DPI, ray=1)

    print(f"Images saved in: {image} \
          \n{image2}")

def active_site_figure(protein:str, active_site:list, image_dir:str, pymol_view:str):
    """
    Inputs: Active site as a string, image directory as a string, 
    and the current view as a string
    Saves a foreground active site image to the image directory
    
    """
    cmd.hide('everything')
    cmd.set('ray_trace_mode', 0)

    if len(active_site) > 2:
        print("You may choose at most, 2 active site objects \
            \nThe first should be the ligand\
            \nThe second should be the active site residues")
        sys.exit()
    
    elif len(active_site) == 2:
        residues = active_site[1]
        cmd.enable(residues) #Makes sure that objects are not toggled off in the GUI
        cmd.show('sticks', f'{residues} and not name n+o+c')
        util.cbay(residues) #Better to set this color in global variables.

    ligand = active_site[0]
    cmd.enable(ligand) 
    cmd.set('ray_opaque_background', 0)
    #If user sets the ligand_color_off in the command line, the color will represent the GUI
    if LIGAND_COLOR != None:
        cmd.color(LIGAND_COLOR, ligand)
    cmd.show('spheres', ligand)
    print(f"LIGAND_COLOR is now set to: {LIGAND_COLOR}")
    
    image = os.path.join(image_dir, f'{protein}_3')
    cmd.set_view(pymol_view)
    cmd.png(image, width=WIDTH, height=HEIGHT, dpi=DPI, ray=1)
    print(f"Image saved as {image}")


def protein_figure(protein:str, resi_list:list, image_dir:str, pymol_view:str):
    """
    Inputs: Protein as a string, list of selected residues, and 
    image directory as a string
    saves a foreground protein image to the image directory
    Returns the string name of the object that will be in the foreground (transparent)
    """
    cmd.set('ray_trace_mode', 2) #Black and white
    #Expand the selection (padded_resi) and covert lists to a string
    residue_string = "+".join(sorted(str(r) for r in resi_list))
    min_resi = max(1, resi_list[0]-2)
    max_resi = resi_list[-1] + 2

    padded_resi = list(range(min_resi, max_resi + 1))
    expanded_residue_string = "+".join(sorted(str(r) for r in padded_resi))
    
    cmd.hide('everything')
    cmd.show('cartoon', f'{protein} and not resi {residue_string}')
    cmd.create(f'{protein}_transparent', f'{protein} and resi {expanded_residue_string}')
    cmd.set('ray_opaque_background', 1)
    cmd.set('bg_rgb', [1,1,1])
    image = os.path.join(image_dir, f'{protein}_4')
    cmd.set_view(pymol_view)
    cmd.png(image, width=WIDTH, height=HEIGHT, dpi=DPI, ray=1)
    print(f"Image saved in {image}")
    return f'{protein}_transparent'

def set_image_dir(image_dir:str=None):
    """
    Input: Takes in the image directory as a string
    Returns: image directory as a string.
    If no image directory is given look for $HOME/tmp
    If no $HOME/tmp direcotry exists, create one and return it as
    the image directory
    """
    if image_dir:
        if os.path.exists(image_dir):
            print(f'Image directory set as: {image_dir}') 
            return image_dir
        else: 
            print(f"The directory: {image_dir} cannot be found, exiting")
            sys.exit()
    else:
        home_dir = os.path.expanduser("~")
        image_dir = os.path.join(home_dir, 'tmp')
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print(f'Image directory set as: {image_dir}')    
    return image_dir

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
    global LIGAND_COLOR
    pymol_settings()
    args = arg_string.split()
    if len(args) < 2 or len(args) > 4:
        print("Usage: run_selection protein_name ligand residues(optional) ligand_color_off(optional)")
        return
    protein = args[0]
    if len(args) == 3: 
        active_sites = args[1:]
    #Allow the user to turn automated ligand color off. Color will fall back to the GUI color.
    elif len(args) == 4:
        active_sites = args[1:3]
        ligand_color_off = args[-1]
        print(ligand_color_off)
        if ligand_color_off == 'ligand_color_off':
            LIGAND_COLOR = None

    print(f"Looking for {protein} and {active_sites}", flush=True)
    
    protein, active_site = select_objects(protein, active_sites)
    resi_list = get_selection_residues(protein=protein, selection_name=SELECTION_NAME)
    image_dir = set_image_dir(IMAGE_DIRECTORY)
    #Create the background protein figure
    protein_transparent_object = protein_figure(protein, resi_list, image_dir, CURRENT_VIEW)
    active_site_figure(protein, active_sites, image_dir, CURRENT_VIEW)
    transparent_figure(protein=protein, transparent_object=protein_transparent_object, image_dir=image_dir, pymol_view=CURRENT_VIEW)

# Register commands in PyMOL
cmd.extend("select_objects", select_objects)
cmd.extend("get_selection_residues", get_selection_residues)
cmd.extend("run_selection", run_selection)
cmd.extend("get_selection_residues", get_selection_residues)
cmd.extend("set_image_dir", set_image_dir)
cmd.extend("protein_figure", protein_figure)
cmd.extend("active_site_figure", active_site_figure)
cmd.extend("transparent_figure", transparent_figure)
cmd.extend("pymol_settings", pymol_settings)

print(f"PyMOL script loaded. \
      \n Select residues to hide and leave the selection labeled as {SELECTION_NAME} \
      \n Usage: run_selection protein ligand residues \
      \n residues argument is optional \
      \n Remember to separate by a space (not a comma) like: \
      \n e.g. run_selection 1EMA 1EMA_organics 1EMA_active_site_residues \
      \n If you wish to set the ligand colors in the GUI add <ligand_color_off> \
      \n to the end of the command: \
      \n e.g. run_selection 1EMA 1EMA_organics 1EMA_active_site_residues ligand_color_off")

#Function Tests for PDB ID: 1EMA
#select_objects('1EMA_A', ['1EMA_organics', '1EMA_active_site_residues'])
#get_selection_residues('1EMA_A', 'sele')
#set_image_dir()
#set_image_dir("//wsl.localhost/Ubuntu-24.04/home/yarrow/projects/pymol-scripting-course/media/lesson-3-py-scripts")
#protein_figure('1EMA_A', [195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207], '//wsl.localhost/Ubuntu-24.04/home/yarrow/projects/pymol-scripting-course/media/lesson-3-py-scripts', cmd.get_view())
#active_site_figure('1EMA_A', ['1EMA_organics', '1EMA_active_site_residues'], '//wsl.localhost/Ubuntu-24.04/home/yarrow/projects/pymol-scripting-course/media/lesson-3-py-scripts', cmd.get_view())
#transparent_figure('1EMA_A', '1EMA_transparent', '//wsl.localhost/Ubuntu-24.04/home/yarrow/projects/pymol-scripting-course/media/lesson-3-py-scripts', cmd.get_view())
#If using lesson3_gfp.pse, the following should work:
#run_selection 1EMA_A 1EMA_organics 1EMA_active_site_residues

#Funciton Tests for PDB ID: 9COR
#active_site_figure('9COR_A', ['9COR_organics', '9COR_active_site_residues'], '//wsl.localhost/Ubuntu-24.04/home/yarrow/projects/pymol-scripting-course/media/lesson-3-py-scripts', cmd.get_view())
#run_selection 9COR_A 9COR_organics 9COR_active_site_residues
#run_selection 9COR_A 9COR_organics 9COR_active_site_residues ligand_color_off

#Test for PDB ID: 9AX6
#run_selection protein 9AX6_organics 9AX6_active_site_residues ligand_color_off