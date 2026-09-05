# SaEvoPro

## Structure-aware active learning for protein engineering

SaEvoPro is a structure-aware active-learning framework developed for iterative protein engineering. It integrates structure-aware protein representations from **SaProt** with experimentally measured fitness values and a top-layer regression model, and then uses active-learning acquisition strategies to nominate variants for the next round of experimental validation.

This repository accompanies the manuscript:

**Pan X. et al. _In situ biocatalysis of naringin in citrus juice for flavor remodeling: from bitterness to sweetness_.**

In this study, SaEvoPro was benchmarked on 21 public deep mutational scanning (DMS) datasets and was subsequently applied to the engineering of flavanone cleavage reductase **ErFCR** for simultaneous improvement of catalytic activity and acid adaptation.

---

## Overview

The original **EvolvePro** framework uses protein language model embeddings and a top-layer regression model to learn the relationship between protein variants and experimentally measured fitness.

SaEvoPro extends this strategy by introducing **structure-aware representations** into the active-learning workflow. The main workflow is:

1. Predict the wild-type protein structure using AlphaFold2.
2. Generate single-site mutant structures using PreMut.
3. Convert protein structures into structure-aware sequences for SaProt.
4. Extract structure-aware protein representations from SaProt.
5. Combine protein representations with experimentally measured activity or fitness values.
6. Train a top-layer regression model.
7. Rank unmeasured protein variants.
8. Select candidate variants using an active-learning acquisition strategy.
9. Experimentally evaluate the selected variants.
10. Feed the experimental measurements back into the model for the next iteration.

For ErFCR engineering, activity measured at **pH 5.5** was used as the low-pH proxy phenotype for model training, whereas activity at **pH 4.5** was used as a stringent secondary screen for identifying acid-adapted variants.

---

## Benchmarking

SaEvoPro was benchmarked using **21 publicly available DMS datasets** covering enzymes, binding proteins, regulatory proteins and viral proteins.

The following protein representation models were evaluated in the study:

- SaProt-35M-AF2
- SaProt-650M-PDB
- SaProt-650M-AF2
- SaProt-1.3B-AFDB-OMG-NCBI
- ESM-2 15B as a sequence-only control

SaProt-1.3B showed the best overall performance and was therefore selected as the structure-aware representation model used in SaEvoPro.

### Top-layer regression models

The following regression models were evaluated:

- ElasticNet
- Gaussian process
- GradientBoosting
- K-nearest neighbours (KNN)
- Lasso
- LightGBM
- Linear regression
- Neural network
- NGBoost
- Random forest
- CatBoost
- Ridge regression
- XGBoost

### Sampling and acquisition strategies

The following strategies were evaluated:

- diversity-based sampling
- random sampling
- Top-n sampling
- Top-n/bottom-n sampling

Random sampling strategies were repeated in **ten independent simulations**, whereas diversity-based sampling was performed once because it is deterministic.

In the benchmark described in the manuscript, **CatBoost combined with Top-n sampling** showed the highest overall performance.

---

## Application to ErFCR engineering

SaEvoPro was applied to engineer ErFCR for improved catalytic activity and acid adaptation.

The experimental campaign included **145 tested ErFCR variants**. Rounds 1–8 contained 16 single mutants per round, followed by combinatorial testing of 10 double mutants and 7 triple mutants.

Two optimized variants were obtained:

- **M1: W380P-A415K**
- **M2: I379D-W380P-A415K**

M1 showed improved acid adaptation, whereas M2 showed substantially enhanced catalytic efficiency.

---

## Installation

Clone this repository:

```bash
git clone https://github.com/panx82854-star/SaEvoPro.git
cd SaEvoPro
```

Install the Python environment using the provided environment file:

```bash
conda env create -f environment.yml
conda activate saevopro
pip install -e .
```

SaEvoPro relies on several external protein-modeling and protein-language-model tools. These tools should be installed separately according to their official instructions.

---

## External software and resources

SaEvoPro was developed using or building upon the following publicly available tools, models and codebases.

| Resource | Role in SaEvoPro | Repository / resource |
|---|---|---|
| **EvolvePro** | Active-learning framework and top-layer regression workflow | https://github.com/mat10d/EvolvePro |
| **SaProt** | Structure-aware protein language model and protein representations | https://github.com/westlake-repl/SaProt |
| **SaProt pretrained models** | Pretrained SaProt checkpoints | https://huggingface.co/SaProtHub |
| **PreMut** | Rapid prediction of single-site mutation-induced structural changes | https://github.com/jianlin-cheng/PreMut |
| **AlphaFold2** | Wild-type protein structure prediction | https://github.com/google-deepmind/alphafold |
| **ESM / ESM-2** | Sequence-only protein language model used as a control | https://github.com/facebookresearch/esm |
| **Foldseek** | Structure encoding / 3Di representation used in the SaProt workflow | https://github.com/steineggerlab/foldseek |
| **CatBoost** | Top-layer regression model used in the optimized SaEvoPro configuration | https://github.com/catboost/catboost |

Users should follow the original installation instructions, software licenses and citation requirements of each external project.

---

## Acknowledgements

SaEvoPro was developed by extending the active-learning concept and implementation provided by **EvolvePro** and by incorporating structure-aware protein representations from **SaProt**.

We gratefully acknowledge the authors and developers of **EvolvePro** for making their active-learning framework and source code publicly available. We also thank the developers of **SaProt**, **PreMut**, **AlphaFold2**, **ESM-2**, **Foldseek**, **CatBoost**, and the broader open-source protein-design and machine-learning communities for providing the software, pretrained models and computational resources that made this work possible.

We strongly encourage users of SaEvoPro to cite the original publications associated with these tools in addition to citing the SaEvoPro study.

---

## Data availability

The 21 DMS datasets used for benchmarking are publicly available from their original publications and repositories. The identities and references of these datasets are provided in the Supplementary Information of the associated manuscript.

Experimental ErFCR measurements supporting this study are provided in the associated manuscript and Supplementary Information.

---

## Code availability

The SaEvoPro source code and related analysis scripts are provided in this repository:

**https://github.com/panx82854-star/SaEvoPro**

---

## Citation

If you use SaEvoPro, please cite:

```text
Pan X. et al.
In situ biocatalysis of naringin in citrus juice for flavor remodeling:
from bitterness to sweetness.
```

The complete publication information will be updated after publication.

---

## Contact

For questions related to SaEvoPro or the associated study, please contact the corresponding authors listed in the manuscript.
