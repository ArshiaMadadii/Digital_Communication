# Digital_Communication

# The first project :

# PAM Baseband Transmission Simulation

## Overview (English)
This project simulates a baseband transmission system using **PAM** (Pulse Amplitude Modulation) with raised cosine pulses. The aim is to generate random bit streams, modulate them into a signal, add Gaussian noise, and analyze the performance.

### Steps:
1. **Bit Stream Generation**: Create a random binary sequence.
2. **Modulation**: Use PAM-1 with raised cosine pulses to modulate the bit stream.
3. **Noise Addition**: Add Gaussian noise to the modulated signal for a specific Signal-to-Noise Ratio (SNR).
4. **Detection**: Sample the received signal and use zero-threshold detection to identify transmitted bits.
5. **Error Analysis**: Compare detected bits with transmitted bits to calculate the Bit Error Rate (BER).
6. **Theoretical Comparison**: Plot the SNR vs. BER curve and compare with theoretical results.

### Extended Experiment:
- **Multiple Amplitudes**: Repeat the simulation with varying amplitudes: 
  - Case 1: \( A, -A \)
  - Case 2: \( A, -A, 3A, -3A \)
  - Case 3: \( -2A, 0, 2A \)
- Use multiple thresholds for detection in higher-order cases.

---

## مرور کلی (فارسی)
این پروژه شبیه‌سازی سیستم انتقال باند پایه با استفاده از **PAM** (مدولاسیون دامنه پالسی) و پالس‌های با کسینوس بالارونده را انجام می‌دهد. هدف تولید رشته‌های بیت تصادفی، مدولاسیون آن‌ها به سیگنال، افزودن نویز گوسی و تحلیل عملکرد سیستم است.

### مراحل:
1. **تولید رشته بیت**: ایجاد توالی باینری تصادفی.
2. **مدولاسیون**: استفاده از PAM-1 با پالس‌های کسینوس بالارونده برای مدوله‌کردن توالی بیت.
3. **اضافه کردن نویز**: افزودن نویز گوسی به سیگنال مدوله‌شده برای یک نسبت سیگنال به نویز مشخص.
4. **آشکارسازی**: نمونه‌برداری از سیگنال دریافتی و استفاده از آشکارساز صفر به منظور شناسایی بیت‌های ارسال‌شده.
5. **تحلیل خطا**: مقایسه بیت‌های آشکارسازی‌شده با بیت‌های ارسال‌شده برای محاسبه نرخ خطای بیت (BER).
6. **مقایسه نظری**: رسم منحنی SNR در برابر BER و مقایسه با نتایج تئوری.

### آزمایش‌های تکمیلی:
- **دامنه‌های مختلف**: شبیه‌سازی را با دامنه‌های متفاوت تکرار کنید:
  - حالت 1: \( A, -A \)
  - حالت 2: \( A, -A, 3A, -3A \)
  - حالت 3: \( -2A, 0, 2A \)
- از آستانه‌های مختلف برای آشکارسازی در حالت‌های مرتبه بالاتر استفاده کنید.

---

## Results
- Plot **SNR vs BER** for all cases.
- Compare simulation results with theoretical curves.

---

## Outputs:
- Graphs of **SNR vs BER** for varying amplitudes.
- Calculated BER values for each SNR level.

---

### Requirements
- Python/Matlab
- Libraries: numpy, matplotlib
