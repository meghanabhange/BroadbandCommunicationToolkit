# BroadbandCommunicationToolkit 

## Usage 
While creating any optical fibre you must provide the following details 
- n1, n2, and profile type (the default profile is step index)
or 
- n1 and refractive index difference

The model will throw an error if incomplete information is provided. 

ex1

`myfibre = OpticalFibre(core_n=1.46, cladding_n=1.39, index="Graded")`

ex2

`myfibre = OpticalFibre(core_n=1.46, refractive_index_difference=0.01, index="Step")`


invalid entry

`myfibre = OpticalFibre(index="Step")`

or 

`myfibre = OpticalFibre(refractive_index_difference=0.01, index="Step")`

Then you can see all the intrensic model parameters :

```
Optical Fibre Properties:
Critical Angle:72.18602353338088
Acceptance Angle:26.52922450390899
Numerical Apparture:0.4466542286825459
Profile :Graded Index Fibre
```

Formulas
![Imgur](https://i.ibb.co/34Hym0K/Screenshot-2020-03-02-at-1-24-54-AM.png)

## Plotting the Profiles

The curves can then be plotted by invoking plot_profile method

![Graded](https://www.its.bldrdoc.gov/fs-1037/equats/37c_30.gif)

`myfibre.plot_profile(core_radius=30, cladding_radius=50)`

Graded Indexed Fibre

![Graded](https://i.ibb.co/q7CygnF/Screenshot-2020-03-02-at-1-32-51-AM.png)

Step Indexed Fibre

![Step](https://i.ibb.co/zr3H66j/Screenshot-2020-03-02-at-1-32-36-AM.png)

Multiple Alpha Plotting
![multi](https://i.ibb.co/h2JMgf4/Screenshot-2020-03-02-at-11-44-36-AM.png)
