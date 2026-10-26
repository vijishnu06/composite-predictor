import matplotlib.pyplot as plt
import numpy as np


def performance(actual, predicted):
    actual, predicted = np.asarray(actual), np.asarray(predicted)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].scatter(actual, predicted, s=12, alpha=0.6)
    low, high = min(actual.min(), predicted.min()), max(actual.max(), predicted.max())
    axes[0].plot([low, high], [low, high], '--', color='gray')
    axes[0].set(xlabel='Held-out target (MPa)', ylabel='Model estimate (MPa)')
    axes[1].scatter(predicted, actual - predicted, s=12, alpha=0.6)
    axes[1].axhline(0, color='gray', linestyle='--')
    axes[1].set(xlabel='Model estimate (MPa)', ylabel='Target − estimate (MPa)')
    fig.tight_layout()
    return fig
