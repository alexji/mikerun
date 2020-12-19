# mikerun
Tools for MIKE observing runs

## Alex's preparation checklist
* If you have not, read the [MIKE user manual](http://www.lco.cl/Members/magins/mike-kb/mike-user-manual)
  * Note this has not really been updated for at least 5+ years, so some info is out of date.
* make human target catalog
* make iobs and/or jskycalc catalog
* make telescope target catalog
* clear space on laptop for data download/reduction
* prep scripts for on-the-fly data reduction
* prep SMHR linelists
* prep SMHR quick analysis scripts
* prep google doc for exptime estimate

## Slits and binning
The default setting is 0.7x5.00, 2x2 binning, and slow readout.
If you go to smaller slits, you will want to decrease the binning.

* 1.0 x 5.00 -> 2x2 binning 
* 0.7 x 5.00 -> 2x2 binning 
* 0.5 x 5.00 -> 2x1 binning or 1x1 binning
* 0.35x 5.00 -> 1x1 binning (I have done 2x2 and 2x1 but this underresolves the image..)

The CCD scale is 8.2 pix/arcsec on the blue (0.12 arcsec/pix), 7.5 pix/arcsec on the red (0.13 arcsec/pix).
You need >2 pixels per resolution element to be Nyquist sampled.

The focus is checked in the afternoon by the instrument scientist by taking arcs with two 0.35 boxes and measuriing the PSFs.
It is not recommended to do any focusing yourself.
On my last run, the FWHM was about 2.5 pixels, or ~0.3 arcseconds.

### Readout mode
I almost always do slow readout because I do faint objects.

However if you are doing bright objects, doing fast readout should be okay because you won't be read-noise dominated. This is probably always the case for data you want to take with 0.50 or 0.35 slits.
(The actual per-pixel read noise is about the same, 3-4 electrons per pixel, but I believe in 2x2 binning the effective read noise goes down by 4x because you only do one read per 4 real pixels.)

IMPORTANT, note that the blue side gain changes by a factor of 2, so your counts will change by 2x! The gain is about 0.5 e-/count for slow readout, but 1 e-/count for fast readout. (Carpy accounts for this during reductions as part of the pixel flat.) The red side gain is about the same, 1 e-/count for both readout modes.
The nonlinear limit is also a bit lower for fast readout, so you want to stay below 40k counts instead of 50k counts (see the plots next to the computer in the control room).
And of course, make sure that your calibrations match your observations.

## Calibrations
* Quartz flats (for slit distortion tracing)
* Milky flats (for flat fielding)
* ThAr arcs (for wavelength calibration)
* Fringe flats (dome screen flats for removing fringing at the red end. Use -fringekey <keyname>)
  * This requires a relatively recent carpy version to work
* Recommended to take at least one RV standard

I usually take 20 quartz, 20 milkys the first afternoon, then 5-10 each afternoon after that.
UPDATE: I now usually take 5 quartz each night, given some reduction problems when the temperature changed a lot over a multi-night run. Would be a good idea to take some milky's each night too.

It is recommended in the manual to take milky flats with hot blue stars in twilight, but I do not do this.
Instead I just take a ton of afternoon milky flats.
However for the very bluest orders (if you're pushing down to 3300-3500A), you will want these because you'll need like 100+ milky flats.
You can estimate the flat S/N by sqrt(total counts) and see if it is "infinite" for your needs.

Typical exposure times (TODO). Nonlinearity sets in around 50k counts, so the goal is to have a peak of ~40k.
(TODO more detail/checks) for 0.35" slit, a 10s arc seems needed to get enough counts for a good wavelength calibration (sometimes the reduction pipeline fails).
However, I think only the first afternoon one needs to be taken like this to get an initial identification, and subsequent arcs could be shorter (5s). I have just started taking 5s arcs for everything, except maybe 3s for 1.0 slit.

### Calibration exposure time estimates
Aim for 40k counts at peak in both blue and red. Make sure to check the exposure counts.

| Slit| Bin | Read | Quartz B/R | Milky B/R | Fringe |
| --- | --- | ---- | ---------- | --------- | ------ |
| 0.7 | 2x2 | Slow | 3.5/1.5    | 12/10     | 40     |
| 1.0 | 2x2 | Slow | 8/7        | 12/10     | 40     |
| 0.5 | 2x1 | Slow | 10/5       | 38/35     | 100    |
| 0.5 | 1x1 | Fast | 30/5       | 90/60     | 120?   |
| 0.35| 2x1 | Slow | 14/8       | 50/45     | 150    |

3-5sec ThArs are good.

The fringe frames are taken without the diffuser. Put in the screen, turn on both the Qh and Ql lamps, and turn the internal dome lamp to 2.7V.
NOTE from Josh:
"Dave Osip says that if the variable lamp is only at 2.7V, then what it's
adding to the flux of the Qh lamp is pretty minimal (and the same goes for
Ql)."

NOTE: keep the dome lights off (or at least constant) when you take the milky flats.
Alex screwed this up once showing people the mirror and got milkys with too much intrinsic noise.

NOTE: 2020-12-19 had to roughly double exposure times on quartz's

## Numbering
I usually number each night starting 1000 for the first night, 2000 for the second night, etc.
(For initial calibrations, e.g. milky's, I usually start numbering at 0000)

## Alex's setup for quick reductions
* make calibration frames ahead of time
* scp raw data to my laptop (r,b)
* mikedb -d raw_data (Carpy)
* python splitdb.py (Anaconda), go into different 
* mikesetup -db redMIKE.db -red -all; make (targ_<objname>); same with blue. (Carpy)
  * Optional: for red side, take dome flats and do -fringekey fringe
* run summary plot (code) on reduced data (Anaconda)

Set up (at least) four terminal windows.
(1) Copying, mikedb (carpy)
(2) Anaconda for split_db 
(3) blue folder reduction (carpy)
(4) red folder reduction (carpy)

### Procedure during the night:
* Copy data to raw_data (e.g. `rsync --progress --azvhr user@computer:/path/to/your/data/directory/ .`)
* Run mikedb -d raw_data (terminal 1)
* Run python split_db.py (terminal 2)
* If redoing target, remove targ_obj<red/blue> and obj<red/blue>/ directory (terminal 3/4)
* make regenerate (and/or mikesetup -db <blue/red>MIKE.db -<red/blue> -all) (terminal 3/4)
* make all (or make targ_obj<red/blue>)

## Guanaco computer/MIKE GUI instructions
* In the MIKE GUI, set the observer and check the DataPath
* "mike" opens MIKE GUI, if it's not open, also opens overview for MIKE-blue and red
* "goiraf" opens IRAF (with xgterm; the big red button does it too)
* dmike xxxx: display image xxxx
* imexam (gives "l" and "c" for line and column cuts)
  * `l` = line cut (across), `c` = column cut (vertical)
  * `limexam` and `cimexam` let you set limits on the plot (useful for long exposures)
  * Many other things: `v` = vector cut, `r` or `.` = radial profile 
  * http://stsdas.stsci.edu/cgi-bin/gethelp.cgi?imexamine
* implot xxxx: will do the cut across the middle for you
* Editing fields in the MIKE GUI requires you to put the mouse in the edit field, type in the changes, and press enter

## Observing
* Experience shows that for abundances, you only need to take arcs at the beginning, middle, and end of night (good to about 1-2 km/s). For more precise RVs you will want an adjacent arc.
* You can edit the exposure time on the fly. The best way to stop and read out an exposure is to change the exposure time 
* I would not change readout settings during an exposure, just set it correctly before you begin exposing. But if you make a mistake, you can change it as long as it's not in the 10-30 seconds before the exposure finishes and reads out. I have been burned by changing it too late.
* I usually take an arc whenever I see the temperature changing a lot (by ~0.5 deg), since this tends to be when it shifts.
* Arcs can be taken while slewing (unless you want super precise RVs).
* It's a good idea to take an arc whenever you change the slit, as in principle the slit position could change slightly. But in practice, I haven't noticed a difference (at the 1-2 km/s level).
* MIKE does not have a rotator. Good for stability, bad for atmospheric dispersion. Because guiding is only done in R band, at airmass > 1.5 if you care about blue light you will want to move the star a bit in the slit. Ian Thompson says he "guides low", i.e. move the star down in the slit viewer.
You can and should check this (can do in twilight with a bright star; you can see where the slit is from the sky background), but moving an object down on the slit viewer makes the object trace move right on the blue CCD (as viewed on the MIKE GUI).
Note also that the blue and red object locations are flipped on the CCDs (right on blue = left on red).
Do this only by about 10-20% of the slit length, or reductions can get painful.

## To-do list
- [ ] Add RV standards catalogs/scripts
- [ ] Add hot blue stars catalog?
- [ ] Add code to turn lists of objects/coordinates into a MIKE observing catalog
- [ ] Add something for finding charts
- [ ] Add something for observation planning
- [ ] Add autosummary script
- [ ] Add exposure time calculator

## Instrument Notes
* 2019-3-7: since my last run in Nov 2018, they moved the quartz lamp to be a bit further away. I find calibration times need about 3-4x more exposure to achieve similar counts. The ThAr should not be affected.
* 2019-6-13: the lamp apparently has been moved back, since we needed much shorter exposure times this run.
* 2020-12-19: there are problems with the ADC alignment between the two parts, which can cause you to lose as much as 90% of the light on the blue end. It will be fixed soon, but make sure to keep an eye out for this! You can see if there's a problem by looking at the object trace with respect to wavelength (which should be perfectly down the middle if the ADC is working well)

# Reduction Instructions

Note: I recommend using this "new" version of CarPy that resolves many bugs:
- Go to ftp://ftp.obs.carnegiescience.edu/pub/kelson 
- Get `dist20190610.tgz`
- In your CarPy directory (e.g. `/usr/local/CarPy/`), make a backup of the `dist` folder
- Unzip the file into the CarPy Directory, it should make a new `dist folder

How to reduce data:
- Put all your raw data in one directory. I will call it `raw_data` in these instructions, but replace it however you want.
  - CarPy searches for every file in `raw_data/*.fits`. Subdirectories of `raw_data` will be ignored.
- Enter the CarPy environment (e.g. `source /usr/local/CarPy/Setup.bash`)
- Run `mikedb -d raw_data`. This will create a file `raw_dataMIKE.db`
- Open `raw_dataMIKE.db` and make any manual modifications needed.
  - Any changes you make have to be done for both the blue and red files in `raw_dataMIKE.db` (I often do just the blue ones at the top of this file, then forget to do the red ones)
  - If any frames were bad and/or test frames, you can delete them in this file and they will be ignored
  - CarPy uses the object names to identify calibration frames
    - Anything with `thar` in the object name is assumed to be an arc.
    - Anything with `milky` in the object name is assumed to be a milky flat.
    - Anything with `quartz` in the object name is assumed to be a quartz flat.
  - If two or more frames have the same object name, CarPy will reduce the frames _together_ into one file. See [this paper](https://code.obs.carnegiescience.edu/Algorithms/ghlb/view) for details (or talk to Alex, it's a complicated paper). You can reduce frames individually by editing the `raw_dataMIKE.db` file so that each frame has a different name (e.g. for object `my-RRL`, where the velocities change between individual exposures, I would rename them `my-RRL-1` and `my-RRL-2`).
  - All the frames will be assumed to have the same slit and chip binning. If that's not the case, pick the files from one slit and delete the rest.
    - It is generally advised to make subdirectories for each setting
    - The script `split_db.py` here was made to do that automatically, you can play around with it or write your own.
    - It is generally advised to reduce the blue and red chips in separate directories, although you don't have to. You can separate that manually, or use `split_db.py`
- Run `mikesetup -db raw_dataMIKE.db -blue -all` and `mikesetup -db raw_dataMIKE.db -red -all`
  - This command creates a bunch of directories, symbolic links, and Makefiles.
  - As mentioned above, I usually make two `.db` files in two different directories, one for each chip. If you do that, `cd` into the relevant directory before you call `mikesetup`.
  - If you have fringe flats, make sure that the object name has `fringe` and add `-fringekey fringe`.
    - Some older versions of CarPy do not have the correct implementation of fringe flats. If your reduced data look weird, just skip the fringe flats and contact Dan Kelson later for an up-to-date version
- Run `make all` and things should work!

## How it works
I will describe the stages of the reduction here in the future. In the meantime, you can see all the stages of the reduction by looking at the Makefile that is created by `mikesetup`.

## Advanced reduction Notes
Make sure to inspect the wavelength calibration output.
For instance, look at `lampblue/lampblue_lampXXXXfbspecshisto.ps`.
If the residuals have obvious trends, this means the wavelength calibration is off.
It is reasonably common for the blue side calibration to be off by a few tenths of angstroms at order edges.
You can also look order-by-order in `lampblue/lampblue_lampXXXXfbspecsmatch.ps`, which shows which lines are being iteratively rejected in the wavelength solution.

To fix the wavelength calibration, go to `lampblue/Makefile` and look for these things:
```
stage-wdist: stage-xdist-copy
...
mikeMatchOrders lampblue_lamp1002fb.fits
mikeFindLines lampblue_lampXXXXfbspecs.fits -fwhm 2.500000 -th 10.000000
mikeMatchLamps lampblue_lampXXXXfbspecs.fits -x 5 -o 4 -maxsh 300
```
If the error message says that you are not finding enough lines, you can adjust `-fwhm` (minimum line FWHM) or `-th` (detection threshold) in `mikeFindLines`.
If the solution is a bad fit, you can change `-x` or `-o` for `mikeMatchLamps` to change the degree of the polynomial fit in the X direction (`-x`) or in the Y direction (`-o` for order, I think).
I think that Carpy uses all lines in all orders to determine an overall distortion, which helps give pretty good wavelength solutions even in orders without that many arc lines. However, this can also lead to bad fits so you HAVE to inspect if you are changing these things around.

It is fairly common for Carpy to die during wavelength calibration. A common failure mode is when the wavelength solution is bad, so bad that it becomes non-monotonic. There will be an unhelpful error message related to `splrep` when that happens, because fitting splines requires the input wavelengths to be monotonic. If this happens, it means your wavelength calibration is bad.
We have also found in practice that the exact failures can change depending on what version of Carpy you are using (I use an old version on my laptop that I installed in 2015 and don't want to touch because it just works, but right now I do all my final reductions on the Carnegie computers to take advantage of Dan Kelson's latest but non-version-controlled improvements).

Also note that there were upgrades made to the wavelength calibration happening in about 2017 or 2018. This helped remove a lot of the previous crashes with slits that are not 0.7 arcsec, plus it was more accurate overall. The 2019 version (see above) is what I recommend.

Sometimes orders are missing. In the `star<blue/red>.out1` file take a look for `What to keep...` and see which frame's orders are the bad ones (`False`).
Usually it is because a frame doesn't have enough flux in those orders.
Not sure what the problem is yet, but for now you can just drop those.
