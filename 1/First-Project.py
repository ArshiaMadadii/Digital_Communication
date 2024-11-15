import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# Add Raised Cosine pulse shaping to PAM BER simulation
# اضافه کردن شکل‌دهی پالس Raised Cosine به شبیه‌سازی احتمال خطا برای PAM.

# تابع Q-function
# Q-function definition
def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))
# Q(x) از تابع مکمل خطای گوسی (erfc) برای محاسبه احتمال خطای نظری استفاده می‌کند.
# Q(x) uses the complementary Gaussian error function (erfc) for theoretical error probability calculation.

# پارامترهای سیگنال
# Signal parameters
A = 1  # دامنه سیگنال PAM
# Amplitude of PAM signal
RB = 1e3  # نرخ داده (تعداد نمادها در ثانیه)
# Data rate (symbols per second)
T_symbol = 1 / RB  # مدت زمان هر نماد
# Duration of each symbol
fs = 10 * RB  # نرخ نمونه‌برداری
# Sampling rate
num_symbols = 10000  # تعداد نمادها برای شبیه‌سازی
# Number of symbols for simulation

# پارامترهای پالس Raised Cosine
# Raised Cosine pulse parameters
roll_off = 0.25  # ضریب رول‌آف
# Roll-off factor
span = 4  # تعداد نمادهای اثرگذار
# Number of symbol durations covered by the pulse

# تولید پالس Raised Cosine
# Generate Raised Cosine pulse
def raised_cosine_pulse(roll_off, span, T_symbol, fs):
    t = np.linspace(-span*T_symbol, span*T_symbol, int(2*span*T_symbol*fs))  # زمان
    # Time range for pulse generation
    h = np.sinc(t / T_symbol) * np.cos(np.pi * roll_off * t / T_symbol) / (1 - (2 * roll_off * t / T_symbol) ** 2)  # پالس
    # Raised Cosine pulse formula
    h[np.isnan(h)] = 0  # رفع NaN‌های احتمالی
    # Handle NaN values (if denominator becomes zero)
    return h / np.max(np.abs(h))  # نرمال‌سازی به دامنه واحد
    # Normalize pulse to unit amplitude

# تولید داده‌های تصادفی
# Generate random data
bits = np.random.choice([0, 1], size=num_symbols)
# Generate random bits (0 or 1)
symbols = 2*bits - 1  # تبدیل بیت‌ها به -1 و +1
# Map bits to PAM symbols (-1 and +1)

# اعمال پالس Raised Cosine به داده‌های PAM
# Apply Raised Cosine pulse shaping to PAM data
pulse = raised_cosine_pulse(roll_off, span, T_symbol, fs)
signal = np.convolve(symbols, pulse, mode='same')  
# Convolve symbols with Raised Cosine pulse

# دامنه SNR (دسی‌بل)
# SNR range in dB
SNR_dB_range = np.arange(0, 20, 1)  
# محدوده SNR از 0 تا 20 دسی‌بل
# SNR range from 0 to 20 dB
SNR_linear = 10**(SNR_dB_range / 10)  
# تبدیل SNR به واحد خطی
# Convert SNR from dB to linear scale

# محاسبه احتمال خطا (BER) با استفاده از تابع Q (تئوری)
# Calculate BER (Bit Error Rate) using the Q-function (theoretical)
BER_theoretical = Q(np.sqrt(SNR_linear))
# مقدار BER نظری بر اساس SNR محاسبه می‌شود.
# BER is calculated theoretically based on the SNR.

# شبیه‌سازی BER
# Simulate BER
BER_simulated = []

# شبیه‌سازی برای مقادیر مختلف SNR
# Simulation for different SNR values
for SNR_dB in SNR_dB_range:
    # تولید نویز گوسی با واریانس مناسب
    # Generate Gaussian noise with appropriate variance
    noise = np.random.normal(0, np.sqrt(1 / (2 * 10**(SNR_dB / 10))), size=signal.shape)
    
    # سیگنال دریافتی
    # Received signal
    received_signal = signal + noise
    
    # آشکارسازی و مقایسه با صفر
    # Detection and comparison with zero
    detected_symbols = np.sign(received_signal)
    
    # محاسبه احتمال خطا
    # Calculate error probability
    num_errors = np.sum(detected_symbols != symbols)
    BER_simulated.append(num_errors / num_symbols)

# رسم منحنی BER
# Plot BER curves
plt.figure(figsize=(8, 6))
plt.semilogy(SNR_dB_range, BER_theoretical, label="Theoretical BER", marker='o')
# رسم BER نظری
# Plot theoretical BER
plt.semilogy(SNR_dB_range, BER_simulated, label="Simulated BER", marker='x')
# رسم BER شبیه‌سازی شده
# Plot simulated BER
plt.title("BER vs SNR for PAM with Raised Cosine Pulse (Theoretical vs Simulated)")
plt.xlabel("SNR (dB)")
plt.ylabel("BER")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
# افزودن خطوط شبکه به نمودار
# Add grid lines to the plot
plt.legend()
plt.show()
