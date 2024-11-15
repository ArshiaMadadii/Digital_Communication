import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# Add theoretical BER computation and plotting for PAM over a range of SNR values
# اضافه کردن محاسبه و رسم احتمال خطای نظری برای PAM در محدوده مقادیر SNR

# تابع Q-function
# Q-function definition
def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))
# Q(x) از تابع مکمل خطای گوسی (erfc) استفاده می‌کند.

# پارامترهای سیگنال
# Signal parameters
A = 1  # دامنه سیگنال PAM
# Amplitude of PAM signal
RB = 1e3  # نرخ داده (تعداد نمادها در ثانیه)
# Data rate (symbols per second)
T_symbol = 1 / RB  # مدت زمان هر نماد
# Duration of each symbol
fs = 10 * RB  # نرخ نمونه‌برداری (بالاتر از نرخ داده)
# Sampling rate (higher than data rate)

# دامنه SNR (دسی‌بل)
# SNR range in dB
SNR_dB_range = np.arange(0, 20, 1)  
# محدوده SNR از 0 تا 20 دسی‌بل
# SNR range from 0 to 20 dB
SNR_linear = 10**(SNR_dB_range / 10)  
# تبدیل SNR از دسی‌بل به مقیاس خطی
# Convert SNR from dB to linear scale

# محاسبه احتمال خطا (BER) با استفاده از تابع Q
# Calculate BER (Bit Error Rate) using the Q-function
BER_theoretical = Q(np.sqrt(SNR_linear))
# مقدار BER نظری بر اساس معادله Q محاسبه می‌شود.
# BER is calculated based on the theoretical Q equation.

# رسم منحنی BER
# Plotting the BER curve
plt.figure(figsize=(8, 6))
plt.semilogy(SNR_dB_range, BER_theoretical, label="Theoretical BER", marker='o')
# رسم منحنی با محور عمودی لگاریتمی
# Plot curve with logarithmic y-axis
plt.title("BER vs SNR for PAM (Theoretical)")
plt.xlabel("SNR (dB)")
plt.ylabel("BER")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
# افزودن خطوط شبکه به نمودار
# Add grid lines to the plot
plt.legend()
plt.show()
