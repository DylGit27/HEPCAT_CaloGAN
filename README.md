# HEPCAT_CaloGAN
Repository for HEPCAT Summer School 2023 on CaloGAN, created by Dylan Smith and Benjamin Nachman. 

# Instructions
## Step 1: Download Docker

Docker is a container package similar to anaconda to build custom code environments. We will be using a docker to generate Geant4 (G4) simulations (which is very unwieldy to install from source).

Docker can be installed for desktop [here](https://www.docker.com/products/docker-desktop/). 

## Step 2: Download Docker G4 Image

Docker uses objects called images to build environments called containers. The entire code for this specific docker image can be found [here](https://github.com/wtakase/docker-geant4).

Run the following line:
```
git clone --branch v10.5.0 https://github.com/wtakase/docker-geant4
./docker-geant4/download_dataset.sh /path/to/download/geant4/data
```
The image is represented by different modules, so be sure to save them all to one place. 

## Step 3: Download CaloGAN Repository

Be sure to download this github repository `HEPCAT_CaloGAN`; it has an augmented version of the original CaloGAN repository; the CaloGAN repo here is based upon the original repo [here](https://github.com/hep-lbdl/CaloGAN/tree/master). 

## Step 4: Run G4 in the Docker Container

With the Docker image and CaloGAN set up, we can now start generating simulated events in G4. Run the following line:
```
docker run --rm -it -v "/path/to/download/geant4/data:/opt/geant4/data:ro" -v "path/to/CaloGAN-master:/opt/geant4/calogan" --platform linux/amd64 wtakase/geant4:10.05-amd64-alpine
```
The ```--platform``` and G4 Docker version flag will vary based on your Docker host (AMD or ARM; see [original repo](https://github.com/wtakase/docker-geant4) for more info.

This command should open what looks like a normal `bash` or `root` session, but within the Docker container specified by the G4 Docker image. 

## Step 5: Compile and Run G4

Run
```
cmake /opt/geant4/calogan/generation
```
And then run `make` to compile the source files. This should create an executable called `generate`. To run G4 as specified in the CaloGAN repo, run `./generate -m /opt/geant4/calogan/generation/cfg/run2.mac`, in which the terminal should begin printing events.

## Changing G4 Settings

All settings for adjusting the G4 simulation are within `generation` in the CaloGAN subdirectory. `cfg/run2.mac` are where the beam settings are with lines starting `/gps/`. These will stay largely the same, unless you want to change the number of particles recorded under `/run/beamOn` or the energy range.

In `generate/src/DetectorConstruction.cc` is more in-depth parameters for the detector geometry. Specifically, try changing the absorber material (defined `absorberMaterial`) and the thickness (defined `absoThickness`). A list of possible detector materials can be found on the [GEANT4 Material Database](https://geant4-userdoc.web.cern.ch/UsersGuides/ForApplicationDeveloper/html/Appendix/materialNames.html).

## Analysis

The output of running G4 discussed above is a ROOT tree; the branches of the tree are every cell in all three calorimeter layers (with the last three cells being overflow cells). The `convert_uproot.py` script converts this ROOT file to a more ML-friendly H5 file. Run the `convert_uproot_script.sh` script to output the H5 file; be sure to change the input and output file locations. `test.h5` is an example output. Finally, `G4_Viz.ipynb` is a Jupyter notebook that goes through some simple visualization and analysis of your G4 samples.
