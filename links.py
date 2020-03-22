import scipy.constants as C
import numpy as np

class Channel:
    def __init__(self, *args, **kwargs):
        """
        - Core Radius in microns
        - Bandwidth in hertz
        - Attenuation in db/m
        """
        if "CoreRadius" in kwargs.keys():
            self.core_radius = kwargs["CoreRadius"]*C.micron
        if "NA" in kwargs.keys():
            self.na = kwargs["NA"]
        if "Bandwidth" in kwargs.keys():
            self.bw = kwargs["Bandwidth"]
        if "Attenuation" in kwargs.keys():
            self.attenuation = kwargs["Attenuation"]/C.kilo
        if "CoreN" in kwargs.keys():
            self.coren = kwargs["CoreN"]
        
class Transmitter:
    def __init__(self, *args, **kwargs):
        """
        - EmissionWavelength in Angstroms
        """
        if "EmissionWavelength" in kwargs.keys(): 
            self.emission_wavelength = kwargs["EmissionWavelength"]*C.micro
        if "SpectralLineWidth" in kwargs.keys():
            self.spectral_line_width = kwargs["SpectralLineWidth"]
        if "EffectiveRadiationArea" in kwargs.keys():
            self.era = kwargs["EffectiveRadiationArea"]
        if "EmissionPattern" in kwargs.keys():
            self.emission_pattern = kwargs["EmissionPattern"]

    def calculate_energy(self):
        return (C.h*C.c)/(self.emission_wavelength)

class Reciever:
    def __init__(self, *args, **kwargs):
        if "Responsivity" in kwargs.keys():
            self.responsivity = kwargs["Responsivity"]
        if "OperatingWavelength" in kwargs.keys():
            self.operating_wavelength = kwargs["OperatingWavelength"]
        if "Sensitivity" in kwargs.keys():
            self.sensitivity = kwargs["Sensitivity"]

class P2PSystem:
    def __init__(self, *args, **kwargs):
        self.transmitter = kwargs["Transmitter"]
        self.reciever = kwargs["Reciever"]
        self.channel = kwargs["Channel"]
        self.length = kwargs["Length"]*C.kilo
        self.dist = kwargs["dist"]*C.kilo
        self.safety_margin = kwargs["SafetyMargin"]
        self.lsp = kwargs["lsp"]
        self.connector_loss = kwargs["ConnectorLoss"]
        self.ps = kwargs["SourcePower"]
    
    def calculate_splice_loss(self):
        number_of_splices = int(self.length/self.dist)-1
        return self.lsp*number_of_splices

    def calculate_attenutation_loss(self):
        return self.channel.attenuation*self.length

    def calculate_allowed_loss(self):
        return self.ps-self.reciever.sensitivity
    
    def total_loss(self):
        LC = self.connector_loss
        L = self.calculate_attenutation_loss()
        Lsp = self.calculate_splice_loss()
        return ((2*LC)+(L)+Lsp+self.safety_margin)
    
    def is_loss_valid(self):
        pt_calc = self.total_loss()
        pt_alllowed = self.calculate_allowed_loss()
        if pt_calc<pt_alllowed:
            return True
        return False
             