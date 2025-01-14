import numpy as np  # Import numpy for numerical operations
import matplotlib.pyplot as plt  # Import matplotlib for plotting graphs
from scipy.signal import convolve  # Import convolve function from scipy for signal processing (not used in this code)
from scipy.stats import norm  # Import norm function from scipy.stats (not used in this code)

# Function to add AWGN (Additive White Gaussian Noise) noise to a signal
def add_awgn_noise(signal, SNR_dB):
    """
    Adds Gaussian noise to the signal based on the specified SNR (Signal-to-Noise Ratio).
    
    Parameters:
    - signal: The original signal to which noise will be added.
    - SNR_dB: The desired Signal-to-Noise Ratio in decibels (dB).
    
    Returns:
    - signal with added AWGN noise.
    """
    # Convert SNR from dB to linear scale
    SNR_linear = 10**(SNR_dB / 10)  # Linear SNR
    # Calculate signal power (mean squared value of the signal)
    signal_power = np.mean(np.abs(signal)**2)
    # Calculate noise power based on SNR
    noise_power = signal_power / SNR_linear
    # Generate complex noise with Gaussian distribution (real and imaginary parts)
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(signal)) + 1j * np.random.randn(len(signal)))
    # Return the signal with added noise
    return signal + noise

# Parameters for the simulation
num_symbols = 1000  # Number of symbols to generate for the communication system
SNR_values = np.arange(0, 21, 2)  # SNR values from 0 to 20 dB in steps of 2

# 1. Generate random symbols (from 0 to 15 for 16-QAM modulation)
symbols = np.random.randint(0, 16, num_symbols)  # Generates 1000 random symbols between 0 and 15

# 2. 16-QAM modulation: Mapping symbols to complex plane
modulated = ((2 * (symbols % 4) - 3) + 1j * (2 * (symbols // 4) - 3)) / np.sqrt(10)
# Explanation: 
# - 'symbols % 4' gives values between 0 and 3 (used for the real part).
# - 'symbols // 4' gives values between 0 and 3 (used for the imaginary part).
# - These values are scaled and mapped to the complex plane, normalized by 1/sqrt(10) for power control.

# 3. Add noise and plot constellations
SNR = 20  # Set a specific SNR value (20 dB) for visualization of the signal
noisy_signal = add_awgn_noise(modulated, SNR)  # Add AWGN noise to the modulated signal

# Plot the constellation diagram of the modulated signal (no noise)
plt.figure()  # Create a new figure
plt.scatter(modulated.real, modulated.imag, c='b', label="Modulated Signal")  # Scatter plot for modulated symbols
plt.title("Constellation Diagram of Modulated Signal")  # Title for the plot
plt.xlabel("In-phase")  # Label for the x-axis
plt.ylabel("Quadrature")  # Label for the y-axis
plt.grid()  # Add a grid for better visualization
plt.legend()  # Add a legend to indicate the plot label

# Plot the constellation diagram of the noisy signal and compare with the transmitted symbols
plt.figure()  # Create a new figure
plt.scatter(noisy_signal.real, noisy_signal.imag, c='g', label="Noisy Signal")  # Scatter plot for noisy signal
plt.scatter(modulated.real, modulated.imag, c='r', label="Transmitted Symbols")  # Scatter plot for transmitted symbols
plt.title("Constellation Diagram of Noisy Signal with Transmitted Symbols")
plt.xlabel("In-phase")  # Label for the x-axis
plt.ylabel("Quadrature")  # Label for the y-axis
plt.grid()  # Add a grid for better visualization
plt.legend()  # Add a legend

# Plot the real and imaginary parts of the signals over time
plt.figure(figsize=(10, 8))  # Create a larger figure for multiple subplots
# Real part of the modulated signal
plt.subplot(2, 2, 1)  # 2 rows, 2 columns, position 1
plt.plot(modulated.real)  # Plot real part of modulated signal
plt.title("Real Part of Modulated Signal")  # Title for the plot
plt.xlabel("Sample")  # Label for the x-axis (samples)
plt.ylabel("Amplitude")  # Label for the y-axis (amplitude)
plt.grid()  # Add grid

# Imaginary part of the modulated signal
plt.subplot(2, 2, 2)  # 2 rows, 2 columns, position 2
plt.plot(modulated.imag)  # Plot imaginary part of modulated signal
plt.title("Imaginary Part of Modulated Signal")  # Title for the plot
plt.xlabel("Sample")  # Label for the x-axis (samples)
plt.ylabel("Amplitude")  # Label for the y-axis (amplitude)
plt.grid()  # Add grid

# Real part of the noisy signal
plt.subplot(2, 2, 3)  # 2 rows, 2 columns, position 3
plt.plot(noisy_signal.real)  # Plot real part of noisy signal
plt.title("Real Part of Noisy Signal")  # Title for the plot
plt.xlabel("Sample")  # Label for the x-axis (samples)
plt.ylabel("Amplitude")  # Label for the y-axis (amplitude)
plt.grid()  # Add grid

# Imaginary part of the noisy signal
plt.subplot(2, 2, 4)  # 2 rows, 2 columns, position 4
plt.plot(noisy_signal.imag)  # Plot imaginary part of noisy signal
plt.title("Imaginary Part of Noisy Signal")  # Title for the plot
plt.xlabel("Sample")  # Label for the x-axis (samples)
plt.ylabel("Amplitude")  # Label for the y-axis (amplitude)
plt.grid()  # Add grid

plt.tight_layout()  # Adjust the layout to prevent overlapping subplots

# 4. Demodulation and error calculation
def demodulate_16qam(received):
    """
    Demodulates a received signal based on 16-QAM modulation scheme.
    
    Parameters:
    - received: The received noisy signal (complex).
    
    Returns:
    - Demodulated symbol indices.
    """
    # Quantize the real and imaginary parts to the closest valid constellation point
    real_part = np.clip(np.round((received.real * np.sqrt(10) + 3) / 2), 0, 3)  # Quantize real part
    imag_part = np.clip(np.round((received.imag * np.sqrt(10) + 3) / 2), 0, 3)  # Quantize imaginary part
    # Reconstruct the symbol by combining real and imaginary parts
    return (real_part + 4 * imag_part).astype(int)  # Mapping back to symbol index

# Demodulate the noisy signal and calculate bit errors
demodulated = demodulate_16qam(noisy_signal)  # Demodulate the noisy signal
num_errors = np.sum(symbols != demodulated)  # Count the number of errors (mismatches)
error_rate = num_errors / num_symbols  # Calculate the error rate

# Print the error information at a specific SNR value (SNR = 20 dB)
print(f"Number of errors at SNR = {SNR} dB: {num_errors}")
print(f"Error rate at SNR = {SNR} dB: {error_rate}")

# 5. Error rate analysis for different SNR values
ber = []  # List to store the Bit Error Rate (BER) for different SNR values

# Loop over different SNR values and calculate the error rate for each
for snr in SNR_values:
    noisy_signal = add_awgn_noise(modulated, snr)  # Add noise to the modulated signal
    demodulated = demodulate_16qam(noisy_signal)  # Demodulate the noisy signal
    num_errors = np.sum(symbols != demodulated)  # Count the number of errors
    ber.append(num_errors / num_symbols)  # Store the error rate for the current SNR

# 6. Plot error probability curve vs SNR
plt.figure()  # Create a new figure for plotting the BER vs SNR
plt.semilogy(SNR_values, ber, 'o-', linewidth=2)  # Plot BER on logarithmic scale (y-axis) vs SNR
plt.xlabel("SNR (dB)")  # Label for the x-axis
plt.ylabel("Bit Error Rate (BER)")  # Label for the y-axis
plt.title("BER vs SNR for 16-QAM")  # Title for the plot
plt.grid()  # Add grid

# Show all plots at once
plt.show()  # Display all the created plots
