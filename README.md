# GluGo2.0

Pursuing an accurate, personalized, and low-maintenance glucose prediction algorithm for Type 1 Diabetetics (T1D) in the spirit of #WeAreNotWaiting

## Introduction

GluGo2.0 is a startup comprised of students at Wheaton College, in Norton MA. We build on the work of the machine learning team in [GluGo](https://github.com/WheatonCS/GluGo/tree/master/4_Backend_MachineLearning). We're using machine learning to prototype predictive glucose algorithms, the kind that could be implemented in an integrated "closed-loop" system. [OpenAPS](https://openaps.org/), and [Loop](https://loopkit.github.io/loopdocs/) have led the charge for automated T1D management, and news [from Dexcom](https://www.fda.gov/newsevents/newsroom/pressannouncements/ucm602870.htm) and [from Tidepool](https://tidepool.org/tidepool-delivering-loop/) over the past year suggests that widely-accessible, FDA approved closed-loop systems are just on the horizon. Yet there are many barriers that need to be overcome: Neither Loop nor OpenAPS are FDA approved, and neither make hard promises about the safety of their software. Furthermore, the software is often only compatible with outdated insulin pumps, and implementation can be too technically challenging for many people. On the other hand, few health insurance plans currently cover pumps that can be integrated with G5/G6 sensors. Therefore, we seek an algorithm that only utilizes sensor data, without sacrificing the accuracy and personalization of closed-loop algorithms. Such an algorithm could implemented in a sensor-linked alert system. This would sidestep many of the barriers to closed-loop systems by keeping glucose management in the hands of the user, while still providing valuable information about future glucose trends. 

## Contents of This Repository

* csvData - CSVs involved in the construction of a dataset for algorithm training/testing (one patient)
* images - Miscellaneous image files
* jsonData - CGM data (before conversion to CSVs in csvData)
* pythonScripts - Python scripts involved in construction/modification of datasets
* referenceDocuments - A concept brief, along with some relevant files from GluGo
* README.md - This document
