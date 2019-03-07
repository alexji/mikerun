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
* 0.5 x 5.00 -> 2x1 binning 
* 0.35x 5.00 -> 1x1 binning (I have done 2x2 and 2x1 but this underresolves the image..)

The CCD scale is 8.2 pix/arcsec on the blue (0.12 arcsec/pix), 7.5 pix/arcsec on the red (0.13 arcsec/pix).
You need >2 pixels per resolution element to be Nyquist sampled.

The focus is checked in the afternoon by the instrument scientist by taking arcs with two 0.35 boxes and measuriing the PSFs.
It is not recommended to do any focusing yourself.
On my last run, the FWHM was about 2.5 pixels, or ~0.3 arcseconds.

## Calibrations
* Quartz flats (for slit distortion tracing)
* Milky flats (for flat fielding)
* ThAr arcs (for wavelength calibration)
* Fringe flats (dome screen flats for removing fringing at the red end. Use -fringekey <keyname>)
  * This requires a relatively recent carpy version to work
* Recommended to take at least one RV standard

I usually take 20 quartz, 20 milkys the first afternoon, then 5-10 each afternoon after that.

It is recommended in the manual to take milky flats with hot blue stars in twilight, but I do not do this.
Instead I just take a ton of afternoon milky flats.
However for the very bluest orders (if you're pushing down to 3300-3500A), you will want these because you'll need like 100+ milky flats.
You can estimate the flat S/N by sqrt(total counts) and see if it is "infinite" for your needs.

Typical exposure times (TODO). Nonlinearity sets in around 50k counts, so the goal is to have a peak of ~40k.
(TODO more detail/checks) for 0.35" slit, a 10s arc seems needed to get enough counts for a good wavelength calibration (sometimes the reduction pipeline fails).
However, I think only the first afternoon one needs to be taken like this to get an initial identification, and subsequent arcs could be shorter (5s). I have just started taking 5s arcs for everything, except maybe 3s for 1.0 slit.

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
* Copy data to raw_data
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

## Observing
* Experience shows that for abundances, you only need to take arcs at the beginning, middle, and end of night (good to about 1-2 km/s). For more precise RVs you will probably want an adjacent arc.
* I usually take an arc whenever I see the outside temperature changing a lot (by ~0.5 deg), since this tends to be when it shifts.
* Arcs can be taken while slewing (unless you really want super precise RVs, I guess).
* MIKE does not have a rotator. Good for stability, bad for atmospheric dispersion. Because guiding is only done in R band, at airmass > 1.5 if you care about blue light you will want to move the star a bit in the slit. Ian Thompson says he "guides low", i.e. move the star down in the slit viewer. However I have not had a chance to verify that this is the right direction. Note that the blue and red object locations are flipped on the CCDs (right on blue = left on red).
  * TODO check 

## To-do list
- [ ] Add RV standards catalogs
- [ ] Add hot blue stars catalog?
- [ ] Add code to turn lists of objects/coordinates into a MIKE observing catalog
- [ ] Add something for finding charts
- [ ] Add something for observation planning
- [ ] Add autosummary script
- [ ] Add exposure time calculator

## Instrument Notes
* 3-7-2019: since my last run in Nov 2018, they moved the quartz lamp to be a bit further away. I find calibration times need about 3-4x more exposure to achieve similar counts.
