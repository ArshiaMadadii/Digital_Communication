import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# تابع Q-function
def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))

# پارامترهای سیگنال
A = 1  # دامنه پایه سیگنال PAM
RB = 1e3  # نرخ داده (تعداد نمادها در ثانیه)
T_symbol = 1 / RB  # مدت زمان هر نماد
fs = 10 * RB  # نرخ نمونه‌برداری
num_symbols = 10000  # تعداد نمادها برای شبیه‌سازی

# پارامترهای پالس Raised Cosine
roll_off = 0.25  # ضریب رول‌آف
span = 4  # تعداد نمادهای اثرگذار

# تولید پالس Raised Cosine
def raised_cosine_pulse(roll_off, span, T_symbol, fs):
    t = np.linspace(-span * T_symbol, span * T_symbol, int(2 * span * T_symbol * fs))
    h = np.sinc(t / T_symbol) * np.cos(np.pi * roll_off * t / T_symbol) / (1 - (2 * roll_off * t / T_symbol) ** 2)
    h[np.isnan(h)] = 0
    return h / np.max(np.abs(h))

# تولید داده‌های تصادفی برای 4-PAM
bits = np.random.choice([0, 1, 2, 3], size=num_symbols)
symbols = A * (2 * bits - 3)  # تبدیل بیت‌ها به مقادیر 4-PAM: A3-, A-, A, A3

# اعمال پالس Raised Cosine به داده‌های PAM
pulse = raised_cosine_pulse(roll_off, span, T_symbol, fs)
signal = np.convolve(symbols, pulse, mode='same')

# دامنه SNR (دسی‌بل)
SNR_dB_range = np.arange(0, 20, 1)
SNR_linear = 10**(SNR_dB_range / 10)

# شبیه‌سازی BER
BER_simulated = []

# مقادیر آستانه برای آشکارسازی 4-PAM
thresholds = np.array([-2 * A, 0, 2 * A])

# شبیه‌سازی برای مقادیر مختلف SNR
for SNR_dB in SNR_dB_range:
    # تولید نویز گوسی با واریانس مناسب
    noise = np.random.normal(0, np.sqrt(1 / (2 * 10**(SNR_dB / 10))), size=signal.shape)
    
    # سیگنال دریافتی
    received_signal = signal + noise
    
    # آشکارسازی
    detected_symbols = np.zeros(received_signal.shape)
    detected_symbols[received_signal < thresholds[0]] = -3 * A  # A3-
    detected_symbols[(received_signal >= thresholds[0]) & (received_signal < thresholds[1])] = -A  # A-
    detected_symbols[(received_signal >= thresholds[1]) & (received_signal < thresholds[2])] = A  # A
    detected_symbols[received_signal >= thresholds[2]] = 3 * A  # A3
    
    # محاسبه احتمال خطا
    num_errors = np.sum(detected_symbols != symbols)
    BER_simulated.append(num_errors / num_symbols)

# محاسبه احتمال خطای نظری (BER)
BER_theoretical = (3 / 2) * Q(np.sqrt(SNR_linear / 5))

# رسم منحنی BER
plt.figure(figsize=(8, 6))
plt.semilogy(SNR_dB_range, BER_theoretical, label="Theoretical BER (4-PAM)", marker='o')
plt.semilogy(SNR_dB_range, BER_simulated, label="Simulated BER (4-PAM)", marker='x')
plt.title("BER vs SNR for 4-PAM with Raised Cosine Pulse (Theoretical vs Simulated)")
plt.xlabel("SNR (dB)")
plt.ylabel("BER")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
