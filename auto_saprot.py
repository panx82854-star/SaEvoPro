
from evolvepro.src.evolve import evolve_experimental, evolve_experimental_multi

protein_name = 'zika'
embeddings_base_path = '/mnt/data/EvolvePro-main/data_embeddings/zika_saprot_650M_PDB.csv'
embeddings_file_name = 'zika_saprot_650M_PDB.csv'
round_base_path = '/mnt/data/EvolvePro-main/Process/Zika/round2'
wt_fasta_path = "/mnt/data/EvolvePro-main/Process/Zika/dataset_WT.fasta"
number_of_variants = 16
output_dir = '/mnt/data/EvolvePro-main/Process/Zika/round10'

# Single variant
round_name = 'Round2'
round_file_names = ['Round2.xlsx']
rename_WT = True

evolve_experimental(
    protein_name,
    round_name,
    embeddings_base_path,
    embeddings_file_name,
    round_base_path,
    round_file_names,
    wt_fasta_path,
    rename_WT,
    number_of_variants,
    output_dir
)