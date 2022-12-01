# Introduction

This project was created to allow for the augmentation of time-series dataset. Time series data are widely used in machine learning. They are commonly used in model  training for prediction and classification, to name a few. However, there have been instance where there were relatively lack of time series data to train the model, which resulted in either underfitting or low generalisation.

"To remedy this, we use Singular Spectrum Analysis (SSA) to seperate a signal into trends and cycles -to describe the shape of the signal- and low level components. In a novel way we subject the low level component to randomizing processes then recombine this with the original trend and cycle components to form a synthetic time series."

Lee, Tracey & Chan, H. & Leo, K. & Chew, Effie & Zhao, Ling & Sanei, Saeid. (2022). Improving Rehabilitative Assessment with Statistical and Shape Preserving Surrogate Data and Singular Spectrum Analysis. 58-63. 10.23919/SPA53010.2022.9927805. 

<br/>

# How to run Time-Series-Date-Augmentation

## Table of Contents

1. [Getting Started](#getting-started)
   
   1. [Install Python]()
   
   2. [Install Anaconda]()
   
   3. [Create Conda Environment]()
   
   4. [Install Dependencies]()

2. [Project Structure]()
   
   1. [Directory Structure]()
   
   2. [Data Directory]()
      
      1. [Score File]()
      
      2. [Data File Naming Convention]()
      
      3. [wrkdir Directory]()

3. [Run the project]()
   
   1. [Setting up]()

4. [Troubleshooting]()

<br/>

# Getting Started <small>[[Top](#table-of-contents)]</small>

## 1. Install Python

Before running this project, you'll need to install Python.

* [Here is a link to the Python downloads page.](https://www.python.org/downloads/)

* [Here is a helpful guide to installing Python on various operating systems.](https://wiki.python.org/moin/BeginnersGuide/Download)

____

<br/>

## 2. Install Anaconda

* [Here is a link to the Anaconda Installer.](https://www.anaconda.com/)

* [Here is a helpful guide to installing Anaconda on various operating systems.](https://docs.anaconda.com/anaconda/install/index.html)

---

<br/>

## 3. Create Anaconda Environment

Two options:

* Using Anaconda prompt:
  
  ```bash
  conda create --name tsgen
  ```

* Using graphical interface:
  
  [Here is a guide to create conda environment using GUI](https://docs.anaconda.com/navigator/tutorials/manage-environments/)

---

<br/>

## 4. Installing Dependencies

* Navigate to project directory:
  
  ```
  C:\path\to\project\dir\time-series-data-augmentation>
  ```

* Switch to 'tsgen' environment:
  
  ```
  ..\time-series-data-augmentation> conda activate tsgen
  ```

* Pip install the dependancies from requirements.txt:
  
  ```
  (tsgen)..\time-series-data-augmentation> pip3 install -r requirements.txt
  ```

<br/>

<br/>

# Project Structure <small>[[Top](#table-of-contents)]</small>

## 1. Directory structure

```
time-series-data-augmentation
|__analyse
|    |__routines.py
|    |__ssa.py
|    |__surrog.py
|
|__data
|__allSurr1D.py
|__pltSSsur.py
|__run_allSurr1D.ipynb
|__run_pltSSsur.ipynb
```

* **analyse**: contains local modules.
* data: dataset directory.
* **allSurr1D.py**: script to generate surrogate data from all the files in data dir.
* **pltSSsur.py**: script to generate one surrogate data from one sample data.
* **run_allSSurr1D.ipynb, run_pltSSsur.ipynb** : jupyter notebook to run the script. Generate surrogate from either all sample or one sample, plot graph, save synthesized data, and plot the output.

---

<br/>

## 2. Data Directory

* ### Score file
  
  Contains list of score for each sample data. (i.e what class the sample belongs).
  
  Sample content (format: \<Sample Name> \<Score\> ):
  
  ```
  P01 0
  P02 3
  P03 1
  .
  P34 2
  ```

---

<br/>

* ### Data File Naming Convention
  
  Generally, each sample file should follow this naming convention:
  
  ```
  <Sample Name><Seperator><Identifier>
  ```
  
  * \<Sample Name\> - Name of the sample.
  
  * \<Seperator\> - Seperator *symbol* to set apart between name and identifier.
    
    * Valid separator: [ _ \. \s - \) \( ]
  
  * \<Identifier\> - ID of the sample if multiple data are collected for that sample (can be omited if there is only one data per sample).
    
    <br/>
  
  Currently, only .csv and .bin files are accepted.

---

<br/>

* ### wrkdir Directory
  
  wrkdir is a working directory containing generated surrogate data, sorted to respective classes.

<br/>

<br/>

# Run the Project <small>[[Top](#table-of-contents)]</small>

* ### Setting up
  
  To run the project, go to either of these jupyter notebook files:
  
  | Name                | Description                                                                        |
  | ------------------- | ---------------------------------------------------------------------------------- |
  | run_allSurr1D.ipynb | Generates surrogate data for all files in data set and saves the output to wrkdir. |
  | run_pltSSsur.ipynb  | Generates surrogate data for one sample and plot the output.                       |
  
  <br/>
  
  Before running the cell, verify that:
  
  1. Data directory is not empty and contains sample file(s) with appropriate naming convention as mentioned above.
  
  2. 'Score' file is present in Data directory and contains "\<SAMPLE\> \<SCORE\>'' value pair.
  
  3. Code is running in the correct Python environment (tsgen).
     
     ```powershell
     conda activate tsgen # to activate tsgen environment
     ```

<br/>

<br/>

# Troubleshooting <small>[[Top](#table-of-contents)]</small>

* cannot find conda in path - pray to jesus
* 
