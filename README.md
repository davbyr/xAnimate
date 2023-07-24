# xAnimate : Quicker xarray animation
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

## Usage examples

### 1. Make animation of a single dataarray using a bespoke frame plotting function

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

Next, define a single function to plot a single frame of this data -- called a "Frame Function". 
This function will be applied to the xarray dataset to create individual frames. 
A Frame Function must take at least one DataArray or Dataset as input. It may also take multiple.
In addition, it must return a single `matplotlib.figure()` object. For example, we can plot a simple
pcolormesh and animate it as follows:

```python
def frame_func( data ):
    f,a = plt.subplots(1,1)
    a.pcolormesh( data.lon, data.lat, data, vmin=-.4, vmax=.4, cmap=plt.get_cmap('Blues',12))
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

### 2. Make animation using multiple dataarrays and/or datasets

As mentioned in the previous section, you can also pass multiple datasets or dataarrays to
a frame function and `make_animation()`. For example, maybe we want to plot a pcolormesh
with a contour overlayed from a different dataset:

```python
def frame_func( data, dataset ):
    f,a = plt.subplots(1,1)
    a.pcolormesh( data.lon, data.lat, data, vmin=-.4, vmax=.4, cmap=plt.get_cmap('Blues',12))
    a.contour( dataset.lon, dataset.lat, dataset.contourdata )
    return f
```

Then, we can use `make_animation()` by passing our data array and datasets in a list:
```python
xAnimate.make_animation( [ds.zeta, ds], fp_out = './anim.gif',
                         anim_dim = 'ocean_time', 
                         frame_func = frame_func)
```

When using multiple datasets, you must ensure that all inputs have the same time dimension,
both in terms of length and name. Spatial dimensions can vary however.
