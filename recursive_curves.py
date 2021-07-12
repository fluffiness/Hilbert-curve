import matplotlib.pyplot as plt
import numpy as np

def hilbert_curve(order:int, scale:int = 10):
    """returns the x and y axis, of the points on the hilbert curve in two seperate numpy arrays"""    
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

def sierpinski_curve(order:int, scale:int = 10):
    """returns the x and y axis, of the points on the triangular sierpinski curve in two seperate numpy arrays"""
    def siepinski_curve_complex(order, scale):
        if order == 0:
            seglen = scale/np.sqrt(3)
            angles = np.exp(np.deg2rad([-30, 30, 150, 210]) * 1j)
            radii = np.array([seglen, seglen/2, seglen/2, seglen])
            return radii * angles
        
        prev = siepinski_curve_complex(order-1, scale/2)
        seglen = scale/np.sqrt(3)/2
        seg1 = np.flip(prev * np.exp(np.deg2rad(120) * 1j) + (np.exp(np.deg2rad(-30) * 1j) * seglen))
        seg2 = prev + seglen * 1j
        seg3 = np.flip(prev * np.exp(np.deg2rad(240) * 1j) + (np.exp(np.deg2rad(210) * 1j) * seglen))
        return np.concatenate((seg1, seg2, seg3))
    
    points = siepinski_curve_complex(order, scale)
    x, y = points.real, points.imag
    return x, y

if __name__ == "__main__":
    x, y = sierpinski_curve(2)
    plt.figure(figsize=(8, 8))
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.axis('equal')
    p, = plt.plot(x, y, linewidth=1)
    plt.show()