import matplotlib.pyplot as plt
import imageio
import numpy as np
from pathlib import Path
import os
import shutil
import random
import warnings

def check_data( data, anim_dim ):

    # Check that all input datasets have the same time dimension
    n_data = len(data)
    n_time0 = data[0].sizes[anim_dim]
    
    for dii in data:
        if anim_dim in dii.dims:
            if dii.sizes[anim_dim] != n_time0:
                raise ValueError('Not all time dimensions have the same length')
        

def make_animation(data, fp_out='anim.gif', frame_func = None, anim_dim = 'time',
                   index_stride = 1, verbose = False,
                   fps = 10, fig_transparent = True, 
                   fig_facecolor = 'white', loop = 0):
    ''' Make an animation from an xarray dataset or data array.

    Args:
        data (xr.Dataset or xr.DataArray): Xarray dataset or dataarray over which to
            animate. Note if a dataset is passed, then frame_func must extract a DataArray.
        fp_out (str or pathlib.Path): Output filepath. Can be relative. Default: Working
            Python directory
        frame_func (Python function): Function which describes how a single animation frame
            should be plotted. This function must take in an argument called data_ii. This
            is the  time-indexed data passed to the function by make_animation_xarray().
            This function must return a single plt.figure() instance.
        anim_dim (str): Name of xarray dimension over which to iterate to create animation
            frames.
        index_stride (int): The stride over which to create animation frames.
        verbose (bool): If true, print some information as we go.
        fig_transparent (bool): Whether to make figure transparent in .savefig()
        fig_facecolor (str): Color of figure facecolor in .savefig()

    Returns:
        None. Generates a new animation file.
    '''
    # Silence warnings
    warnings.filterwarnings("ignore")

    try:
        # Get output directory
        fp_out = Path( fp_out ).resolve()
        fp_out_base = fp_out.stem
        dir_out = fp_out.parents[0]
        randstr = str( random.randint(1000000, 9999999) )
        dir_tmp = dir_out / f'xanim_tmp_{fp_out_base}.{randstr}'
        os.mkdir(dir_tmp)
        _try_make_animation( dir_tmp, data, fp_out, frame_func, anim_dim, 
                             index_stride, verbose, fps,
                             fig_transparent, fig_facecolor, loop )
    except:
        # If there's a problem or interrupted, make sure to remove temporary directory
        shutil.rmtree(dir_tmp)



def _try_make_animation( dir_tmp, data, fp_out='anim.gif',
                         frame_func = None, anim_dim = 'time',
                         index_stride = 1, verbose = False,
                         fps = 10, fig_transparent = True, 
                         fig_facecolor = 'white', loop=0):
    ''' The real make_animation function. All the same inputs as make_animation. '''
    
    # Check if input data is list
    if type(data) != list:
        data = [data]
    check_data(data, anim_dim)

    # Get some important numbers
    n_inputs = len(data)
    n_anim = data[0].sizes[anim_dim]
    n_keyframes = np.ceil( n_anim / index_stride ).astype(int)
                               
    # Get number of digits for output files
    n_digits = len(str(n_keyframes))

    # Loop over keyframes and create a bunch of temporary files
    fp_out_list = []
    for ii in range(n_keyframes):
        if verbose:
            pc = np.round(100 * (ii / n_keyframes),1)
            print( f'{pc}%', end='\r')

        # Index xarray function is here to future proof
        data_ii=[]
        for dii in data:
            if anim_dim in dii.dims:
                data_ii.append(dii.isel( {anim_dim:ii*index_stride} ).squeeze() )
            else:
                data_ii.append(dii.squeeze())
        fig = frame_func( *data_ii )

        # Get filename for this index
        idx_str = str(ii).zfill(n_digits)
        fn_out_ii = f'xanim_tmpfile_{idx_str}.png'
        fig.savefig( dir_tmp / fn_out_ii, 
                     transparent = fig_transparent,  
                     facecolor = fig_facecolor )
        fp_out_list.append( dir_tmp / fn_out_ii )
        plt.close(fig)

    compile_images_into_animation( fp_out_list, fp_out, fps = fps, loop = loop )

    shutil.rmtree(dir_tmp)

    return

def ms2fps( ms ):
    ''' Converts milliseconds to frames per second '''
    return 1000 / ms

def compile_images_into_animation( fp_list, fp_out, fps = 10, loop = 0 ):
    '''
    Wraps ImageIO.mimsave to make an animation file from a list of single image files

    Args:
        fp_list (list): List of file paths to images that are to be combined
            into an animation.
        fp_out (str or pathlib.Path): 
            File path for output animation file. Specify extension here.
        duration (int): 
            Frame duration in ms.
    '''

    n_frames = len(fp_list)
    frames = []
    for ii in range(n_frames):
        image = imageio.v2.imread(fp_list[ii])
        frames.append(image)

    duration = ms2fps( fps )
    imageio.mimsave(fp_out,        
                    frames,      
                    duration = duration,
                    loop = loop)    