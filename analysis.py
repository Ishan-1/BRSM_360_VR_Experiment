import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# --- 1. LOAD THE CONSOLIDATED DATA ---
# Using the master file created in the previous step
FILE_PATH = 'master_vr_movement_data.csv'

def run_comprehensive_analysis(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found. Please run the consolidation script first.")
        return

    # --- 2. DESCRIPTIVE STATISTICS ---
    # Focusing on the core psychomotor measure: Rotation Speed 
    desc_stats = df.groupby('Video_ID')['Summary_Avg_RotationSpeedTotal'].describe().round(2)
    desc_stats = desc_stats[['mean', 'std', 'min', 'max']]
    desc_stats.columns = ['Mean Speed', 'Std Dev', 'Min Speed', 'Max Speed']

    print("\n" + "="*60)
    print(" DESCRIPTIVE STATISTICS: AVERAGE ROTATIONAL SPEED (deg/sec) ")
    print("="*60)
    print(desc_stats.to_string())
    print("="*60)

    # --- 3. NORMALITY CHECKS (SHAPIRO-WILK) ---
    print("\n--- NORMALITY CHECKS (Shapiro-Wilk Test) ---")
    print("Hypothesis: Data is normally distributed (p > 0.05)")
    for video in df['Video_ID'].unique():
        data = df[df['Video_ID'] == video]['Summary_Avg_RotationSpeedTotal']
        shapiro_test = stats.shapiro(data)
        status = "Normal" if shapiro_test.pvalue > 0.05 else "NOT Normal"
        print(f"{video}: W={shapiro_test.statistic:.3f}, p-value={shapiro_test.pvalue:.4f} ({status})")

    # --- 4. VISUALIZATIONS ---
    sns.set_theme(style="whitegrid", context="talk")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

    # Plot A: Average Rotational Speed (Psychomotor Activation) 
    sns.boxplot(data=df, x='Video_ID', y='Summary_Avg_RotationSpeedTotal', 
                palette="viridis", ax=ax1, hue='Video_ID', legend=False)
    ax1.set_title('Distribution of Rotational Speed per Video', pad=20, fontweight='bold')
    ax1.set_ylabel('Mean Rotation Speed (deg/sec)')

    # Plot B: Exploration Range (SD of Yaw) 
    sns.boxplot(data=df, x='Video_ID', y='Summary_SD_Yaw_Y', 
                palette="rocket", ax=ax2, hue='Video_ID', legend=False)
    ax2.set_title('Spatial Exploration (SD of Yaw Position)', pad=20, fontweight='bold')
    ax2.set_ylabel('Standard Deviation (degrees)')

    plt.tight_layout()
    plt.savefig('VR_Behavioral_Analysis_Boxplots.png', dpi=300)
    print("\nVisualizations saved as 'VR_Behavioral_Analysis_Boxplots.png'.")
    plt.show()

if __name__ == "__main__":
    run_comprehensive_analysis(FILE_PATH)