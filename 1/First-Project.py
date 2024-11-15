import numpy as np
import matplotlib.pyplot as plt

#"Simulate PAM signal transmission with Gaussian noise at 10 dB SNR"
# شبیه‌سازی انتقال سیگنال PAM همراه با نویز گوسی در SNR برابر با 10 دسی‌بل.

# پارامترهای اولیه
# Initial parameters
A = 1  # دامنه سیگنال - Amplitude of the signal
RB = 1e3  # نرخ داده (تعداد نمادها در ثانیه) - Data rate (symbols per second)
T_symbol = 1 / RB  # زمان هر نماد - Duration of each symbol
fs = 10 * RB  # نرخ نمونه‌برداری (باید بزرگتر از نرخ داده باشد) - Sampling rate (must be higher than the data rate)
t_symbol = np.linspace(0, T_symbol, int(fs * T_symbol), endpoint=False)  
# محور زمان برای یک نماد - Time axis for a single symbol

# پالس Raised Cosine
# Raised Cosine pulse
beta = 0.35  # عامل roll-off - Roll-off factor
sinc_part = np.sinc(t_symbol / T_symbol - 1 / 2)  
# قسمت سینک از پالس - Sinc part of the pulse
cos_part = np.cos(np.pi * beta * t_symbol / T_symbol) / (1 - (2 * beta * t_symbol / T_symbol) ** 2)  
# قسمت کسینوسی پالس - Cosine part of the pulse

# ترکیب پالس
# Combining the pulse
raised_cosine_pulse = sinc_part * cos_part  
# ترکیب دو قسمت برای تولید پالس - Combining the two parts to create the pulse
raised_cosine_pulse /= np.max(np.abs(raised_cosine_pulse))  
# نرمال‌سازی پالس به ماکزیمم مقدارش - Normalizing the pulse to its maximum value

# تولید سیگنال PAM
# Generating the PAM signal
symbols = np.array([A, -A, A, -A, A])  
"Simulate PAM signal transmission with Gaussian noise at 10 dB SNR"

# دنباله‌ای از نمادهای دیجیتال با دامنه‌های مثبت و منفی - A sequence of digital symbols with positive and negative amplitudes
signal = np.zeros(0)  
# مقدار اولیه سیگنال کلی - Initializing the overall signal

# حلقه برای ترکیب نمادها با پالس
# Loop to combine symbols with the pulse
for symbol in symbols:
    signal = np.concatenate((signal, symbol * raised_cosine_pulse))  
    # مقیاس‌دهی پالس با نماد و اضافه کردن به سیگنال کلی - Scaling the pulse with the symbol and appending it to the overall signal

# محور زمان برای سیگنال نهایی
# Time axis for the final signal
t_signal = np.linspace(0, len(symbols) * T_symbol, len(signal), endpoint=False)  
# زمان برای کل سیگنال - Time axis for the entire signal

# پارامتر نویز گوسی
# Gaussian noise parameters
SNR_dB = 10  
# نسبت سیگنال به نویز در دسی‌بل - Signal-to-Noise Ratio (SNR) in decibels
SNR_linear = 10**(SNR_dB / 10)  
# تبدیل SNR از دسی‌بل به مقدار خطی - Convert SNR from decibels to linear scale

# انرژی سیگنال
# Signal power
signal_power = np.mean(signal**2)  
# توان میانگین سیگنال محاسبه می‌شود - Calculate the mean power of the signal

# واریانس نویز (برای ایجاد SNR مشخص)
# Noise variance (to match the specified SNR)
noise_power = signal_power / SNR_linear  
# توان نویز براساس نسبت SNR محاسبه می‌شود - Calculate noise power based on the SNR ratio

# تولید نویز گوسی
# Generate Gaussian noise
noise = np.random.normal(0, np.sqrt(noise_power), len(signal))  
# نویز گوسی با میانگین صفر و واریانس محاسبه شده ایجاد می‌شود - Generate Gaussian noise with zero mean and calculated variance

# ترکیب سیگنال با نویز
# Combine signal with noise
received_signal = signal + noise  
# اضافه کردن نویز به سیگنال اصلی - Add noise to the original signal

# نمایش سیگنال PAM همراه با نویز گوسی
# Plot the PAM signal with Gaussian noise
plt.figure(figsize=(10, 6))  
# تنظیم اندازه نمودار - Setting the figure size
plt.plot(t_signal, received_signal)  
# رسم سیگنال همراه نویز - Plot the signal with noise
plt.title(f"PAM Signal with Gaussian Noise (SNR = {SNR_dB} dB)")  
# عنوان نمودار همراه با مقدار SNR - Title of the plot with the SNR value
plt.xlabel("Time (s)")  
# برچسب محور زمان - X-axis label
plt.ylabel("Amplitude")  
# برچسب محور دامنه - Y-axis label
plt.grid(True)  
# فعال کردن شبکه نمودار - Enabling grid lines
plt.show()  
# نمایش نمودار - Display the plot
