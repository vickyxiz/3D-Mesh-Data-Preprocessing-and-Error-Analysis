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
▶️ Running the Project

Place your .obj meshes inside the folder:

8samples/


Run the main script:

python main.py
The program will automatically:

Load and inspect all meshes (Task 1)

Apply normalization and quantization (Task 2)

Reconstruct meshes and compute error metrics (Task 3)

Perform adaptive quantization (Bonus Task)

Save results to:

plots/ → normalized, quantized, and reconstructed meshes + plots

results_summary.csv → summary of Mean Squared Error (MSE)
