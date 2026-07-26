"""
RAIL+AION photo-z entry points, wrapping the modular Pontifex package.
"""

from typing import Union
from pathlib import Path
import pontifex

def train_and_estimate(
    train_file: Union[str, Path],
    test_file: Union[str, Path],
    output_file: Union[str, Path],
    save_model_to: Union[str, Path, None] = None,
    seed: int = 42,
    optimize_hyperparams: bool = False,
) -> None:
    """
    Train the committee of experts, perform footprint-corrected EM calibration
    via Nugundam, and predict on the test catalog.
    """
    pontifex.train_and_estimate(
        train_file=train_file,
        test_file=test_file,
        output_file=output_file,
        save_model_to=save_model_to,
        seed=seed,
        optimize_hyperparams=optimize_hyperparams
    )

def estimate_only(
    model_file: Union[str, Path],
    test_file: Union[str, Path],
    output_file: Union[str, Path],
) -> None:
    """
    Run committee prediction and Nugundam EM calibration using saved model weights.
    """
    pontifex.estimate_only(
        model_file=model_file,
        test_file=test_file,
        output_file=output_file
    )
