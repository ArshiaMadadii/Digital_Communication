import numpy as np
import matplotlib.pyplot as plt

# Add PAM signal error detection with Gaussian noise at 10 dB SNR
# اضافه کردن آشکارسازی خطای سیگنال PAM با نویز گوسی در SNR برابر 10 دسی‌بل.

# پارامترهای اولیه
# Initial parameters
A = 1  # دامنه سیگنال PAM
# Amplitude of PAM signal
RB = 1e3  # نرخ داده (تعداد نمادها در ثانیه)
# Data rate (symbols per second)
T_symbol = 1 / RB  # زمان هر نماد (ثانیه)
# Duration of each symbol (seconds)
fs = 10 * RB  # نرخ نمونه‌برداری (بالاتر از نرخ داده)
# Sampling rate (higher than data rate)
t_symbol = np.linspace(0, T_symbol, int(fs * T_symbol), endpoint=False)
# تولید بازه زمانی برای یک نماد
# Time range for one symbol

# پالس Raised Cosine
# Raised Cosine Pulse
beta = 0.35  # عامل roll-off
# Roll-off factor
sinc_part = np.sinc(t_symbol / T_symbol - 1 / 2)
# قسمت سینک (sinc function)
cos_part = np.cos(np.pi * beta * t_symbol / T_symbol) / (1 - (2 * beta * t_symbol / T_symbol) ** 2)
# قسمت کسینوس برای اعمال roll-off
# Cosine part for roll-off application

# ترکیب پالس
# Combining the pulse
raised_cosine_pulse = sinc_part * cos_part
raised_cosine_pulse /= np.max(np.abs(raised_cosine_pulse))
# نرمالیزه کردن پالس برای محدود کردن دامنه به 1
# Normalize pulse to limit amplitude to 1

# تولید سیگنال PAM
# Generating PAM signal
symbols = np.array([A, -A, A, -A, A])  
# سیگنال PAM با دامنه‌های مثبت و منفی
# PAM signal with positive and negative amplitudes
signal = np.zeros(0)  
# سیگنال اولیه خالی
# Initialize empty signal

for symbol in symbols:
    signal = np.concatenate((signal, symbol * raised_cosine_pulse))
# اضافه کردن هر نماد با استفاده از پالس Raised Cosine
# Append each symbol using the Raised Cosine pulse

# محور زمان برای سیگنال نهایی
# Time axis for the final signal
t_signal = np.linspace(0, len(symbols) * T_symbol, len(signal), endpoint=False)

# پارامتر نویز گوسی
# Gaussian noise parameters
SNR_dB = 10  
# نسبت سیگنال به نویز (دسی‌بل)
# Signal-to-Noise Ratio (dB)
SNR_linear = 10**(SNR_dB / 10)
# تبدیل SNR به مقیاس خطی
# Convert SNR to linear scale

# انرژی سیگنال
# Signal power
signal_power = np.mean(signal**2)

# واریانس نویز (برای ایجاد SNR مشخص)
# Noise variance (to achieve the desired SNR)
noise_power = signal_power / SNR_linear

# تولید نویز گوسی
# Generate Gaussian noise
noise = np.random.normal(0, np.sqrt(noise_power), len(signal))

# ترکیب سیگنال با نویز
# Combine signal with noise
received_signal = signal + noise

# آشکارسازی
# Detection
# مقایسه سیگنال دریافتی با صفر برای شناسایی نمادها
# Compare received signal with zero to detect symbols
detected_symbols = np.sign(received_signal)

# تولید نمادهای ایده‌آل (بدون نویز)
# Generate ideal symbols (noise-free)
ideal_symbols = np.concatenate([np.ones_like(raised_cosine_pulse) * symbol for symbol in symbols])

# محاسبه خطا: مقایسه نمادهای شناسایی شده با نمادهای اصلی
# Calculate errors: Compare detected symbols with original symbols
errors = np.sum(detected_symbols != ideal_symbols)

# محاسبه احتمال خطا
# Calculate error probability
error_probability = errors / len(detected_symbols)

# نمایش سیگنال PAM همراه با نویز گوسی
# Plot PAM signal with Gaussian noise
plt.figure(figsize=(10, 6))
plt.plot(t_signal, received_signal)
plt.title(f"PAM Signal with Gaussian Noise (SNR = {SNR_dB} dB)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

# چاپ تعداد خطاها و احتمال خطا
# Print number of errors and error probability
print(f"خطاهای آشکارسازی: {errors}")
print(f"احتمال خطا: {error_probability:.4f}")
