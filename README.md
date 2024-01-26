# CREST – A Signal-to-Noise Ratio (SNR) Method for Raman Analyzer Evaluation

## Overview
CREST method was designed to meet the following requirements:  Accurately represent the quantitative measurement precision of any Raman system, Test a representative range of exposure time and Raman scattering cross section, Be independent of spectrometer design factors like dispersion and pixel size.

## Introduction

Raman analyzers come in many different types, ranging from compact handheld units to large laboratory devices, each designed for specific tasks. Process Raman analyzers, a subset of these systems, aim to provide real-time quantitative chemical measurements during processes or reactions. This capability offers precise and timely information, enabling users to address process deviations promptly and optimize yields. To ensure accurate assessments of a given process analyzer’s performance, Raman users and potential users require a consistent and reliable evaluation method to assess whether a specific Raman analyzer will meet their requirements.

This need is underscored by the observation that Raman vendors often describe their devices using terms like "high throughput" or "high sensitivity" without providing detailed quantification of their analyzers' actual measurement performance. In certain instances, vendors may employ strategies such as adjusting analog-to-digital conversion gain or applying spectral smoothing to improve the visual presentation of Raman peaks. While these practices can enhance the apparent performance, it can be misrepresentative of the actual sensitivity and precision of the spectrometric device.

While the most comprehensive analyzer evaluation involves collecting numerous spectra and building multivariate chemometric models, this approach demands significant effort and may be impractical for initial assessments. An efficient alternative quality indicator for Raman instrumentation is the Signal-to-Noise Ratio (SNR). SNR serves as a robust indicator of quantitative measurement precision and sensitivity, as it represents the relationship between the average chemical measurement value (the signal) and the variation or uncertainty in that measurement value (the noise). An analyzer with a higher SNR will deliver more precise chemical measurements and will be able to detect trace constituents of a mixture with better sensitivity. 

There are several approaches to calculating SNR, not all of which are valid for quantitative Raman spectroscopy. Some of the more common methods include: 

1.	Exposure Time to Saturate Spectrometer Camera:

- This method involves determining the time required for the spectrometer camera to reach saturation while measuring a standard analyte. While it provides an indication of the camera's dynamic range, it is less effective for quantifying the instrument's precision and sensitivity, as it focuses on a specific parameter (saturation time) and does not capture other relevant noise variations like photon shot noise and laser power variations. This approach is not recommended for comparing instruments from multiple vendors, as customers can easily be misled by analyzer detectors with high gain settings which artificially amplify the signal.

2.	Raman Peak Height Divided by Background Signal:

- The Raman peak height divided by the background signal is a straightforward method that assesses the ratio of the signal strength to the underlying background noise in the spectrum. While it offers a quick evaluation, this approach can severely  oversimplify the analysis by focusing solely on background noise without considering other factors which also add noise (uncertainty) to the peak measurement. It may be less robust for comprehensive assessments of quantitative precision, and will often significantly underestimate the actual measurement noise.

3.	CREST - Chemometrically Relevant Empirical Spectral Test:
   
- This method involves collecting multiple “replicate” spectral measurements of a single analyte, subtracting a linear baseline from the Raman peak, making a univariate peak area measurement of each spectrum, and calculating the average and standard deviation of these peak area measurements.  This method is considered more robust and more accurate than other methods mentioned previously, as it accounts for most sources of noise which can impact the precision of a process Raman measurement, is straightforward to calculate, and can be used to compare across vendor instruments without requiring a priori knowledge of the details of the instrument hardware. 

## Rationale

The CREST test was designed to meet the following requirements:

- Accurately represent the quantitative measurement precision of any Raman system
- Test a representative range of exposure time and Raman scattering cross section
- Be independent of spectrometer design factors like dispersion and pixel size
- Be independent of the spectroscopic calibration or gain setting of the analyzer
- Provide a way to separate spectrometer and detector noise from laser variation noise
- Employ a univariate analysis algorithm as a simplest common denominator and evaluate the instrumentation itself rather than including complex multivariate processing steps

## Data Acquisition

In the context of this document, a “Raman system” comprises an excitation laser, fiber optic cables, a Raman probe, and a spectrometer. Additional accessories such as a multiplexer may also be part of a system. Changing any component of the system makes a new system, as the optical characteristics of the components and their interconnections will have changed. As such, the CREST test can be used to compare different Raman analyzers, or different configurations of the same base analyzer unit, e.g. how much performance is lost if we add a multiplexer, or which of three different probes is likely to deliver the best results? If the excitation laser power is adjustable, changing this parameter can also be considered a change in the system, so one might run the CREST test on the same physical configuration of an analyzer while comparing the performance at 200 mW versus 400 mW laser power, for instance.

Follow this procedure to prepare a Raman system for the test:

1.	Set up the Raman system as per the manufacturer’s instructions, power it on, allow it to warm up, and perform all recommended calibrations (although the CREST test is relatively insensitive to the calibration state of the system).
2.	Place a suitable quantity of a Raman analyte (99% IPA, cyclohexane, polystyrene, or other Raman-active material) in a container so that the probe can measure the material without interference from the container. 
3.	If using an immersion probe, make sure the material is in contact with the probe. Make sure that the probe tip is at least 1 cm away (and ideally 3 to 5 cm away) from the sides and bottom of the container to avoid spectral contamination. A stainless steel container is recommended rather than glass or plastic, as stainless steel has the lowest Raman background signature.
4.	If using a non-contact probe, focus the probe beam upon the material and adjust the position of the probe or container to get the strongest Raman signal of material with a minimum of interference from the container. For best results, aim the probe downwards upon the top surface of the IPA, not through the sides of a transparent container.
5.	Take steps to eliminate ambient light contamination. A light-tight sample chamber is the best method to isolate the sample from ambient or background light sources, but aluminum foil, black cloth, or turning out all lights in the room are also adequate as long as they fully suppress the ambient light.
6.	Set the exposure time and number of averages/accumulations so that the total integration time per spectrum is consistent between instruments.
7.	Set the number of collected spectra to at least 100, and configure the software to write those spectra to disk files or other storage medium. The spectra can all be written to a single file, or each spectrum to an individual file, whichever is easier for the postprocessing analysis. Write each spectrum to an individual file, one spectrum per file, with SPC output format. If CSV, then ensure the csv file format has the x-coordinates in the first column and y-coordinates in the second column.
8.	Turn on dark/background subtraction. Turn on cosmic ray filtering if that is available and will not increase the total integration time.
9.	Start the data acquisition sequence and permit it to run to completion.


## Data analysis

The CREST-SNR-Calc.py script performs the following:

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




