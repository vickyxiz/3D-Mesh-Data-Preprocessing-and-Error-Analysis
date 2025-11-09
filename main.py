import trimesh
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import os
import scipy.spatial
import trimesh.transformations
import csv
def normalize_min_max(vertices):
    v_min = vertices.min(axis=0)
    v_max = vertices.max(axis=0)
    v_range = v_max - v_min
    v_range[v_range == 0] = 1e-6
    normalized = (vertices - v_min) / v_range
    return normalized, v_min, v_max

def denormalize_min_max(normalized_vertices, v_min, v_max):
    v_range = v_max - v_min
    reconstructed = (normalized_vertices * v_range) + v_min
    return reconstructed

def normalize_unit_sphere(vertices):
    centroid = vertices.mean(axis=0)
    centered_vertices = vertices - centroid
    scale = np.max(np.linalg.norm(centered_vertices, axis=1))
    if scale == 0:
        scale = 1.0
    normalized = centered_vertices / scale
    return normalized, centroid, scale

def denormalize_unit_sphere(normalized_vertices, centroid, scale):
    reconstructed = (normalized_vertices * scale) + centroid
    return reconstructed


def quantize(vertices, bins):
    quantized = np.floor(vertices * (bins - 1)).astype(int)
    return quantized

def dequantize(quantized_vertices, bins):
    dequantized = quantized_vertices.astype(float) / (bins - 1)
    return dequantized

def calculate_error(original, reconstructed):
    squared_errors = np.sum((original - reconstructed)**2, axis=1)
    mse = np.mean(squared_errors)
    return mse

def plot_error_distribution(errors_min_max, errors_unit_sphere, title, save_path=None):
    plt.figure(figsize=(12, 6))
    plt.hist(errors_min_max, bins=50, alpha=0.5, label='Min-Max Error', color='blue')
    plt.hist(errors_unit_sphere, bins=50, alpha=0.5, label='Unit Sphere Error', color='red')
    plt.title(f'Error Distribution for {title}')
    plt.xlabel('Per-Vertex Squared Error')
    plt.ylabel('Number of Vertices')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def plot_error_per_axis(original, reconstructed, title, save_path=None):
    errors = (original - reconstructed) ** 2
    plt.figure(figsize=(6, 4))
    plt.bar(['X', 'Y', 'Z'], errors.mean(axis=0), color=['r','g','b'])
    plt.title(f'Mean Squared Error per Axis - {title}')
    plt.ylabel('MSE')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def visualize_error_heatmap(vertices, errors, title):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(vertices)
    norm_errors = (errors - errors.min()) / (errors.max() - errors.min() + 1e-9)
    colors = np.zeros((len(vertices), 3))
    colors[:, 0] = norm_errors
    colors[:, 1] = 1 - norm_errors
    pcd.colors = o3d.utility.Vector3dVector(colors)
    print(f"Displaying 3D Error Heatmap for {title}...")
    o3d.visualization.draw_geometries([pcd], window_name=title)

BIN_SIZE = 1024
SAMPLES_DIR = "8samples"
PLOTS_DIR = "plots"
RESULTS_CSV = "results_summary.csv"

def process_and_plot_all_samples():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    results = []

    obj_files = [f for f in os.listdir(SAMPLES_DIR) if f.endswith(".obj")]
    for obj_file in obj_files:
        mesh_path = os.path.join(SAMPLES_DIR, obj_file)
        print(f"\n=== Processing {obj_file} ===")
        try:
            mesh = trimesh.load(mesh_path, process=False)
        except Exception as e:
            print(f"❌ Failed to load {obj_file}: {e}")
            continue

        vertices = mesh.vertices
        if vertices.shape[0] == 0:
            print(f"⚠️ Skipping {obj_file}: No vertices found.")
            continue

        print("   --- Task 1: Original Stats ---")
        print(f"   > Vertices: {vertices.shape[0]}")
        print(f"   >   Min:   {np.round(vertices.min(axis=0), 3)}")
        print(f"   >   Max:   {np.round(vertices.max(axis=0), 3)}")
        print(f"   >   Mean:  {np.round(vertices.mean(axis=0), 3)}")
        print(f"   >   Std:   {np.round(vertices.std(axis=0), 3)}")

        print("   --- Task 2/3: Processing ---")
        
        norm_min_max, v_min, v_max = normalize_min_max(vertices)
        quant_min_max = quantize(norm_min_max, BIN_SIZE)
        recon_min_max = denormalize_min_max(dequantize(quant_min_max, BIN_SIZE), v_min, v_max)
        mse_min_max = calculate_error(vertices, recon_min_max)
        errors_min_max = np.sum((vertices - recon_min_max)**2, axis=1)

        trimesh.Trimesh(vertices=norm_min_max, faces=mesh.faces).export(os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_norm_minmax.obj"))
        trimesh.Trimesh(vertices=quant_min_max, faces=mesh.faces).export(os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_quant_minmax.obj"))


        norm_us, centroid, scale = normalize_unit_sphere(vertices)
        norm_us_01 = (norm_us + 1.0) / 2.0
        quant_us = quantize(norm_us_01, BIN_SIZE)
        recon_us = denormalize_unit_sphere((dequantize(quant_us, BIN_SIZE) * 2.0) - 1.0, centroid, scale)
        mse_us = calculate_error(vertices, recon_us)
        errors_us = np.sum((vertices - recon_us)**2, axis=1)

        trimesh.Trimesh(vertices=norm_us, faces=mesh.faces).export(os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_norm_unitsphere.obj"))
        trimesh.Trimesh(vertices=quant_us, faces=mesh.faces).export(os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_quant_unitsphere.obj"))


        trimesh.Trimesh(vertices=recon_min_max, faces=mesh.faces).export(os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_recon_minmax.obj"))
        trimesh.Trimesh(vertices=recon_us, faces=mesh.faces).export(os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_recon_unitsphere.obj"))

        plot_error_distribution(errors_min_max, errors_us, obj_file, save_path=os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_error_dist.png"))
        plot_error_per_axis(vertices, recon_min_max, f"{obj_file} - MinMax", save_path=os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_axis_minmax.png"))
        plot_error_per_axis(vertices, recon_us, f"{obj_file} - UnitSphere", save_path=os.path.join(PLOTS_DIR, f"{obj_file.replace('.obj','')}_axis_unitsphere.png"))

        results.append([obj_file, mse_min_max, mse_us])

        print(f"✅ {obj_file}: MSE Min-Max={mse_min_max:.8e}, UnitSphere={mse_us:.8e}")
    with open(RESULTS_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Mesh", "MSE_MinMax", "MSE_UnitSphere"])
        writer.writerows(results)

    print(f"\n✅ All meshes processed. Results saved to '{RESULTS_CSV}' and plots to '{PLOTS_DIR}/'.")


def create_transformed_mesh(mesh):
    translation = np.random.rand(3) * 10.0
    rotation = trimesh.transformations.random_rotation_matrix()
    transform_matrix = trimesh.transformations.translation_matrix(translation) @ rotation
    transformed_mesh = mesh.copy()
    transformed_mesh.apply_transform(transform_matrix)
    print("   > Generated transformed mesh (rotation + translation).")
    return transformed_mesh.vertices

def quantize_adaptive(vertices, bins_array):
    return np.floor(vertices * (bins_array - 1)).astype(int)

def dequantize_adaptive(quantized_vertices, bins_array):
    return quantized_vertices.astype(float) / (bins_array - 1)

def get_adaptive_bins(vertices_01, base_bins=1024, dense_bins=2048):
    print("   > Analyzing vertex density (KDTree)...")
    tree = scipy.spatial.KDTree(vertices_01)
    neighbor_counts = tree.query_ball_point(vertices_01, r=0.05, return_length=True)
    dense_threshold = np.percentile(neighbor_counts, 75)
    bins_array = np.full((len(vertices_01), 1), base_bins, dtype=int)
    bins_array[neighbor_counts > dense_threshold] = dense_bins
    print(f"   > Dense: {np.sum(bins_array==dense_bins)} | Base: {np.sum(bins_array==base_bins)}")
    return bins_array

def run_full_pipeline(vertices, uniform_bins, use_adaptive=False):
    norm_vertices, centroid, scale = normalize_unit_sphere(vertices)
    norm_vertices_01 = (norm_vertices + 1.0) / 2.0
    if use_adaptive:
        adaptive_bins = get_adaptive_bins(norm_vertices_01, base_bins=uniform_bins)
        quantized = quantize_adaptive(norm_vertices_01, adaptive_bins)
        dequantized_01 = dequantize_adaptive(quantized, adaptive_bins)
    else:
        quantized = quantize(norm_vertices_01, uniform_bins)
        dequantized_01 = dequantize(quantized, uniform_bins)
    dequantized = (dequantized_01 * 2.0) - 1.0
    reconstructed = denormalize_unit_sphere(dequantized, centroid, scale)
    mse = calculate_error(vertices, reconstructed)
    return mse

def run_bonus_task():
    print("\n=== 🚀 BONUS TASK (Option 2): Adaptive Quantization ===")
    FILE = os.path.join(SAMPLES_DIR, "girl.obj")
    mesh = trimesh.load(FILE, process=False)
    original_vertices = mesh.vertices
    transformed_vertices = create_transformed_mesh(mesh)

    mse_uniform_orig = run_full_pipeline(original_vertices, uniform_bins=1024, use_adaptive=False)
    mse_adaptive_orig = run_full_pipeline(original_vertices, uniform_bins=1024, use_adaptive=True)
    mse_uniform_trans = run_full_pipeline(transformed_vertices, uniform_bins=1024, use_adaptive=False)
    mse_adaptive_trans = run_full_pipeline(transformed_vertices, uniform_bins=1024, use_adaptive=True)

    print("\n--- Final Results ---")
    print("---------------------------------------------------------------")
    print("| Pipeline         | MSE Original Mesh | MSE Transformed Mesh |")
    print("|------------------|------------------:|----------------------:|")
    print(f"| Uniform (1024)   | {mse_uniform_orig:.10f} | {mse_uniform_trans:.10f} |")
    print(f"| Adaptive (2048)  | {mse_adaptive_orig:.10f} | {mse_adaptive_trans:.10f} |")
    print("---------------------------------------------------------------")

    diff = abs(mse_uniform_orig - mse_uniform_trans)
    improvement = (mse_uniform_orig - mse_adaptive_orig) / mse_uniform_orig * 100
    print(f"\nAnalysis:")
    print(f" • Invariance difference: {diff:.10f}")
    print(f" • Adaptive quantization improvement: {improvement:.2f}%")
    print("✅ Bonus Task Completed.")

if __name__ == "__main__":
    print("=== 📊 RUNNING TASKS 1–3 FOR ALL SAMPLES ===")
    process_and_plot_all_samples()
    run_bonus_task()
