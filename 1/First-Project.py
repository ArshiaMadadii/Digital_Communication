import numpy as np
import matplotlib.pyplot as plt


# "تولید سیگنال PAM با استفاده از پالس Raised Cosine برای شبیه‌سازی ارتباطات دیجیتال."
# "Generate PAM signal using Raised Cosine pulse for digital communication simulation."

# پارامترهای اولیه
# Initial parameters
A = 1  # دامنه سیگنال - Amplitude of the signal
RB = 1e3  # نرخ داده (تعداد نمادها در ثانیه) - Data rate (symbols per second)
T_symbol = 1 / RB  # زمان هر نماد - Duration of each symbol
fs = 10 * RB  # نرخ نمونه‌برداری (باید بزرگتر از نرخ داده باشد) - Sampling rate (must be higher than the data rate)
t_symbol = np.linspace(0, T_symbol, int(fs * T_symbol), endpoint=False)  
# زمان برای یک نماد - Time axis for a single symbol

# پالس Raised Cosine
# Raised Cosine Pulse
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
# مثال برای یک سری از نمادها با دامنه‌های مثبت و منفی - Example of a sequence with positive and negative amplitudes
symbols = np.array([A, -A, A, -A, A])  
# سیگنال PAM با دامنه‌های مختلف - PAM signal with different amplitudes
signal = np.zeros(0)  
# مقدار اولیه سیگنال کلی - Initializing the overall signal

# حلقه برای تولید سیگنال نهایی
# Loop to generate the final signal
for symbol in symbols:
    signal = np.concatenate((signal, symbol * raised_cosine_pulse))  
    # ضرب پالس در هر نماد و اضافه کردن به سیگنال - Scaling the pulse with the symbol and appending to the signal

# محور زمان برای سیگنال نهایی
# Time axis for the final signal
t_signal = np.linspace(0, len(symbols) * T_symbol, len(signal), endpoint=False)  
# زمان برای کل سیگنال - Time axis for the entire signal

# نمایش سیگنال PAM
# Plotting the PAM signal
plt.figure(figsize=(10, 6))  
# تنظیم اندازه نمودار - Setting the figure size
plt.plot(t_signal, signal)  
# رسم سیگنال - Plotting the signal
plt.title("PAM Signal with Raised Cosine Pulse")  
# عنوان نمودار - Chart title
plt.xlabel("Time (s)")  
# برچسب محور زمان - X-axis label
plt.ylabel("Amplitude")  
# برچسب محور دامنه - Y-axis label
plt.grid(True)  
# فعال کردن شبکه نمودار - Enabling grid lines
plt.show()  
# نمایش نمودار - Display the plot


