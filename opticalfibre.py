import math
import matplotlib.pyplot as plt


class OpticalFibre:
    def __init__(
        self,
        core_n=None,
        cladding_n=None,
        refractive_index_difference=None,
        index="Step",
    ):
        """[summary]
        
        Keyword Arguments:
            index {str} -- Type of the fibre "Step index" or "Graded Index" (default: {"Step"})
        """
        self.index = index
        if not (refractive_index_difference):
            if not (core_n) or not (cladding_n):
                raise ValueError(
                    "Incomplete information\nPlease Provide either n1, n2 or refractive index difference"
                )
            self.n1 = core_n
            self.n2 = cladding_n
            if self.n1 < self.n2:
                raise ValueError("Core Refractive Index is greater than cladding")
            self.NA = math.sqrt((self.n1 ** 2) - (self.n2 ** 2))
            self.critical_angle = math.degrees(math.asin(self.n2 / self.n1))
            self.acceptance_angle = math.degrees(math.asin(self.NA))
        else:
            if not (refractive_index_difference) or not (core_n):
                raise ValueError(
                    "Incomplete information\nPlease Provide either n1, n2 or refractive index difference"
                )
            self.delta = refractive_index_difference
            self.n1 = core_n
            self.NA = self.n1 * math.sqrt(2 * self.delta)
            self.critical_angle = math.degrees(math.asin(1 - self.delta))
            self.acceptance_angle = math.degrees(math.asin(self.NA))
            self.n2 = self.n1 * (1 - self.delta)

        print(f"Optical Fibre Properties:")
        print(f"Critical Angle:{self.critical_angle}")
        print(f"Acceptance Angle:{self.acceptance_angle}")
        print(f"Numerical Apparture:{self.NA}")
        print(f"Profile :{self.index} Index Fibre")

    def plot_profile(self, core_radius, cladding_radius, alpha=2):
        total_length = int((2 * cladding_radius))
        if self.index == "Step":
            X = [i for i in range(-int(total_length / 2), int(total_length / 2))]
            Y = [
                self.n2 if ((rad < -core_radius) or (rad > core_radius)) else self.n1
                for rad in X
            ]
        elif self.index == "Graded":
            self.delta = (self.n1 ** 2 - self.n2 ** 2) / (2 * self.n1 ** 2)
            X = [i for i in range(-int(total_length / 2), int(total_length / 2))]
            Y = [
                self.n1 * (sqrt(1 - 2 * self.delta))
                if ((rad < -core_radius) or (rad > core_radius))
                else self.n1
                * (sqrt(1 - (2 * self.delta * ((rad / core_radius) ** alpha))))
                for rad in X
            ]
        plt.plot(X, Y)
        plt.ylabel("Refractive Index")
        plt.xlabel("Radius")
        plt.show()
