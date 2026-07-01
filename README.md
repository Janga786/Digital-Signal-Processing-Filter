# Digital Signal Processing: Second-Order IIR Resonator

A Python implementation of a second-order IIR bandpass (resonator) filter, demonstrated on a multi-tone test signal. The project covers the full analysis pipeline: signal generation, spectral analysis via direct evaluation of the discrete-time Fourier transform (DTFT), filter design and frequency-response analysis, time-domain filtering with the recursive difference equation, and export of the results as plots and WAV audio files.

## What it does

- Generates a 2-second test signal at a 20 kHz sampling rate: the sum of three cosines at digital frequencies pi/10, pi/5, and 3pi/10 radians/sample.
- Computes the magnitude and phase spectra of the input and output signals by evaluating the DTFT directly on an 801-point frequency grid over [0, pi].
- Designs a second-order IIR resonator with pole radius R = 0.95 and center frequency omega_0 = pi/5, with the gain normalized so the response at the center frequency is unity.
- Plots the filter's magnitude and phase response using `scipy.signal.freqz`.
- Applies the filter sample by sample with its difference equation and plots both the transient (first 201 samples) and steady-state segments of the output.
- Writes the input and filtered signals to 16-bit WAV files so the effect of the filter is audible: the pi/5 tone passes through while the other two tones are attenuated.

## Theory

The filter is a second-order resonator with transfer function

```
H(z) = G / (1 - 2R cos(omega_0) z^-1 + R^2 z^-2)
```

Its poles sit at `z = R e^(+/- j omega_0)`, i.e. at radius R = 0.95 just inside the unit circle at angles of +/- pi/5. Placing the poles close to the unit circle produces a narrow passband centered on omega_0; the pole radius controls the bandwidth. The gain

```
G = (1 - R) / sqrt(1 - 2R cos(2 omega_0) + R^2)
```

normalizes the peak of the magnitude response to approximately 1. In the time domain the filter is realized by the recursive difference equation

```
y[n] = 2R cos(omega_0) y[n-1] - R^2 y[n-2] + G x[n]
```

Applied to the three-tone test signal, the resonator passes the pi/5 component and attenuates the components at pi/10 and 3pi/10.

## Repository layout

```
Digital-Signal-Processing-Filter/
├── dsp_filter.py          # Class-based implementation (DSPFilter) with full analysis pipeline
├── DSP_Project/
│   ├── main.py            # Original script version of the same analysis
│   ├── input_signal.wav   # Pre-generated example: unfiltered three-tone signal
│   └── output_signal.wav  # Pre-generated example: filtered (single-tone) result
├── requirements.txt
├── LICENSE
└── README.md
```

## Setup and usage

Requires Python 3.9+.

```bash
git clone https://github.com/Janga786/Digital-Signal-Processing-Filter.git
cd Digital-Signal-Processing-Filter
pip install -r requirements.txt
python dsp_filter.py
```

Each figure is displayed interactively and also saved to an `output/` directory; close each plot window to advance to the next step.

The `DSPFilter` class can also be used directly:

```python
from dsp_filter import DSPFilter

filter_system = DSPFilter(sampling_rate=20000, duration=2)
x = filter_system.generate_test_signal()
b, a = filter_system.design_iir_filter(R=0.95, center_freq_ratio=1/5)
y = filter_system.apply_filter(x)
filter_system.save_audio_files()
```

## Output

Running `dsp_filter.py` produces the following files in `output/`:

| File | Contents |
| --- | --- |
| `input_signal_spectrum.png` | Magnitude and phase spectra of the three-tone input |
| `filter_response.png` | Magnitude and phase response of the designed resonator |
| `output_signal_spectrum.png` | Magnitude and phase spectra of the filtered output |
| `time_domain_analysis.png` | Transient and steady-state stem plots, input/output comparison |
| `input_signal.wav`, `output_signal.wav` | Audio of the signal before and after filtering |

The console prints the filter specifications, for example:

```
Filter Type: IIR (Infinite Impulse Response)
Sampling Rate: 20000 Hz
Signal Duration: 2 seconds
Total Samples: 40000

Filter Parameters:
  Pole Radius (R): 0.95
  Center Frequency: 0.6283 rad/sample (2000.0 Hz)
  Gain (G): 0.0436

Filter Coefficients:
  Numerator (b): [0.0436, 0, 0]
  Denominator (a): [1, -1.5371, 0.9025]
```

Pre-generated example WAV files from the script version are included in `DSP_Project/`.

## Dependencies

- NumPy
- SciPy
- Matplotlib

## License

MIT License. See [LICENSE](LICENSE).
