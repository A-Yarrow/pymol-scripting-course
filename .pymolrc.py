import os

# Detect WSL and disable shaders if needed
if 'WSL' in os.uname().release:
    set('use_shaders', 0)

# ======= General Appearance =======
set('ray_opaque_background', 0)
set('bg_rgb', [1, 1, 1])  # White background
set('cartoon_smooth_loops', 1)
set('cartoon_flat_sheets', 1)
set('cartoon_side_chain_helper', 1)
set('cartoon_fancy_helices', 1)
set('cartoon_transparency', 0.1)

# ======= Labeling =======
set('label_font_id', 7)        # Nicer font
set('label_size', 14)
set('label_color', 'black')

# ======= Colors =======
set('color', 'palegreen')      # Default object color
set('two_sided_lighting', 1)

# ======= Rendering Quality =======
set('ray_trace_mode', 2)
set('ray_shadows', 1)
set('ray_trace_gain', 0.1)
set('antialias', 2)
set('depth_cue', 0)

# ======= Startup Behavior =======
set('auto_zoom', 0)
set('splash', 0)

# ======= Custom color scheme placeholder =======
set_color('deep_sky', [0.0, 0.5, 1.0])
