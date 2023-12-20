# i550 Signal to Noise Method

## Overview
i550 test was designed to meet the following requirements:  Accurately represent the quantitative measurement precision of any Raman system, Test a representative range of exposure time and Raman scattering cross section, Be independent of spectrometer design factors like dispersion and pixel size.

## Introduction

Raman analyzers take many forms, from tiny handheld units to enormous laboratory devices, each designed for a specific set of tasks. Process Raman analyzers are a specific subset of systems which are intended to make quantitative chemical measurements in real time, providing accurate and actionable information on a process or reaction so that deviations can be addressed and yields can be optimized. As such, Raman users (and potential users) need a consistent and reliable method for evaluating the performance of a given process analyzer. 

This need is particularly acute as some Raman vendors claim that their devices have “high throughput” characteristics or deliver “high sensitivity”, but provide no quantification of their analyzers’ actual measurement performance. Even worse, some Raman vendors deliberately increase the gain (amplification) of the analog-to-digital conversion on their instrument’s sensor to make the Raman peaks appear taller, or apply spectral smoothing to the data readout (prior to any chemometric proprecessing) to decrease the apparent noise. These tricks can make the spectra look better to the untrained human eye and can also reach saturation faster, but they do not actually improve the quality of the chemometric predictions. The astute Raman user must take care not to be fooled by such shenanigans, and apply solid quantitative methods to the comparison of different Raman systems.

The most thorough means of evaluating the suitability of Raman analyzers for a specific application is to collect many spectra of many samples of the actual chemical matrices from the process (or appropriate proxies), create multivariate chemometric models to predict the chemical concentration(s) of interest, and see which analyzer yields the lowest chemometric errors (e.g. RMSECV or RMSEP values). However, this approach requires significant effort and may not be warranted for an initial evaluation. 

As a precursor to this sort of application-specific trial, we propose a simple standardized method, referred to as the “i550” test, which can be performed with any Raman analyzer to assess its quantitative precision and sensitivity. This test requires a single readily-available analyte, isopropyl alcohol (also known as IPA or isopropanol), and takes less than 15 minutes of data collection. The data analysis procedure (detailed below) is straightforward and fully deterministic (no subjective judgements), and it captures most sources of noise which can impact the precision of a process Raman measurement. Users can easily run this test on any Raman system and compare the quantitative results to any other Raman system to determine which one is better. Manufacturers of Raman analyzers are also welcome to perform the test themselves and share the results with customers. With this assessment tool, we hope to provide the process Raman analyzer marketplace with a convenient and robust method for evaluating which systems are best suited for a given PAT scenario.

## Rationale

The i550 test was designed to meet the following requirements:

- Accurately represent the quantitative measurement precision of any Raman system
- Test a representative range of exposure time and Raman scattering cross section
- Be independent of spectrometer design factors like dispersion and pixel size
- Be independent of the spectroscopic calibration or gain setting of the analyzer
- Provide a way to separate spectrometer and detector noise from laser variation noise
- Employ a univariate analysis algorithm as a simplest common denominator and evaluate the instrumentation itself rather than including complex multivariate processing steps

## Data Acquisition

In the context of this document, a “Raman system” comprises an excitation laser, fiber optic cables, a Raman probe, and a spectrometer. Additional accessories such as a multiplexer may also be part of a system. Changing any component of the system makes a new system, as the optical characteristics of the components and their interconnections will have changed. As such, the i550 test can be used to compare different Raman analyzers, or different configurations of the same base analyzer unit, e.g. how much performance is lost if we add a multiplexer, or which of three different probes is likely to deliver the best results? If the excitation laser power is adjustable, changing this parameter can also be considered a change in the system, so one might run the i550 test on the same physical configuration of an analyzer while comparing the performance at 200 mW versus 400 mW laser power, for instance.

Follow this procedure to prepare a Raman system for the test:

1.	Set up the Raman system as per the manufacturer’s instructions, power it on, allow it to warm up, and perform all recommended calibrations (although the i550 test is relatively insensitive to the calibration state of the system).
2.	Place a suitable quantity of a Raman analyte (99% IPA, cyclohexane, polystyrene, or other Raman-active material) in a container so that the probe can measure the material without interference from the container. 
3.	If using an immersion probe, make sure the material is in contact with the probe. Make sure that the probe tip is at least 1 cm away (and ideally 3 to 5 cm away) from the sides and bottom of the container to avoid spectral contamination. A stainless steel container is recommended rather than glass or plastic, as stainless steel has the lowest Raman background signature.
4.	If using a non-contact probe, focus the probe beam upon the material and adjust the position of the probe or container to get the strongest Raman signal of material with a minimum of interference from the container. For best results, aim the probe downwards upon the top surface of the IPA, not through the sides of a transparent container.
5.	Take steps to eliminate ambient light contamination. A light-tight sample chamber is the best method to isolate the sample from ambient or background light sources, but aluminum foil, black cloth, or turning out all lights in the room are also adequate as long as they fully suppress the ambient light.
6.	Set the exposure time and number of averages/accumulations so that the total integration time per spectrum is consistent between instruments.
7.	Set the number of collected spectra to at least 100, and configure the software to write those spectra to disk files or other storage medium. The spectra can all be written to a single file, or each spectrum to an individual file, whichever is easier for the postprocessing analysis. Write each spectrum to an individual file, one spectrum per file, with SPC output format. If CSV, then ensure the csv file format has the x-coordinates in the first column and y-coordinates in the second column.
8.	Turn on dark/background subtraction. Turn on cosmic ray filtering if that is available and will not increase the total integration time.
9.	Start the data acquisition sequence and permit it to run to completion.


## Data analysis

The i550-SNR-Calc.py script performs the following:

1.	Pop-up dialog prompts for filetype, instrument type, and file directory for all saved spectral data.
   
    a. For the number spectra saved, ensure that these are separated in directories by material type, integration time, and instrument type.

2. The next step will prompt for material choice. Depending on the material measured, there are preset band locations already built in for cyclohexane, isopropyl alcohol, and polystyrene. If using a different material, you do have the option to define custom band area measurements. The mathematics applied are as follows:

  	a. For each spectrum, calculate and subtract the linear baseline between the beginning and end of the defined band region.
   
    b. Add together all the baseline subtracted intensity values in the band region, creating an array of univariate area measurements of the same length as the number of spectra selected. 
  	
    c. The mean and standard deviation of the area values are calculated.
  	 	
    d. Divides the mean by standard deviation to determine the signal-to-noise ratio SNR

    e. A dotplot, range-focused spectrum plot, and a trend plot of the band areas are produced and saved in the same directory as the loaded spectra.

    f. A csv with the spectral filenames and peak areas is produced and saved into the same directory as the loaded spectra. 


## Features
Import and analyze spectral data files.
Calculate SNR and RSD for specified analytes.
Visualize spectral data with annotated SNR and RSD information.

## Requirements
Python > 3.9

numpy==1.20.3

matplotlib==3.4.2

spc==0.6.0

easygui==0.98.2

natsort==7.1.1


## License
This project is licensed under the MIT License.




