import pandas as pd
import numpy as np

# Read the CSV files
hsi_data = pd.read_csv("/Users/eliyoung/Desktop/Egg data/csvs/HSI_egg_data.csv")
spectra_data = pd.read_csv("/Users/eliyoung/Desktop/Egg data/csvs/spectra and reference parameters.csv")

def calculate_match_score(row, spectra_row):
    """Calculate a match score between two rows based on multiple criteria."""
    score = 0
    max_score = 0
    
    # Mass matching (weight: 4) - more relaxed threshold
    mass_diff = abs(row['Mass (g)'] - spectra_row['Mass (g)'])
    if mass_diff <= 0.5:  # Relaxed threshold for mass
        score += 4
    elif mass_diff <= 1.0:
        score += 2
    max_score += 4
    
    # Major diameter matching (weight: 2) - more relaxed
    major_diff = abs(row['Major dia. (mm)'] - spectra_row['Major dia (mm)'])
    if major_diff <= 0.5:  # Relaxed tolerance
        score += 2
    elif major_diff <= 1.0:
        score += 1
    max_score += 2
    
    # Minor diameter matching (weight: 2) - more relaxed
    minor_diff = abs(row['Minor dia. (mm)'] - spectra_row['Minor dia (mm)'])
    if minor_diff <= 0.5:  # Relaxed tolerance
        score += 2
    elif minor_diff <= 1.0:
        score += 1
    max_score += 2
    
    # Fertility status matching (weight: 2) - must match exactly
    if row['Fertility status'] == spectra_row['Fertility status']:
        score += 2
    max_score += 2
    
    return score / max_score

def find_all_potential_matches(hsi_df, spectra_df):
    """Find all potential matches between HSI and Spectra data."""
    potential_matches = []
    
    for _, hsi_row in hsi_df.iterrows():
        if pd.isna(hsi_row['Mass (g)']) or pd.isna(hsi_row['Major dia. (mm)']) or pd.isna(hsi_row['Minor dia. (mm)']):
            continue
            
        for _, spectra_row in spectra_df.iterrows():
            # Skip if mass difference is too large (>1.0g)
            if abs(hsi_row['Mass (g)'] - spectra_row['Mass (g)']) > 1.0:
                continue
                
            score = calculate_match_score(hsi_row, spectra_row)
            if score >= 0.9:  # Accept matches with score >= 0.9
                potential_matches.append({
                    'HSI_ID': hsi_row['HSI sample ID'],
                    'Spectra_ID': spectra_row['Sample ID'],
                    'Score': score,
                    'Mass_Diff': abs(hsi_row['Mass (g)'] - spectra_row['Mass (g)']),
                    'Major_Dia_Diff': abs(hsi_row['Major dia. (mm)'] - spectra_row['Major dia (mm)']),
                    'Minor_Dia_Diff': abs(hsi_row['Minor dia. (mm)'] - spectra_row['Minor dia (mm)']),
                    'HSI_Row': hsi_row,
                    'Spectra_Row': spectra_row
                })
    
    # Sort potential matches by score (highest first), then by mass difference
    potential_matches.sort(key=lambda x: (-x['Score'], x['Mass_Diff']))
    return potential_matches

def create_consolidated_row(hsi_row, spectra_row, score):
    """Create a consolidated row from HSI and Spectra data."""
    return {
        # HSI data
        'HSI_ID': hsi_row['HSI sample ID'],
        'Date': hsi_row['Date'],
        'Exp_No': hsi_row['Exp. No.'],
        'Gender': hsi_row['Gender'],
        'HSI_Fertility': hsi_row['Fertility status'],
        'Mortality_Status': hsi_row['Mortality status'],
        'HSI_Mass': hsi_row['Mass (g)'],
        'HSI_Major_Dia': hsi_row['Major dia. (mm)'],
        'HSI_Minor_Dia': hsi_row['Minor dia. (mm)'],
        'Comment': hsi_row['Comment'],
        
        # Spectra data
        'Spectra_ID': spectra_row['Sample ID'],
        'Spectra_Mass': spectra_row['Mass (g)'],
        'Spectra_Major_Dia': spectra_row['Major dia (mm)'],
        'Spectra_Minor_Dia': spectra_row['Minor dia (mm)'],
        'Spectra_Fertility': spectra_row['Fertility status'],
        'Thickness': spectra_row['Thickness (mm)'],
        'Yolk_Mass': spectra_row['Yolk mass (g)'],
        'Shell_Strength': spectra_row['Shell strength (N)'],
        
        # Match quality
        'Match_Score': score,
        
        # Verification metrics
        'Mass_Difference': abs(hsi_row['Mass (g)'] - spectra_row['Mass (g)']),
        'Major_Dia_Difference': abs(hsi_row['Major dia. (mm)'] - spectra_row['Major dia (mm)']),
        'Minor_Dia_Difference': abs(hsi_row['Minor dia. (mm)'] - spectra_row['Minor dia (mm)'])
    }

# Find all potential matches
potential_matches = find_all_potential_matches(hsi_data, spectra_data)

# Create sets to track used IDs
used_hsi_ids = set()
used_spectra_ids = set()

# Create list to store final matches
final_matches = []

# Process potential matches in order of score and mass difference
for match in potential_matches:
    hsi_id = match['HSI_ID']
    spectra_id = match['Spectra_ID']
    
    # Skip if either ID has already been used
    if hsi_id in used_hsi_ids or spectra_id in used_spectra_ids:
        continue
    
    # Add IDs to used sets
    used_hsi_ids.add(hsi_id)
    used_spectra_ids.add(spectra_id)
    
    # Create consolidated row
    consolidated_row = create_consolidated_row(match['HSI_Row'], match['Spectra_Row'], match['Score'])
    
    # Add spectral data
    for col in spectra_data.columns:
        if col.startswith('3') or col.startswith('4') or col.startswith('5') or col.startswith('6') or col.startswith('7') or col.startswith('8') or col.startswith('9'):
            consolidated_row[f'Spectrum_{col}'] = match['Spectra_Row'][col]
    
    final_matches.append(consolidated_row)

# Create DataFrame and save to CSV
final_matches_df = pd.DataFrame(final_matches)
final_matches_df.to_csv('one_to_one/relaxed_matches.csv', index=False)

# Print summary
print(f"Total HSI samples: {len(hsi_data)}")
print(f"Total Spectra samples: {len(spectra_data)}")
print(f"Total potential matches found (score >= 0.9): {len(potential_matches)}")
print(f"Final one-to-one matches: {len(final_matches_df)}")

print("\nMatch score distribution:")
print(final_matches_df['Match_Score'].describe())

print("\nPhysical measurement differences:")
print("\nMass differences (g):")
print(final_matches_df['Mass_Difference'].describe())
print("\nMajor diameter differences (mm):")
print(final_matches_df['Major_Dia_Difference'].describe())
print("\nMinor diameter differences (mm):")
print(final_matches_df['Minor_Dia_Difference'].describe())

print("\nFirst few matches:")
print(final_matches_df[['HSI_ID', 'Spectra_ID', 'Match_Score', 'HSI_Mass', 'Spectra_Mass', 'Mass_Difference']].head().to_string()) 