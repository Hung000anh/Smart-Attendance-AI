# Smart-Attendance-AI

## Introduction

**Smart-Attendance-AI** is an automatic attendance system that uses face recognition technology. This project leverages deep learning models to recognize and identify students from images to automatically record their attendance. This system can be applied in educational environments, companies, or events where attendance tracking is required.

## Objectives

The goal of this project is to develop an intelligent attendance system using face recognition technology, helping to save time and improve accuracy in managing attendance for students or employees.

## Key Features

* **Face Recognition:** Identifies individuals based on their facial features.
* **Automatic Attendance:** Records the attendance of participants automatically.
* **Easy Deployment:** Provides configuration files and source code that are easy to use.
* **High Accuracy:** Uses modern deep learning algorithms to achieve high accuracy.

## Directory Structure

```
├── config/           # Configuration files for the system
├── dataset/          # Training data and sample images
├── haarcascade/      # Cascade files for face detection
├── model/            # Trained models
├── notebook/         # Jupyter Notebooks for training steps
├── scripts/          # Scripts to run the system
├── test/             # Source code for testing
```

## System Requirements

* Python 3.12+
* Libraries: `opencv`, `tensorflow`, `keras`, `numpy`, `matplotlib`, ...



## Model Evaluation

Classification Report: 
- The classification report shows the performance of the model for each student. The model achieved a perfect score across all metrics:

- Precision, Recall, and F1-Score: 1.00 for all classes (students), indicating that the model perfectly identified each student without any errors.

- Accuracy: The model achieved an accuracy of 100%, meaning it correctly identified every student in the test set.

Confusion Matrix: 
- The Confusion Matrix further confirms the model's excellent performance, with no misclassifications. 


## Real-World Evaluation Video
To showcase the real-world application of the model, below is a video demonstrating the attendance marking process using face recognition in action.

![Video](output/video.gif)

Note: Sorry my computer has a problem for filming, so I will shoot by my phone

## Web-based Attendance System Demo

[Video](output/web.gif)