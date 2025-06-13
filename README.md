# Egg Data Matching Process

This repository contains scripts and data for matching egg samples between two datasets: HSI (Hyperspectral Imaging) data and Spectra data.

## Data Files

The matching process produces two main output files:

1. `strict_matches.csv`: Contains perfect matches (score = 1.0) with strict measurement tolerances
2. `relaxed_matches.csv`: Contains matches with score ≥ 0.9 and more relaxed measurement tolerances

## Matching Criteria

The matching process uses the following criteria to identify corresponding eggs:

### Strict Matching (strict_matches.csv)
- Mass difference ≤ 0.2g
- Major diameter difference ≤ 0.2mm
- Minor diameter difference ≤ 0.2mm
- Fertility status must match exactly
- One-to-one matching (no duplicates)

### Relaxed Matching (relaxed_matches.csv)
- Mass difference ≤ 1.0g
- Major diameter difference ≤ 1.0mm
- Minor diameter difference ≤ 1.0mm
- Fertility status must match exactly
- One-to-one matching (no duplicates)

### Scoring System
Each potential match is scored based on:
- Mass matching (40% of total score)
  - Strict: Must be within 0.2g
  - Relaxed: Within 0.5g (full points) or 1.0g (partial points)
- Major diameter matching (20% of total score)
  - Strict: Must be within 0.2mm
  - Relaxed: Within 0.5mm (full points) or 1.0mm (partial points)
- Minor diameter matching (20% of total score)
  - Strict: Must be within 0.2mm
  - Relaxed: Within 0.5mm (full points) or 1.0mm (partial points)
- Fertility status matching (20% of total score)
  - Must match exactly to receive points

## Results

### Strict Matches (strict_matches.csv)
- 157 pairs with 100% confidence (score = 1.0)
- Mass differences:
  - Mean: 0.060g
  - Maximum: 0.200g
  - 25% of matches have zero mass difference
- Diameter differences:
  - Major diameter: mean 0.090mm, max 0.200mm
  - Minor diameter: mean 0.093mm, max 0.200mm
- Estimated correctness: 90-95%

### Relaxed Matches (relaxed_matches.csv)
- 395 total pairs (score ≥ 0.9)
- Mass differences:
  - Mean: 0.090g
  - Maximum: 0.500g
  - 50% of matches have zero mass difference
- Diameter differences:
  - Major diameter: mean 0.283mm, max 1.000mm
  - Minor diameter: mean 0.270mm, max 0.900mm
- Estimated correctness: 70-80%

## Example Matches

Perfect matches from strict_matches.csv:
```
HSI_ID         Spectra_ID         HSI_Mass  Spectra_Mass  Mass_Difference
Egg-036.bil    Egg-F-03Feb-0592'  65.9      65.9          0.0
Egg-061.bil    Egg-F-12Dec-0278'  61.2      61.2          0.0
Egg-073.bil    Egg-F-06Dec-0187'  62.3      62.3          0.0
Egg-075.bil    Egg-F-23Jan-0431'  63.2      63.2          0.0
Egg-094.bil    Egg-F-29Jan-0522'  65.2      65.2          0.0
```

## Data Sources

The matching process uses two input files:
1. HSI data: `/Users/eliyoung/Desktop/Egg data/csvs/HSI_egg_data.csv`
2. Spectra data: `/Users/eliyoung/Desktop/Egg data/csvs/spectra and reference parameters.csv`

## Process

1. The scripts read both HSI and Spectra data files
2. For each HSI sample, they:
   - Filter out samples with missing measurements
   - Find potential matches based on the scoring system
   - Apply one-to-one matching constraint
   - Sort matches by quality and mass difference
3. Create two output files:
   - `strict_matches.csv`: Contains only perfect matches with strict tolerances
   - `relaxed_matches.csv`: Contains matches with relaxed tolerances (score ≥ 0.9)

## Quality Assurance

The matching process ensures high confidence in matches by:
1. Using one-to-one matching to prevent duplicates
2. Requiring exact fertility status matches
3. Considering multiple physical measurements (mass and diameters)
4. Using a weighted scoring system to evaluate match quality
5. Providing both strict and relaxed matching options for different use cases 