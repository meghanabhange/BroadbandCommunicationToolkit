import math
import matplotlib.pyplot as plt


class OpticalFibre:
    def __init__(
        self,
        core_radius, 
        cladding_radius,
        wavelength,
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
        self.core_radius = core_radius
        self.cladding_radius = cladding_radius
        if core_radius>cladding_radius:
            raise ValueError("Core Radius can't be bigger than cladding radius")
        self.wavelength = wavelength
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
            self.calculate_normalised_frequency()
            self.calculate_guided_mode()
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
            self.calculate_normalised_frequency()
            self.calculate_guided_mode()
            self.n2 = self.n1 * (1 - self.delta)

        print(f"Optical Fibre Properties:")
        print(f"Critical Angle:{self.critical_angle}")
        print(f"Acceptance Angle:{self.acceptance_angle}")
        print(f"Numerical Apparture:{self.NA}")
        print(f"Profile :{self.index} Index Fibre")
        print(f"Normalised Frequency :{self.normalised_frequency}")
        print(f"Guided Mode :{self.guided_mode}")
        print(f"Mode :{self.mode}")

    def calculate_normalised_frequency(self):
        self.normalised_frequency = (2*math.pi*self.core_radius*self.NA)/(self.wavelength)
        if self.normalised_frequency<2.405:
            self.mode="Single Mode"
        else:
            self.mode= "Multi Mode"
    
    def calculate_guided_mode(self, alpha=2):
        if self.mode=="Multi Mode":
            if self.index=="Step":
                self.guided_mode=int((self.normalised_frequency**2)/2)
            else:
                self.guided_mode=int((alpha*(self.normalised_frequency**2))/((alpha+2)*2))
        else:
            self.guided_mode="NA"

    def get_profile(self, alpha=2):
        total_length = int((2 * self.cladding_radius))
        if self.index == "Step":
            X = [i for i in range(-int(total_length / 2), int(total_length / 2))]
            Y = [
                self.n2 if ((rad < -self.core_radius) or (rad > self.core_radius)) else self.n1
                for rad in X
            ]
        elif self.index == "Graded":
            self.delta = (self.n1 ** 2 - self.n2 ** 2) / (2 * self.n1 ** 2)
            X = [i for i in range(-int(total_length / 2), int(total_length / 2))]
            if alpha%2==0:
                Y = [
                    self.n1 * (math.sqrt(1 - 2 * self.delta))
                    if ((rad < -self.core_radius) or (rad > self.core_radius))
                    else self.n1
                    * (math.sqrt(1 - (2 * self.delta * ((rad / self.core_radius) ** alpha))))
                    for rad in X
                ]
            else:
                Y1 = [
                    self.n1 * (math.sqrt(1 - 2 * self.delta))
                    if ((rad < -self.core_radius) or (rad > self.core_radius))
                    else self.n1
                    * (math.sqrt(1 - (2 * self.delta * ((-rad / self.core_radius) ** alpha))))
                    for rad in X[:int(len(X)/2)]
                ]
                Y2 = [
                    self.n1 * (math.sqrt(1 - 2 * self.delta))
                    if ((rad < -self.core_radius) or (rad > self.core_radius))
                    else self.n1
                    * (math.sqrt(1 - (2 * self.delta * ((rad / self.core_radius) ** alpha))))
                    for rad in X[int(len(X)/2):]
                ]
                Y = Y1+Y2
        return X, Y

    def plot_profile(self, alpha=2):
        X, Y = self.get_profile(alpha)
        plt.plot(X, Y)
        plt.ylabel("Refractive Index")
        plt.xlabel("Radius")
        plt.title(f"{self.index} Indexed Fibre. Alpha : {alpha}")
        plt.show()
    
    def plot_multiple_profile(self, alphas=[1,2,3,10000]):
        if self.index!="Graded":
            raise ValueError("The fibre is not Graded Indexed Fibre")
        for alpha in alphas:
            X, Y = self.get_profile(alpha)
            plt.plot(X, Y, label=f"{alpha}")
        plt.ylabel("Refractive Index")
        plt.xlabel("Radius")
        plt.legend(loc="upper left")
        plt.title(f"{self.index} Indexed Fibre.")
        plt.show()
