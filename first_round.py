import os
import pandas as pd
from evolvepro.src.model2 import first_round

# =========================

embedding_path = "/mnt/data/EvolvePro-main/data_embeddings/Zika_saprot_650M_PDB.csv"


base_name = os.path.basename(embedding_path)             
protein_name = base_name.split("_")[0]                

# =========================

embeddings = pd.read_csv(embedding_path, index_col=0)

# =========================

try:
    labels = pd.read_csv("labels.csv")
    assert "variant" in labels.columns
except Exception:
    labels = pd.DataFrame({"variant": embeddings.index})

# =========================

labels0, iter0, this_round_variants = first_round(
    labels=labels,
    embeddings=embeddings,
    explicit_variants=None,
    num_mutants_per_round=16,
    first_round_strategy="diverse_medoids",
    embedding_type=None,
    random_seed=3407
)



output_dir = "data/base"
os.makedirs(output_dir, exist_ok=True)


round0_path = os.path.join(output_dir, f"round0_{protein_name}.csv")
variant_path = os.path.join(output_dir, f"round0_{protein_name}_variants.txt")


iter0.to_csv(round0_path, index=False)
pd.Series(this_round_variants).to_csv(variant_path, index=False, header=False)

print(f"✔ 已保存: {round0_path}")
print(f"✔ 已保存: {variant_path}")
print(iter0.head())
