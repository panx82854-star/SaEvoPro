# SaEvoPro

## Structure-aware active learning for protein engineering

SaEvoPro is a structure-aware active-learning framework developed for iterative protein engineering. It integrates structure-aware protein representations from **SaProt** with experimentally measured fitness values and a top-layer regression model, and then uses active-learning acquisition strategies to nominate variants for the next round of experimental validation.

In this study, SaEvoPro was benchmarked on 21 public deep mutational scanning (DMS) datasets and was subsequently applied to the engineering of flavanone cleavage reductase **ErFCR** for simultaneous improvement of catalytic activity and acid adaptation.

<img width="789" height="289" alt="image" src="https://github.com/user-attachments/assets/32995fe2-9341-4303-a48e-1d5099beb9af" />

---

## Overview

SaEvoPro retains the core workflow of EvolvePro, in which protein representations are interpreted by a top-layer regression model and experimentally measured fitness values are iteratively fed back into the model to guide subsequent variant selection.

The SaEvoPro workflow consists of four main steps:

1.Process: prepare wild-type and mutant protein sequences/structures together with experimental activity data.

2.Structure-aware representation: generate SaProt structure-aware embeddings for protein variants.

3.Run SaEvoPro: train and optimize the top-layer regression model and use an acquisition strategy to nominate variants for the next round.

4.Visualize and iterate: analyze the predicted fitness landscape, experimentally test selected variants, and feed the new measurements back into the next iteration.


---

## Installation

## External software and resources

Step-by-Step Description

1. Process

The wild-type protein structure is first generated using AlphaFold2. Single-site mutant structures are then generated using PreMut.

The protein variants and their experimentally measured activity or fitness values are prepared for downstream active-learning analysis.

External resources:

AlphaFold2: https://github.com/google-deepmind/alphafold

PreMut: https://github.com/jianlin-cheng/PreMut

For installation and usage, please follow the instructions provided by the original developers.

2. Structure-aware protein representations

SaEvoPro introduces SaProt structure-aware protein representations into the EvolvePro active-learning framework.

The following SaProt checkpoints were evaluated in this study:

SaProt-35M-AF2

SaProt-650M-PDB

SaProt-650M-AF2

SaProt-1.3B-AFDB-OMG-NCBI

Among the tested models, SaProt-1.3B-AFDB-OMG-NCBI showed the best overall benchmark performance and was selected as the structure-aware representation model for SaEvoPro.

ESM-2 15B was used as a sequence-only control.

External resources:

SaProt: https://github.com/westlake-repl/SaProt

SaProt pretrained models: https://huggingface.co/SaProtHub

ESM / ESM-2: https://github.com/facebookresearch/esm

Foldseek: https://github.com/steineggerlab/foldseek

3. Run SaEvoPro


External resources:

EvolvePro: https://github.com/mat10d/EvolvePro


---




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
