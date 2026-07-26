# Photo-Z Data Challenge Submission: Pontifex

This branch contains the **Pontifex** submission for the DESC Photometric Redshift Data Challenge.

## Package Architecture & Modularity

Unlike previous submissions, the core codebase of the `Pontifex` pipeline has been refactored into a standalone, pip-installable python package. The code in this repository (`rail_aion_pz.py`) acts as a thin wrapper interfacing the challenge entry points with the modular `pontifex` package.

* **Core Package**: Development, documentation, and unit tests of the pipeline logic reside in the `code/Pontifex` directory.
* **Challenge Submission**: Standardized entry points, pre-computed prediction outputs, and CI workflows reside in this `pz_data_challenge` repository.

## Installation & Environment Setup

To run the `pontifex` pipeline locally, first create the Conda environment and install the package:

1. **Create and Activate Conda Environment**
   ```bash
   conda create -n CorrFunc python=3.11 numpy scipy pandas joblib astropy matplotlib sphinx sphinx-autoapi pytest -y
   conda activate CorrFunc
   ```

2. **Editable Installation**
   Run the editable installation of the package:
   ```bash
   pip install -e ../../code/Pontifex
   ```

### Troubleshooting Linker Errors
If compilation fails with `cannot find /lib64/libm.so.6`, edit your Conda compiler sysroot linker scripts (typically under `~/anaconda3/x86_64-conda-linux-gnu/sysroot/lib64/`) and modify the absolute references to relative ones (e.g. change `/lib64/libm.so.6` to `libm.so.6`). See the package README in `code/Pontifex/README.md` for detailed instructions.

## Offline CI Test Execution & Split Packaging

To accommodate GitHub's **2 GB release asset size limit**, the submission assets are split into three packages under tag `v2.0.0` of the release page:
1. **`aion_base_weights.tgz`** (1.1 GB): Packaged Hugging Face transformer model cache.
2. **`whitesmoke.tgz`** (1.7 GB): Whitesmoke submission predictions.
3. **`pontifex.tgz`** (1.9 GB): Pontifex submission predictions and `.pkl` model definitions.

The CI test suite automatically downloads both `aion_base_weights.tgz` and the corresponding submission archive (`pontifex.tgz`), combines them locally in the workspace, and runs unit tests offline without network dependencies.

### Running Unit Tests Locally
To validate the submission locally using the CI limits (which caps training set size to 100 objects and EM iterations to 2 to run fast):
```bash
PZDC_CI_MAX_TRAIN=100 AION_PZ_DEVICE=cpu pytest -v tests/test_pontifex.py
```

## Hyperparameter Tuning (PSO)

The base estimators (experts) have been tuned using Particle Swarm Optimization (PSO) via `optunity` on a validation split of the challenge training catalog.
* By default, the pipeline loads precomputed optimal parameters from `results/pso_best_hyperparameters.pkl` to run fast.
* To perform a fresh optimization run (e.g., if new training data is provided), set the `optimize_hyperparams` toggle to `True` when calling the training entry point:
  ```python
  import rail_aion_pz
  rail_aion_pz.train_and_estimate(..., optimize_hyperparams=True)
  ```
