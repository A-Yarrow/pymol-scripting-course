from pymol import cmd
import os

#https://pymol.org/dokuwiki/doku.php?id=setting:ray
def ray_trace():

    cmd.set('ray_trace_mode', 2) #Black and white
    cmd.set('ray_shadows', 0) #Remove shadows
    cmd.set('fog', 0) #Remove fog
    cmd.set('ray_trace_gain', 20) #Create a dark outline
    cmd.set('ray_trace_slope_factor', 5) #Remove some shadow constrast

def quality(anti_alias=4, hash_max=300):

    cmd.set('antialias', anti_alias)#Set the anti-aliasing level to highest available
    cmd.set('hash_max', hash_max)

    #hide residues 197-206
    #hide residues 218-