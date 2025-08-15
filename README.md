# Digital Signal Processing Filter Implementation

**A comprehensive implementation of IIR digital filtering with frequency domain analysis and audio processing capabilities.**

---

### Key Features:
* **IIR Filter Design**: Implementation of Infinite Impulse Response filter with configurable parameters
* **Frequency Domain Analysis**: Complete DTFT spectrum computation and visualization
* **Time Domain Processing**: Multi-frequency test signal generation and filtering
* **Audio Output**: WAV file generation for audible verification of filter performance
* **Mathematical Visualization**: Detailed plots of magnitude/phase responses and time-domain signals

### Tech Stack:
* **Languages:** Python
* **Key Libraries/Frameworks:** NumPy, SciPy, Matplotlib
* **Mathematical Tools:** Discrete-Time Fourier Transform, Z-Transform, Digital Filter Theory

### What I Learned
This project deepened my understanding of fundamental signal processing concepts:
* **Digital Filter Theory**: Mastered the mathematical foundations of IIR filter design, including pole-zero placement and stability analysis
* **Frequency Domain Analysis**: Implemented DTFT computation from first principles, gaining insight into spectral analysis techniques crucial for robotics sensor processing
* **Real-Time Processing Concepts**: Developed understanding of difference equations and recursive filtering that directly applies to real-time control systems
* **Audio Signal Processing**: Gained experience with sampling rates, quantization, and audio file formats that translate to sensor data acquisition in robotics
* **Mathematical Programming**: Strengthened skills in translating complex mathematical equations into efficient, readable code

### Mathematical Foundation

#### Filter Design
The IIR filter implements a second-order resonator with the transfer function:
```
H(z) = G / (1 - 2R·cos(ω₀)·z⁻¹ + R²·z⁻²)
```

Where:
- `R` = pole radius (controls bandwidth)
- `ω₀` = center frequency in radians/sample
- `G` = gain normalization factor

#### Difference Equation
The filter is implemented using the time-domain difference equation:
```
y[n] = 2R·cos(ω₀)·y[n-1] - R²·y[n-2] + G·x[n]
```

### Filter Specifications
- **Type**: IIR (Infinite Impulse Response) Digital Filter
- **Order**: Second-order (biquad)
- **Implementation**: Direct Form II difference equation
- **Sampling Rate**: 20 kHz (configurable)
- **Test Signal**: Multi-frequency cosine sum at π/10, π/5, and 3π/10 rad/sample

### Project Structure
```
Digital_Signal_Processing_Filter/
├── dsp_filter.py          # Main implementation with DSPFilter class
├── requirements.txt       # Python dependencies
├── output/               # Generated plots and audio files
│   ├── filter_response.png
│   ├── input_spectrum.png
│   ├── output_spectrum.png
│   ├── time_domain_analysis.png
│   ├── input_signal.wav
│   └── output_signal.wav
└── README.md
```

### How to Run It

#### Prerequisites
Make sure you have Python 3.7+ installed on your system.

#### Setup and Execution
1. Clone the repository:
   ```bash
   git clone https://github.com/Janga786/Digital_Signal_Processing_Filter.git
   cd Digital_Signal_Processing_Filter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the complete analysis:
   ```bash
   python dsp_filter.py
   ```

#### Expected Output
The program will generate:
- **Frequency domain plots**: Magnitude and phase spectra of input/output signals
- **Filter response plots**: Comprehensive analysis of the designed filter
- **Time domain plots**: Signal comparison and steady-state analysis
- **Audio files**: WAV files for audible verification of filtering effects
- **Console output**: Detailed filter specifications and parameters

### Example Usage
```python
from dsp_filter import DSPFilter

# Create filter instance
filter_system = DSPFilter(sampling_rate=20000, duration=2)

# Generate and process signal
input_signal = filter_system.generate_test_signal()
b, a = filter_system.design_iir_filter(R=0.95, center_freq_ratio=1/5)
output_signal = filter_system.apply_filter(input_signal)

# Analyze results
filter_system.compute_dtft_spectrum(output_signal, "Filtered Output")
filter_system.save_audio_files()
```

### Technical Applications
This implementation demonstrates concepts directly applicable to:
- **Robotics**: Sensor data filtering for IMUs, encoders, and vision systems
- **Control Systems**: Real-time signal conditioning for feedback loops
- **Audio Processing**: Digital effects and noise reduction algorithms
- **Communications**: Channel equalization and interference rejection

### Advanced Features
- **Configurable Parameters**: Easy adjustment of filter characteristics
- **Comprehensive Analysis**: Both frequency and time domain insights
- **Professional Visualization**: Publication-quality plots with proper labeling
- **Audio Verification**: Listen to the filtering effects
- **Modular Design**: Clean OOP structure for easy extension

### Performance Considerations
- **Numerical Stability**: Careful handling of recursive computations
- **Memory Efficiency**: Optimized for large signal processing
- **Vectorized Operations**: NumPy-based implementation for speed
- **Visualization Quality**: High-DPI output suitable for presentations

This project showcases both theoretical understanding and practical implementation skills essential for signal processing applications in modern robotics and embedded systems.