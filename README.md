# 3D Mesh Normalization, Quantization, and Error Analysis

This project implements a 3D mesh data preprocessing pipeline for the SeamGPT data processing assignment.

It covers the full workflow — from loading mesh data to normalization, quantization, reconstruction, and error analysis — and includes a bonus adaptive quantization task for rotation and translation invariance.

---

## 📂 Project Structure


```text
Mesh_Preprocessing_Assignment_VigneshV/
│
├── main.py                    # Main Python script for all tasks (1–3) + Bonus Task
├── 8samples/                  # Folder containing input .obj meshes
├── plots/                     # Output folder for meshes and plots (auto-generated)
├── results_summary.csv        # CSV file summarizing MSE results
├── report.pdf                 # Final analysis report
└── README.md                  # This file
```

---

## ⚙️ Setup Instructions

### 🧩 Prerequisites
Ensure **Python 3.8+** is installed on your system.

### 📦 Install Dependencies
Run the following command:
```bash
pip install numpy trimesh open3d matplotlib scipy
```
▶️ How to Run the Code
Place all your .obj sample meshes inside the 8samples/ folder.

Run the main script from your terminal:
```bash
python main.py
```
The program will execute all tasks and:

- 🟢 **Load and inspect all meshes (Task 1)**
- 🟡 **Apply normalization and quantization (Task 2)**
- 🔵 **Reconstruct and compute error metrics (Task 3)**
- 🟣 **Perform adaptive quantization (Bonus Task)**
Outputs will be saved to:

- 📁 **plots/** → Output meshes and visualizations  
- 📊 **results_summary.csv** → Summary of MSE values  

💡 Check the console output for progress and final MSE comparisons.
## 📊 Generated Outputs  

| File / Folder | Description |
|----------------|-------------|
| **plots/** | Contains normalized, quantized, and reconstructed meshes (`.obj`) and plots (`.png`) |
| **results_summary.csv** | Table of Mean Squared Error (MSE) for each normalization method |
| **report.pdf** | Final written analysis and results summary |
| **main.py** | Core implementation file for all tasks |
## 🧩 Implemented Tasks

### 🔹 Task 1 – Mesh Loading and Inspection
- Loads all `.obj` files from the **8samples/** directory  
- Extracts and prints vertex statistics (**min, max, mean, std**)

---

### 🔹 Task 2 – Normalization and Quantization
Implements two normalization methods:
- **Min–Max Normalization**
- **Unit Sphere Normalization**

Additional steps:
- Quantizes vertices to **1024 discrete bins**  
- Saves normalized and quantized meshes for comparison

---

### 🔹 Task 3 – Reconstruction and Error Analysis
- Dequantizes and denormalizes meshes to reconstruct them  
- Computes the **Mean Squared Error (MSE)** between original and reconstructed vertices  
- Generates:
  - 📈 **Error distribution histograms**
  - 📊 **Per-axis error plots (X, Y, Z)**
  - 💾 **Reconstructed mesh output files**

---

### 🔹 Bonus Task – Adaptive Quantization (Option 2)
- Computes vertex density using a **KDTree**  
- Applies **adaptive bin sizes** (e.g., `2048` bins for dense regions, `1024` otherwise)  
- Evaluates **rotation and translation invariance**  
- Compares reconstruction accuracy between **uniform** and **adaptive quantization**
## 📈 Key Observations

- 🟢 **Unit Sphere Normalization** consistently produced the **lowest reconstruction error**.  
- 🟡 **Min–Max Normalization** worked well but was slightly more sensitive to **meshes with uneven scales**.  
- 🟣 **Adaptive Quantization** successfully improved the **MSE by approximately 20%** compared to uniform quantization and enhanced **robustness to transformations**.  
- ⚪ **Overall reconstruction quality** was high, with **MSE values generally in the range of 10⁻⁶ – 10⁻⁴**.

