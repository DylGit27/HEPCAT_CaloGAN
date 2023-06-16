# HEPCAT_CaloGAN
Repository for HEPCAT Summer School 2023 on CaloGAN, created by Dylan Smith and Benjamin Nachman. 

# Instructions
## Step 1: Download Docker

Docker is a container package similar to anaconda to build custom code environments. We will be using a docker to generate Geant4 (G4) simulations (which is very unwieldy to install from source).

Docker can be installed for desktop [here](https://www.docker.com/products/docker-desktop/) 

## Step 2: Download Docker G4 Image

Docker uses objects called images to build environments called containers. The entire code for this specific docker image can be found [here](https://github.com/wtakase/docker-geant4)

Run the following line:
```
git clone --branch v10.5.0 https://github.com/wtakase/docker-geant4
./docker-geant4/download_dataset.sh /path/to/download/geant4/data
```
The image is represented by different modules, so be sure to save them all to one place. 

## Step 3: Download CaloGAN Repository

The CaloGAN repo here is based upon the original repo [here](https://github.com/hep-lbdl/CaloGAN/tree/master). 

## Step 4: Run G4 in the Docker Container

With the Docker image and CaloGAN set up, we can now start generating simulated events in G4. Run the following line:
```
docker run --rm -it -v "/path/to/download/geant4/data:/opt/geant4/data:ro" -v "path/to/CaloGAN-master:/opt/geant4/calogan" --platform linux/amd64 wtakase/geant4:10.05-amd64-alpine
```
The ```--platform``` and G4 Docker version flag will vary based on your Docker host (AMD or ARM; see [original repo](https://github.com/wtakase/docker-geant4) for more info.

This command should open what looks like a normal ```bash``` or ```root``` session, but within the Docker container specified by the G4 Docker image. 

## Step 5: Compile and Run G4

Run
```
cmake /opt/geant4/calogan/generation
```
This should create an executable called `generate`
