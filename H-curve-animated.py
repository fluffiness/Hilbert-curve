import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

class AniCurve:
    """animates the Hilbert curve growing from order 0 to self.order"""
    def __init__(self, order=0, scale=10, f=11, color='#38D6A6', figsize=8, linewidth=1, interval=20):
        """
        order: the order of Hilbert curve to animate
        scale: the side length of the initial order 0 curve in units
        f: frames per stage
        figsize: in inches
        interval: milliseconds per frame
        """
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(figsize, figsize)
        self.scale = scale
        self.f = f
        self.interval = interval
        self.original = np.array([-1 - 1j, -1 + 1j, 1 + 1j, 1 - 1j]) * self.scale / 2 # complex coords for the order 0 curve
        self.prev = self.original # stores the previous order curve (complex)
        self.order = order
        self.current = [np.array([]) for _ in range(4)]
        self.ln = [plt.plot([], [], color, linewidth=linewidth, animated=True)[0] for _ in range(4)]
        self.ani = None
        # An array of matplotlib.lines.Line2D objects that will be returned by the update function

    def set_order(self, order: int):
        self.order = order

    def set_scale(self, scale: int):
        self.scale = scale
        self.original = np.array([-1 - 1j, -1 + 1j, 1 + 1j, 1 - 1j]) * self.scale / 2

    def set_frames_per_stage(self, f: int):
        self.f = f
    
    def set_color(self, color: str):
        for l in self.ln:
            l.set_color(color)
    
    def set_figsize(self, figsize):
        self.fig.set_size_inches(figsize, figsize)
    
    def set_linewidth(self, linewidth):
        for l in self.ln:
            l.set_linewidth(linewidth)
    
    def set_interval(self, interval):
        self.interval = interval

    def __get_frames(self):
        """
        a generator of tuples (i, j, k)
        i: the current order of the Hilbert curve
        j: indicates the current stage. the four stages are: scale down, duplicate, rotate, connect
        k: self.f frames in each stage
        """
        if self.order == 0: yield 0
        for i in range(self.order):
            for j in range(4):
                for k in range(self.f):
                    yield (i, j, k)
    
    def __scale_down(self, t):
        """the scale down stage: scales down self.prev by 2 and transposes it to the upper left corner"""
        # t is used to parameterize the process. the whole process is split into (self.f-1) parts since t goes from 0 to (self.f-1)
        self.current[0] = self.prev * (1 - t / 2 / (self.f - 1)) + (-1 + 1j) * self.scale / 2 * t / (self.f - 1)
        self.ln[0].set_data(self.current[0].real, self.current[0].imag)
        return self.ln[0],

    def __duplicate(self, t):
        """the duplicate stage: duplicates the scaled-down curve and moves them to place"""
        self.current[1] = self.current[0] + self.scale * 1 * t / (self.f - 1)
        self.current[2] = self.current[0] + self.scale * (1 - 1j) * t / (self.f - 1)
        self.current[3] = self.current[0] + self.scale * (-1j) * t / (self.f - 1)
        for i in range(4):
            self.ln[i].set_data(self.current[i].real, self.current[i].imag)
        return self.ln

    def __rotate(self, t):
        """the rotate stage: rotates the bottom two curves"""
        self.current[2] = self.prev * 0.5 * np.exp(np.deg2rad(-90 / (self.f - 1) * t) * 1j) + self.scale * (-1 - 1j) / 2
        self.current[3] = self.prev * 0.5 * np.exp(np.deg2rad(90 / (self.f - 1) * t) * 1j) + self.scale * (1 - 1j) / 2
        for i in range(4):
            self.ln[i].set_data(self.current[i].real, self.current[i].imag)
        return self.ln

    def __connect(self, t):
        """the connect stage: connects the four lower-order curves"""
        self.prev = np.concatenate((np.flip(self.current[2]), self.current[0], self.current[1], np.flip(self.current[3])))
        self.ln[0].set_data(self.prev.real, self.prev.imag)
        return self.ln[0],

    def animate(self):
        """animates the curve generation using matplotlib.animation.FuncAnimation"""
        def init():
            """the initialization function to be passed to FuncAnimation class"""
            self.prev = self.original
            self.ax.set_xlim(-self.scale-2, self.scale+2)
            self.ax.set_ylim(-self.scale-2, self.scale+2)
            self.ax.set_aspect('equal')
            x, y = self.original.real, self.original.imag
            self.ln[0].set_data(x, y)
            plt.plot([-10, -10, 10, 10, -10], [-10, 10, 10, -10, -10])
            return self.ln[0],
        
        def update(frame):
            """tells FuncAnimation what to display each frame"""
            # the comma at the end packs the returned value in a tuple, since FuncAnimation only takes iterables
            if self.order == 0: return self.ln[0], 
            
            stage = frame[1]
            t = frame[2]

            # no if-else here. beautiful<3
            if stage == 0: return self.__scale_down(t)
            if stage == 1: return self.__duplicate(t)
            if stage == 2: return self.__rotate(t)
            return self.__connect(t)
        
        self.ani = animation.FuncAnimation(self.fig, update, frames=self.__get_frames(), init_func=init, blit=True, repeat=False, interval=self.interval)
        plt.show()

if __name__ == "__main__":
    animated = AniCurve(order=2)
    animated.set_color('b')
    animated.set_figsize(9)
    animated.animate()  
