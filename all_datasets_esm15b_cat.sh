#!/bin/bash
export PYTHONPATH=/mnt/data/EvolvePro-main
DATASETS=( "pafa" "Pafa" "B3VI55" "cas12f" "cov2" "GB1" "AVGFP" "BG" "HAH1" "HSP90" "KKA2" "TEM1" "zika" "TP53" "PTEN" "YAP1" "MAPK1_2" "MAPK1" "infa_pdb" "infa" "HSP90" "HIV" "H3N2" "GPCR" "AMIE"  )
BASE_CMD="python /mnt/data/EvolvePro-main/scripts/dms/dms_main2.py"

for NAME in "${DATASETS[@]}"; do
  echo "🚀 开始运行数据集: $NAME"

  $BASE_CMD \
    --dataset_name "$NAME" \
    --experiment_name "catboost" \
    --model_name "esm2_15B" \
    --embeddings_path "/mnt/data/EvolvePro-main/data_embeddings" \
    --labels_path "/mnt/data/EvolvePro-main/data_labels" \
    --num_simulations 1 \
    --num_iterations 10 \
    --measured_var "activity" \
    --learning_strategies "topn" \
    --num_mutants_per_round 16 \
    --num_final_round_mutants 16 \
    --first_round_strategies "diverse_medoids" \
    --embedding_types embeddings \
    --regression_types "catboost" \
    --embeddings_file_type csv \
    --output_dir "/mnt/data/EvolvePro-main/dms_output_paper"

  echo "✅ 完成: $NAME"
  echo "--------------------------------------------"
done
