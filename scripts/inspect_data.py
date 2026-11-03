from pathlib import Path
import hashlib

source = Path("data/raw/telco.csv")  # Your input path.
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
print("running")


import pandas as pd

df = pd.read_csv(source)
print(df.shape)
print(df.dtypes)
print(df["Churn"].value_counts(dropna=False))

# =====================================================================
# 3. CARDINALITY, DIMENSIONS & FIELD TYPES
# =====================================================================
rows_count, cols_count = df.shape
field_types = {col: str(dtype) for col, dtype in df.dtypes.items()}

# =====================================================================
# 4. TARGET BALANCE METRICS (CHURN PROFILE)
# =====================================================================
target_col = "Churn"
target_metrics = {}
if target_col in df.columns:
    counts = df[target_col].value_counts(dropna=False)
    proportions = df[target_col].value_counts(dropna=False, normalize=True)
    for val in counts.index:
            str_val = "Missing/NaN" if pd.isna(val) else str(val)
            target_metrics[str_val] = {
                "count": int(counts[val]),
                "proportion": float(proportions[val])
            }
else:
    target_metrics = {"error": f"Target matrix identifier field '{target_col}' not found in file columns."}
    
# =====================================================================
# 5. INTEGRITY TRACKING: IDENTITY RESOLUTION (CUSTOMER ID)
# =====================================================================
    
id_col = "customerID"
duplicate_ids_count = 0
if id_col in df.columns:
        # Number of rows containing a customerID that has already been registered
        duplicate_ids_count = int(df.duplicated(subset=[id_col]).sum())
else:
        duplicate_ids_count = -1 # Indicates field column missing entirely
