# mikerun
Tools for MIKE observing runs

## Preparation checklist
* make human target catalog
* make iobs and/or jskycalc catalog
* make telescope target catalog
* clear space on laptop for data download/reduction
* prep scripts for on-the-fly data reduction
* prep SMHR linelists
* prep SMHR quick analysis scripts
* prep google doc for exptime estimate

## Setup for quick reductions
* make calibration frames ahead of time
* scp raw data to my laptop (r,b)
* mikedb -d raw_data (Carpy)
* python splitdb.py (Anaconda)
* mikesetup -db redMIKE.db -red -all; make (targ_<objname>); same with blue. (Carpy)
  * Optional: for red side, take dome flats and do -fringekey fringe
* run summary plot (code) on reduced data (Anaconda)
