# i550-Signal-to-Noise-Method
i550 test was designed to meet the following requirements:  Accurately represent the quantitative measurement precision of any Raman system, Test a representative range of exposure time and Raman scattering cross section, Be independent of spectrometer design factors like dispersion and pixel size

Introduction

Raman analyzers take many forms, from tiny handheld units to enormous laboratory devices, each designed for a specific set of tasks. Process Raman analyzers are a specific subset of systems which are intended to make quantitative chemical measurements in real time, providing accurate and actionable information on a process or reaction so that deviations can be addressed and yields can be optimized. As such, Raman users (and potential users) need a consistent and reliable method for evaluating the performance of a given process analyzer. 

This need is particularly acute as some Raman vendors claim that their devices have “high throughput” characteristics or deliver “high sensitivity”, but provide no quantification of their analyzers’ actual measurement performance. Even worse, some Raman vendors deliberately increase the gain (amplification) of the analog-to-digital conversion on their instrument’s sensor to make the Raman peaks appear taller, or apply spectral smoothing to the data readout (prior to any chemometric proprecessing) to decrease the apparent noise. These tricks can make the spectra look better to the untrained human eye and can also reach saturation faster, but they do not actually improve the quality of the chemometric predictions. The astute Raman user must take care not to be fooled by such shenanigans, and apply solid quantitative methods to the comparison of different Raman systems.

The most thorough means of evaluating the suitability of Raman analyzers for a specific application is to collect many spectra of many samples of the actual chemical matrices from the process (or appropriate proxies), create multivariate chemometric models to predict the chemical concentration(s) of interest, and see which analyzer yields the lowest chemometric errors (e.g. RMSECV or RMSEP values). However, this approach requires significant effort and may not be warranted for an initial evaluation. 

As a precursor to this sort of application-specific trial, we propose a simple standardized method, referred to as the “i550” test, which can be performed with any Raman analyzer to assess its quantitative precision and sensitivity. This test requires a single readily-available analyte, isopropyl alcohol (also known as IPA or isopropanol), and takes less than 15 minutes of data collection. The data analysis procedure (detailed below) is straightforward and fully deterministic (no subjective judgements), and it captures most sources of noise which can impact the precision of a process Raman measurement. Users can easily run this test on any Raman system and compare the quantitative results to any other Raman system to determine which one is better. Manufacturers of Raman analyzers are also welcome to perform the test themselves and share the results with customers. With this assessment tool, we hope to provide the process Raman analyzer marketplace with a convenient and robust method for evaluating which systems are best suited for a given PAT scenario.

Rationale

The i550 test was designed to meet the following requirements:

•	Accurately represent the quantitative measurement precision of any Raman system
•	Test a representative range of exposure time and Raman scattering cross section
•	Be independent of spectrometer design factors like dispersion and pixel size
•	Be independent of the spectroscopic calibration or gain setting of the analyzer
•	Provide a way to separate spectrometer and detector noise from laser variation noise
•	Employ a univariate analysis algorithm as a simplest common denominator and evaluate the instrumentation itself rather than including complex multivariate processing steps

Raman system setup

In the context of this document, a “Raman system” comprises an excitation laser, fiber optic cables, a Raman probe, and a spectrometer. Additional accessories such as a multiplexer may also be part of a system. Changing any component of the system makes a new system, as the optical characteristics of the components and their interconnections will have changed. As such, the i550 test can be used to compare different Raman analyzers, or different configurations of the same base analyzer unit, e.g. how much performance is lost if we add a multiplexer, or which of three different probes is likely to deliver the best results? If the excitation laser power is adjustable, changing this parameter can also be considered a change in the system, so one might run the i550 test on the same physical configuration of an analyzer while comparing the performance at 200 mW versus 400 mW laser power, for instance.

Follow this procedure to prepare a Raman system for the test:

1.	Set up the Raman system as per the manufacturer’s instructions, power it on, allow it to warm up, and perform all recommended calibrations (although the i550 test is relatively insensitive to the calibration state of the system).
2.	Place a suitable quantity of 99% IPA in a container so that the probe can measure the IPA without interference from the container. 
3.	If using an immersion probe, place it in the IPA. Make sure that the probe tip is at least 1 cm away (and ideally 3 to 5 cm away) from the sides and bottom of the container to avoid spectral contamination. A stainless steel container is recommended rather than glass or plastic, as stainless steel has the lowest Raman background signature.
4.	If using a non-contact probe, focus the probe beam upon the IPA and adjust the position of the probe or container to get the strongest Raman signal of IPA with a minimum of interference from the container. For best results, aim the probe downwards upon the top surface of the IPA, not through the sides of a transparent container.
5.	Take steps to eliminate ambient light contamination. A light-tight sample chamber is the best method to isolate the sample from ambient or background light sources, but aluminum foil, black cloth, or turning out all lights in the room are also adequate as long as they fully suppress the ambient light.
Data acquisition, part 1
1.	Set the exposure time and number of averages/accumulations so that the total integration time per spectrum is 50 milliseconds (ms). This might be a single exposure of 50 ms duration, or 5 exposures of 10 ms each, or any other combination that totals 50 ms of “shutter open” time. Readout time between exposures does not have to counted.
2.	Set the number of collected spectra to 100, and configure the software to write those spectra to disk files or other storage medium. The spectra can all be written to a single file, or each spectrum to an individual file, whichever is easier for the postprocessing analysis. If you are using Tornado’s Matlab or Python scripts for the analysis, please select individual files, one spectrum per file, with SPC output format.
3.	Turn on dark/background subtraction. Turn on cosmic ray filtering if that is available and will not increase the total integration time.
4.	Start the data acquisition sequence and permit it to run to completion.

Data acquisition, part 2

1.	Set the exposure time and number of averages/accumulations so that the total integration time per spectrum is 5.000 seconds. This might be 100 exposures of 50 ms duration, or 10 exposures of 500 ms each, or a single 5 second exposure, or any other combination that totals 5000 ms of “shutter open” time. Readout time between exposures does not have to counted. For typical Raman analyzers, best results will be obtained if the exposure time is selected such that the strongest IPA peak uses most of the dynamic range of the detector, e.g. peak intensity is 80-90% of the maximum intensity.
2.	Set the number of collected spectra to 100, and configure the software to write those spectra to disk files or other storage medium. The spectra can all be written to a single file, or each spectrum to an individual file, whichever is easier for the postprocessing analysis. If you are using Tornado’s Matlab script for the analysis, please select individual files, one spectrum per file, with SPC output format.
3.	Turn on dark/background subtraction. Turn on cosmic ray filtering if that is available and will not increase the total integration time.
4.	Start the data acquisition sequence and permit it to run to completion.

Data analysis

1.	Using the 100 spectra with 50 ms integration time:
a.	For each spectrum, add together all the intensity values between 330 and 550 cm-1, creating an array of 100 univariate area measurements for the first Raman band, which we will call A1.
b.	Calculate the mean of the 100 values in A1 and call this mean signal S1.
c.	Calculate the standard deviation of the 100 values in A1 and call this noise value N1.
d.	Divide the S1 by N1 to determine the signal-to-noise ratio SNR1 of this first IPA band. Enter this value into the appropriate cell (“50 ms” and “strong band”) of the table below.
e.	Repeat steps (a)-(d) with the second IPA band using boundaries of 2015 to 2145 cm-1. Compute the mean value of the band area S2 and the standard deviation N2, and then enter the resulting signal-to-noise ratio SNR2 = S2 / N2 value in the appropriate cell (“50 ms” and “weak band”) of the table below.
f.	Repeat step (a) with the third Raman band which will use several strong peaks of IPA to provide an intensity normalization reference. Using boundaries of 885 to 1600 cm-1, create an array of 100 univariate area measurements and call it A3. 
g.	Divide A1 by A3 and call it A1n. Calculate the mean of A1n and call it S1n. Calculate the standard deviation of A1n and call it N1n. Divide S1n by N1n to get the normalized signal-to-noise ratio SNR1n and enter it in the appropriate cell (“50 ms normalized” and strong band”).
h.	Divide A2 by A3 and call it A2n. Calculate the mean of A2n and call it S2n. Calculate the standard deviation of A2n and call it N2n. Divide S2n by N2n to get the normalized signal-to-noise ratio SNR2n and enter it in the appropriate cell (“50 ms normalized” and “weak band”).
2.	Repeat all steps in 1(a) through 1(h) using the 5 sec exposure time data, and enter the SNR values in the 3rd and 4th rows of the table.
3.	Take the average of all eight SNR values in the table and enter that average value in the last cell of the table.

