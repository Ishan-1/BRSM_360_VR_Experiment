import pandas as pd
import numpy as np
import os

# --- CONFIGURATION ---
# Use raw strings (r'') to avoid Windows path errors
BASE_PATH = r'C:\Users\Kunal Angadi\Downloads\360 Videos VR project\data\headtracking-data'
OUTPUT_FILE = 'master_vr_movement_data.csv'

def collapse_vr_dataset(base_directory):
    master_list = []
    # Video folders as defined in the apparatus [cite: 8]
    video_folders = ['v1', 'v2', 'v3', 'v4', 'v5']
    
    print(f"Starting collapse of files from: {base_directory}")

    for folder in video_folders:
        folder_path = os.path.join(base_directory, folder)
        if not os.path.exists(folder_path):
            print(f"Skipping {folder}: Path not found.")
            continue
            
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        for file in files:
            file_path = os.path.join(folder_path, file)
            
            try:
                # 1. Load movement data (skip the summary row to avoid ParserError)
                # This covers columns like RotationSpeedTotal and PositionChange 
                df_raw = pd.read_csv(file_path, skipfooter=1, engine='python')
                
                # Calculate mean of all movement columns (excluding Time)
                movement_means = df_raw.drop(columns=['Time']).mean().to_dict()
                movement_means = {f"Mean_{k}": v for k, v in movement_means.items()}

                # 2. Extract specific behavioral measures from the summary row 
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    if not lines: continue
                    last_line = lines[-1].split(',')
                
                # Mapping indices based on your CSV structure:
                # index 1-3: Circular Averages (X,Y,Z) [cite: 14]
                # index 5-7: Standard Deviations (X,Y,Z) [cite: 14]
                # index 12: Rotation Speed Total Average [cite: 6]
                entry = {
                    'Full_CSV_Name': file, # Entire CSV name as requested
                    'Video_ID': folder.upper(),
                    **movement_means,
                    'Summary_Avg_Pitch_X': float(last_line[1]),
                    'Summary_Avg_Yaw_Y': float(last_line[2]),
                    'Summary_Avg_Roll_Z': float(last_line[3]),
                    'Summary_SD_Pitch_X': float(last_line[5]),
                    'Summary_SD_Yaw_Y': float(last_line[6]),
                    'Summary_SD_Roll_Z': float(last_line[7]),
                    'Summary_Avg_RotationSpeedTotal': float(last_line[12])
                }
                master_list.append(entry)
            except Exception as e:
                print(f"Error processing {file}: {e}")

    # Create the master DataFrame
    master_df = pd.DataFrame(master_list)
    
    # Save to CSV
    master_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSuccess! Consolidated {len(master_df)} records into: {OUTPUT_FILE}")
    return master_df

if __name__ == "__main__":
    collapse_vr_dataset(BASE_PATH)