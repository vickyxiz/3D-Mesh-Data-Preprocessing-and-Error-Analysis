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
python main.py
