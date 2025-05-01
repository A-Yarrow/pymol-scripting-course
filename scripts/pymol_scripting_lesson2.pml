# Author: Yarrow Madrona. Pymol script to create black and white quantized protein with colored ligand

# Rendering settings
set ray_trace_mode, 2
set ray_shadows, 0
set fog, 0
set ray_trace_gain, 20
set ray_trace_slope_factor, 5
set antialias, 4
#set hash_max, 300

# Hide organics, water, and active site residues
hide everything, 1EMA_organics
hide everything, 1EMA_active_site_water
hide everything, 1EMA_active_site_residues
show cartoon, 1EMA_A

# Hide foreground
select hide, 1EMA_A and resi 199-207 or 1EMA_A and resi 220-227
hide everything, hide
create hide_object, 1EMA_A and resi 198-208 or 1EMA_A and resi 219-229
hide everything, hide_object

# Background Png
set ray_opaque_background, 1
set bg_rgb, [1,1,1]

set_view (\
     0.754109502,    0.209661528,    0.622382581,\
     0.483664513,   -0.818386257,   -0.310343027,\
     0.444282532,    0.535057366,   -0.718559742,\
     0.000000000,   -0.000000000, -152.335403442,\
    25.307531357,   28.691156387,   38.890853882,\
   120.102386475,  184.568420410,   20.000000000 )

png C:\Users\yarro\pymol_stuff\images\gfp4, width=1700, height=2100, dpi=300, ray=1

# Organics and active site residues Png
hide everything, 1EMA_A
set ray_opaque_background, 0
show spheres, 1EMA_organics
color limegreen, 1EMA_organics
show sticks, 1EMA_active_site_residues and not name n+o+c
set ray_trace_mode, 0
#zoom 1EMA_A
png C:\Users\yarro\pymol_stuff\images\gfp3, width=1700, height=2100, dpi=300, ray=1

# Foreground residues
hide everything, 1EMA_organics or 1EMA_active_site_residues
show cartoon, hide_object
set ray_trace_mode, 2
#zoom 1EMA_A
png C:\Users\yarro\pymol_stuff\images\gfp2, width=1700, height=2100, dpi=300, ray=1

# Foreground2
set ray_trace_mode, 0
color white, hide_object
set cartoon_transparency, 0.5, hide_object
#zoom 1EMA_A
png C:\Users\yarro\pymol_stuff\images\gfp1, width=1700, height=2100, dpi=300, ray=1
