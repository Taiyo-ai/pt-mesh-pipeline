import numpy as np

def convert_non_black_dots_to_white(img: np.ndarray) -> np.ndarray:
    grayscale = img
    grayscale[(grayscale[:, :, :] < 1) & (grayscale[:, :, :] != 0)] = 1

    for i in range(grayscale.shape[2] - 1):
        grayscale[:, :, i] = 1 - (1 - grayscale[:, :, 0]) * (1 - grayscale[:, :, 1]) * (1-grayscale[:, :, 2])
    
    return grayscale