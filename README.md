# xAnimate Package : Easier xarray animation
Small package for easing the basic animation of data in an Xarray DataArray.

The basic use of this package is to create a function that plots a single frame. 
This can then be passed to `make_animation()` to loop through a dataset
and make an animation.

Essentially this package wraps some ImageIO functions to make quick exploratory animations easier.
`make_animation()` is the essential function. You can pass your xarray dataset to this
routine. A function is also passed, which controls how to plot a single frame. See below
for an example.

Running `make_animation()` will create a temporary directory in the same directory as
your specified output file. This contains images of individual frames, which are later compiled
into the output animation and removed (along with the temporary directory).

## Installation
There is no pip or conda install for this package at the moment

1. Clone this repository.
2. Activate your conda environment of choice.
3. Change directory into the top level of the repo
4. Enter `pip install .`

## Useage examples

### 1. Make animation of dataarray using a bespoke frame plotting function

Import what we need:

```python
import xAnimate
import xarray as xr
import matplotlib.pyplot as plt
```

Read in your xarray dataset, with chunking if you want:

```python
fp = <PATH TO NETCDF FILE>
ds = xr.open_dataset(fp, chunks={'ocean_time':10})
```

Next, define a single function to plot a single frame of this data. This function will be
applied to the xarray dataset to create individual frames. The only things that matter
to this package are that it takes an input argument called `data_ii` (which is data from
a single iteration of the plotting) and outputs the `matplotlib.figure()` object. For example
to apply the basic xarray `.plot()` routine with some preset params:

```python
def frame_func( data_ii ):
    f = data_ii.plot(vmin = -.5, vmax = .5, cmap=plt.get_cmap('bwr', 12)).figure
    return f
```

Then we can animate the data using `xAnimate.make_animation()`:

```python
xAnimate.make_animation( ds.zeta, fp_out = './anim.gif',
                         anim_dim = 'ocean_time', 
                         frame_func = frame_func)
```

There are a number of optional arguments you can pass to this routine, which you can find
in docstring of the function.

### 2. Make animation using the default Xarray xr.DataArray.plot() function

If you are animating a single data array, you can call the xr.DataArray.plot() function by importing the
`xAnimate.frames` module. This contains a `Plot` class, which can be used in place of a bespoke function.
You can pass this class directly to the make_animation function (using the `frame_func` argument), passing
any of the arguments for `xr.DataArray.plot()`.

An example might be a better way to explain:

```
import xAnimate
import xAnimate.frames as frames

# Read dataset from netcdf
fp = <PATH TO NETCDF FILE>
ds = xr.open_dataset(fp, chunks={'ocean_time':10})

# Make animation
xAnimate.make_animation( ds.zeta, 
                         fp_out = './anim.gif',
                         anim_dim = 'ocean_time', 
                         frame_func = frames.Plot(vmin = 0, cmap='Reds'))
```

Alternatively, you can instantiate `Plot()` before the make animation call:

```
plot_func = frames.Plot(vmin = 0, vmax = 1, cmap='Reds')
xAnimate.make_animation( ds.zeta, 
                         fp_out = './anim.gif',
                         anim_dim = 'ocean_time', 
                         frame_func = plot_func)
```

