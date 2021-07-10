import matplotlib.pyplot as plt
import numpy as np

def hilbert_curve(order:int, scale:int = 10):
    
    def hilbert_curve_complex(order, scale):
        if order == 0: return np.array([-1 - 1j, -1 + 1j, 1 + 1j, 1 - 1j]) * scale / 2
        
        prev = hilbert_curve_complex(order-1, scale/2)
        seg1 = np.flip(-1j * prev + (-1 - 1j) * scale / 2)
        seg2 = prev + (-1 + 1j) * scale / 2
        seg3 = prev + ( 1 + 1j) * scale / 2
        seg4 = np.flip(1j * prev + (1 - 1j) * scale / 2)
        return np.concatenate((seg1, seg2, seg3, seg4))

    points = hilbert_curve_complex(order, scale)
    x, y = points.real, points.imag
    return x, y

if __name__ == "__main__":
    x, y = hilbert_curve(7)
    plt.figure(figsize=(10, 10))
    plt.axis(False)
    plt.plot(x, y)
    plt.show()