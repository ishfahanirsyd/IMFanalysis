#!/usr/bin/env python3
import cfpack as cfp
import numpy as np
import matplotlib.pyplot as plt

# Define parameter
num_bins=1000  # Number of bins
M_min=1e-2  # Minimum mass for the IMF
M_max=1e2  # Initial maximum mass for the IMF

# Define the function to compute dN/dlogM
def dN_dlogM(M):
    if M <= 1:
        return 0.093 * np.exp(-((np.log10(M) - np.log10(0.2))**2) / (2 * 0.55**2))
    else:
        return 0.041 * M**(-1.35)

# Question 3.1
""" This is the definition of the IMF function. The IMF dN_dM) is computed by using the chain rule. Here, I dont print anything, 
but this function will be called in the next question"""
# Define the derivative of logM with respect to M
def dlogM_dM(M):
    return 1 / (M * np.log(10))

# Define the IMF function dN/dM
def dN_dM(M):
    return dN_dlogM(M) * dlogM_dM(M) # Compute dN/dM using the chain rule


# Question 3.2
""" This is the function to discretize the IMF. I define the parameter above so it is easy to modify, which currently i set it to be 1000 bins.
This function will also not print anything but it will be called in the next question"""
# Function to discretize IMF(M)
def IMF_discretized(M_min, M_max, num_bins):
    Mass_bins = np.logspace(np.log10(M_min), np.log10(M_max), num_bins) # Create logarithmically spaced mass bins
    IMF_bins = np.array([dN_dM(M) for M in Mass_bins]) # Calculate dN/dM for each bin
    return Mass_bins, IMF_bins


# Function for question 3.3, 3.4, and 3.5
""" This is a function to get the statistics and making plot for the IMF. This function will be used to answer question 3.3-3.5. 
It will generate a plot and print the answer for related question"""
def get_and_plot_pdf_stats(bins=num_bins, plot=True, xlabel="M", ylabel= "IMF(M)", mass_max= M_max, log=True, save='Question 3.3: IMF.png'):
    # Call function to discretize IMF
    Mass_bins, IMF_bins = IMF_discretized(M_min, mass_max, bins)
    # Define the width
    bin_width = Mass_bins[1:] - Mass_bins[:-1]
    # Append the last bin edges and assign it to variable M
    M = np.append(Mass_bins, Mass_bins[-1]+bin_width[-1])
    # Assign the IMF values to the variable IMF
    IMF = IMF_bins
    # Normalize IMF
    width = M[1:] - M[:-1]
    IMF = IMF /np.sum(IMF*width)
 

    # Question 3.3
    # Plot the IMF
    if plot:
        cfp.plot(x=M, y=IMF, xlabel=xlabel, xlog=log, ylabel=ylabel, ylog=log, xlim=(1e-2,1e2), label="Initial Mass Function (IMF)", type="pdf", save=save)

    # Class to return the statistics
    class ret:
        # Store the bin edges
        bin_edges = M
        # Average the edges to get the bin centers
        bin_center = (M[:-1] + M[1:]) / 2
        # Assign the IMF bins to the class attribute 
        IMF = IMF_bins  
        # Compute the bin width
        bin_width = M[1:] - M[:-1]
        # Get the mean by summation over the IMF
        mean = np.sum(IMF * bin_center * bin_width)
        # Get the mode
        mode = bin_center[IMF == np.max(IMF)]

    return ret


# Get the IMF statistics
dat=get_and_plot_pdf_stats()

# Question 3.4
# Get the mode mass of IMF
print("Question 3.4: mode of the IMF is", dat.mode)

# Question 3.5
# Get average star mass
print("Question 3.5: average star mass is", dat.mean, '(M☉)')


# Question 3.6
""" This question aims to test how the resulting average star mass depends on the number of bins. Here, I plot different number of bins
vs its average masses and see where is it started to converge within 1% accuracy (0.01)""" 
# Setting the minimum bins to 10 and the maximum bins to 1000, with interval 10
def average_mass_vs_bins(min_bins=10, max_bins=1000, step=10, target_accuracy=0.01):
    # Create an array of bin counts from min_bins to max_bins
    bins_range = np.arange(min_bins, max_bins+1, step)
    # List to store the average mass and bins
    average_masses = []
    number_bins=[]
    
    i = 0
    # Iterating through the bin counts 
    for bins in bins_range:
        # Call function to get the mean 
        result = get_and_plot_pdf_stats(bins=bins, plot=False)
        #Append the calculated mean and for each bins
        average_masses.append(result.mean)
        number_bins.append(bins)

        # If the average masses on the list is more than 1, start to check the convergence
        if len(average_masses) > 1:
            # Define the accuracy
            # The accuracy is the difference between current average mass and the previous average mass normalized by the previous average mass
            accuracy = abs(average_masses[-1] - average_masses[-2]) / average_masses[-2]
            # Check if the desired accuracy (less than 1%) is achieved
            if accuracy < target_accuracy:
                i += 1
                if i==1:
                    print(f"Question 3.6: Convergence achieved with {bins} bins for 1% accuracy.")
    # Use cfpack to plot the average mass vs. number of bins
    cfp.plot(x=number_bins, y=average_masses, xlabel='Number of Bins', ylabel='Average Star Mass (M☉)', type='xy', label= "Average mass as a function of bins", save='Question 3.6: AverageMass_vs_Bins.png')

    return bins_range, average_masses

# Run the function for 3.6
bins_range, average_masses = average_mass_vs_bins()

# Question 3.7
""" This question aims to compute the average mass for Mmax → ∞. Here I examine different huge number of mass and see where is it started to converge. I also add 
a plot to see the convergence within 1% accuracy (0.01)"""
# Setting the initial Mmax to 1 and maximum Mmax to 1e14, with interval 10
def average_mass_vs_Mmax(initial_Mmax=1, max_Mmax=1e14, step=10, accuracy_threshold=0.01):
    M_max_values = []  # List to store the different M_max values used
    average_masses = []  # List to store the average mass corresponding to each M_max value
    M_max = initial_Mmax  # Start with the initial M_max value

    i = 0
    # Iterating through each M_max 
    while M_max <= max_Mmax:
        # Call function to get the average mass for the current M_max
        result = get_and_plot_pdf_stats(bins=5000, plot=False,mass_max= M_max)
        average_masses.append(result.mean)
        # Append the current M_max to the list
        M_max_values.append(M_max)

        # If the average masses on the list is more than 1, start to check the convergence
        if len(average_masses) > 1:
            # Check if the accuracy is within 1%
            # The accuracy is the difference between current average mass and the previous average mass normalized by the previous average mass
            if abs(average_masses[-1] - average_masses[-2]) / average_masses[-2] < accuracy_threshold:
                i+=1
                if i==1:
                    print(f"Question 3.7: converged to within 2 significant figures at M_max = {M_max} with average mass= {result.mean}")
                
        M_max *= step  # Increase M_max exponentially with step= 10
    # Use cfpack to plot the average mass vs. number of bins
    cfp.plot(x=M_max_values, y=average_masses, xlabel='Maximum Mass', ylabel='Average Star Mass (M☉)', type='xy', label= "Average mass as a function of mass", save='Question 3.7: AverageMass_vs_Mass.png',xlog=True)
    return M_max_values, average_masses

# Run the function for 3.7
M_max_values, average_masses= average_mass_vs_Mmax()


