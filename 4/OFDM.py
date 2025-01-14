import numpy as np
from scipy.fft import ifft, fft
from scipy.stats import norm
from sklearn.preprocessing import binarize 

# Define parameters
numSubcarriers = 64  # Number of subcarriers in the OFDM system
numSymbols = 1000    # Number of OFDM symbols to be transmitted
modOrder = 4         # Modulation order (e.g., 4 for QPSK, 16 for 16-QAM)
cpLength = 16        # Length of the cyclic prefix to mitigate ISI (Inter-Symbol Interference)
SNR_dB = 10          # Signal-to-Noise Ratio (SNR) in dB

# Calculate bits per symbol
bitsPerSymbol = int(np.log2(modOrder))  # Number of bits per symbol (e.g., 2 bits for QPSK)

# Generate random bitstream for data transmission
dataBits = np.random.randint(0, 2, numSymbols * numSubcarriers * bitsPerSymbol)  # Random binary data

# Map bits to QAM symbols
# Reshape the bitstream into groups of bits that represent each symbol
dataSymbols = dataBits.reshape(-1, bitsPerSymbol)
# Convert each group of bits into a decimal number representing the symbol
symbols = np.dot(dataSymbols, 2**np.arange(bitsPerSymbol)[::-1])

# Modulate the data using QAM (QPSK in this case)
# Create complex QAM symbols by modulating the symbol indices
modulatedData = np.exp(1j * (2 * np.pi * symbols / modOrder))

# Reshape the modulated data into OFDM symbols
# Each column represents an OFDM symbol (with numSubcarriers subcarriers)
ofdmSymbols = modulatedData.reshape(numSubcarriers, -1)

# Perform IFFT (Inverse Fast Fourier Transform) to convert frequency-domain symbols to time-domain
ifftData = ifft(ofdmSymbols, numSubcarriers, axis=0)

# Add a cyclic prefix to the IFFT data to prevent ISI (Inter-Symbol Interference)
cyclicPrefix = ifftData[-cpLength:, :]  # Take the last `cpLength` samples of each OFDM symbol
dataWithCP = np.vstack([cyclicPrefix, ifftData])  # Prepend the cyclic prefix to the IFFT data

# Serialize the OFDM symbols into a single array for transmission
txSignal = dataWithCP.flatten()

# Add AWGN (Additive White Gaussian Noise) to the transmitted signal to simulate a real channel
SNR_linear = 10**(SNR_dB / 10)  # Convert SNR from dB to linear scale
noisePower = np.var(txSignal) / SNR_linear  # Calculate noise power based on SNR and signal variance
# Generate complex Gaussian noise and add it to the transmitted signal
noise = np.sqrt(noisePower / 2) * (np.random.randn(len(txSignal)) + 1j * np.random.randn(len(txSignal)))
rxSignal = txSignal + noise  # Received signal is the transmitted signal plus noise

# Reshape the received signal to remove the cyclic prefix
rxSignalMatrix = rxSignal.reshape(numSubcarriers + cpLength, -1)  # Reshape into OFDM symbol blocks
rxSignalNoCP = rxSignalMatrix[cpLength:, :]  # Remove the cyclic prefix from the received signal

# Perform FFT (Fast Fourier Transform) to convert received time-domain signal back to frequency domain
rxSymbols = fft(rxSignalNoCP, numSubcarriers, axis=0)

# Demodulate the received QAM symbols
rxSymbolsFlattened = rxSymbols.flatten()  # Flatten the matrix into a vector
# Estimate the symbol values by mapping the phase angle of each received symbol
estimatedSymbols = np.round((np.angle(rxSymbolsFlattened) * modOrder) / (2 * np.pi))

# Adjust negative symbol indices to be positive, as QAM symbols are cyclic
estimatedSymbols[estimatedSymbols < 0] = estimatedSymbols[estimatedSymbols < 0] + modOrder

# Map the estimated symbols back to bits
receivedBits = np.array([list(np.binary_repr(int(symbol), width=bitsPerSymbol)) for symbol in estimatedSymbols])
# Flatten the list of binary representations and convert it to an array of bits
receivedBits = receivedBits.flatten().astype(int)

# Calculate the Bit Error Rate (BER)
# Count the number of bit errors by comparing the transmitted and received bitstreams
numErrors = np.sum(dataBits != receivedBits)
# Calculate the Bit Error Rate (BER) as the ratio of errors to the total number of bits
ber = numErrors / len(dataBits)

# Display the results
print(f'Number of errors: {numErrors}')
print(f'Bit Error Rate (BER): {ber:.5f}')
