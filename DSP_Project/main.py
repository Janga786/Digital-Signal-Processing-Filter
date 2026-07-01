import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
from scipy.io.wavfile import write

# Problem 2
n = np.arange(201)
x = np.cos((np.pi/10) * n) + np.cos((np.pi/5) * n) + np.cos(((3*np.pi)/10) * n)

plt.figure()
plt.stem(n, x)
plt.xlabel('n')
plt.ylabel('x[n]')
plt.title('First 201 Samples of x[n]')
plt.show()


# Problem 3
omega = np.linspace(0, np.pi, 801)
fs = 20000
duration = 2
N = fs * duration
n_long = np.arange(N)
x_long = np.cos((np.pi/10) * n_long) + np.cos((np.pi/5) * n_long) + np.cos(((3*np.pi)/10) * n_long)
X = np.zeros(len(omega), dtype=complex)

for i, w in enumerate(omega):
    X[i] = np.sum(x_long * np.exp(-1j * w * n_long))

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(omega, np.abs(X))
plt.title('Magnitude Spectrum of x[n]')
plt.xlabel('ω (radians/sample)')
plt.ylabel('|X(ω)|')

plt.subplot(1, 2, 2)
plt.plot(omega, np.angle(X))
plt.title('Phase Spectrum of x[n]')
plt.xlabel('ω (radians/sample)')
plt.ylabel('Phase (radians)')
plt.tight_layout()
plt.show()

# Problem 6
R = 0.95
omega0 = np.pi / 5
G = (1 - R) / np.sqrt(1 - 2 * R * np.cos(2 * omega0) + R**2)

b = [G, 0, 0]
a = [1, -2 * R * np.cos(omega0), R**2]

omega, H = freqz(b, a, worN=801)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(omega, np.abs(H))
plt.title('Magnitude Spectrum of the Filter')
plt.xlabel('ω (radians/sample)')
plt.ylabel('|H(e^(jω))|')

plt.subplot(1, 2, 2)
plt.plot(omega, np.angle(H))
plt.title('Phase Spectrum of the Filter')
plt.xlabel('ω (radians/sample)')
plt.ylabel('Phase (radians)')
plt.tight_layout()
plt.show()

# Problem 9
y = np.zeros(N)

y[0] = 0
y[1] = 0

for n in range(2, N):
    y[n] = 2 * R * np.cos(omega0) * y[n-1] - R**2 * y[n-2] + G * x_long[n]

# Problem 10
plt.figure()
plt.stem(np.arange(201), y[:201])
plt.xlabel('n')
plt.ylabel('y[n]')
plt.title('Filter Output y[n] (First 201 Samples)')
plt.show()

# Problem 11
plt.figure()
plt.stem(np.arange(201), y[10000:10201])
plt.xlabel('n')
plt.ylabel('y[n]')
plt.title('Filter Output y[n] (Steady-State Segment)')
plt.show()

# Problem 12
omega_dtft = np.linspace(0, np.pi, 801)

Y = np.zeros(len(omega_dtft), dtype=complex)

for i, w in enumerate(omega_dtft):
    Y[i] = np.sum(y * np.exp(-1j * w * np.arange(N)))

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(omega_dtft, np.abs(Y))
plt.title('Magnitude Spectrum of Filtered Output')
plt.xlabel('ω (radians/sample)')
plt.ylabel('|Y(ω)|')

plt.subplot(1, 2, 2)
plt.plot(omega_dtft, np.angle(Y))
plt.title('Phase Spectrum of Filtered Output')
plt.xlabel('ω (radians/sample)')
plt.ylabel('Phase (radians)')
plt.tight_layout()
plt.show()

# Problem 13
x_norm = (x_long / np.max(np.abs(x_long)) * 32767).astype(np.int16)
y_norm = (y / np.max(np.abs(y)) * 32767).astype(np.int16)

write("input_signal.wav", fs, x_norm)
write("output_signal.wav", fs, y_norm)

print("WAV files 'input_signal.wav' and 'output_signal.wav' have been saved.")