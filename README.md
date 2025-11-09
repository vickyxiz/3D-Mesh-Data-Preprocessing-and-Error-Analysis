# 3D-Mesh-Data-Preprocessing-and-Error-Analysis
🧠 3D Mesh Normalization, Quantization, and Error Analysis

This project implements a 3D mesh data preprocessing pipeline for the SeamGPT data processing assignment.
It covers the full workflow — from loading mesh data to normalization, quantization, reconstruction, and error analysis — and includes a bonus adaptive quantization task for rotation and translation invariance.

📂 Project Structure
Mesh_Preprocessing_Assignment_VigneshV/
│
├── main.py                    # Main Python script for all tasks (1–3) + Bonus Task
├── 8samples/                  # Folder containing input .obj meshes
├── plots/                     # Output folder for meshes and plots (auto-generated)
├── results_summary.csv        # CSV file summarizing MSE results
├── report.pdf                 # Final analysis report
└── README.md                  # This file

⚙️ Setup Instructions
1. Prerequisites

Ensure you have Python 3.8+ installed.

2. Install Required Libraries

Run the following command in your terminal or command prompt:

pip install numpy trimesh open3d matplotlib scipy

▶️ How to Run the Code

Place all your .obj sample meshes inside the folder:

8samples/


Run the main script:

python main.py


The program will:

Load and inspect all meshes (Task 1)

Apply normalization and quantization (Task 2)

Reconstruct and compute error metrics (Task 3)

Perform adaptive quantization (Bonus Task)

Save results to:

plots/ → output meshes and visualizations

results_summary.csv → summary of MSE values

Check the console output for progress and MSE comparisons.

📊 Generated Outputs
File / Folder	Description
plots/	Contains normalized, quantized, and reconstructed meshes (.obj) and plots (.png)
results_summary.csv	Table of Mean Squared Error (MSE) for each normalization method
report.pdf	Final written analysis and results summary
main.py	Core implementation file for all tasks
🧩 Implemented Tasks
Task 1 – Mesh Loading and Inspection

Loads all .obj files from 8samples/

Extracts and prints vertex statistics (min, max, mean, std)

Task 2 – Normalization and Quantization

Implements:

Min–Max Normalization

Unit Sphere Normalization

Quantizes vertices to 1024 discrete bins

Saves normalized and quantized meshes for comparison

Task 3 – Reconstruction and Error Analysis

Dequantizes and denormalizes meshes

Computes Mean Squared Error (MSE) between original and reconstructed vertices

Generates:

Error distribution histograms

Per-axis error plots (X, Y, Z)

Reconstructed mesh outputs

Bonus Task – Adaptive Quantization (Option 2)

Computes vertex density using KDTree

Applies adaptive bin sizes (2048 for dense regions, 1024 otherwise)

Evaluates rotation and translation invariance

Compares reconstruction accuracy between uniform and adaptive quantization

📈 Key Observations

Unit Sphere Normalization produced the lowest reconstruction error.

Min–Max Normalization worked well but was slightly sensitive to uneven scales.

Adaptive Quantization improved MSE by ~20% and enhanced robustness to transformations.

Overall reconstruction quality was high with MSE ≈ 10⁻⁶ – 10⁻⁴.

🧰 Technologies Used
Parameter	Description
Programming Language	Python 3
Libraries	NumPy, Trimesh, Open3D, Matplotlib, SciPy
Input Files	8 sample .obj meshes
Quantization Bins	1024
Output Files	Normalized, quantized, and reconstructed .obj meshes
Hardware	CPU only (no GPU required)
