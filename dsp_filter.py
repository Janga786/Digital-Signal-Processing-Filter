"""
Digital Signal Processing Filter Implementation
A comprehensive implementation of IIR filtering with frequency domain analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
from scipy.io.wavfile import write
import os


class DSPFilter:
    """
    Digital Signal Processing Filter class implementing IIR filtering
    with comprehensive frequency and time domain analysis.
    """
    
    def __init__(self, sampling_rate=20000, duration=2):
        """
        Initialize the DSP filter with sampling parameters.
        
        Args:
            sampling_rate (int): Sampling frequency in Hz
            duration (float): Signal duration in seconds
        """
        self.fs = sampling_rate
        self.duration = duration
        self.N = int(self.fs * self.duration)  # Total number of samples
        self.n = np.arange(self.N)
        
        # Create output directory for plots and audio files
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_test_signal(self):
        """
        Generate a multi-frequency test signal composed of three cosines.
        
        Returns:
            numpy.ndarray: The generated test signal
        """
        # Multi-frequency test signal: sum of three cosines at different frequencies
        self.x = (np.cos((np.pi/10) * self.n) + 
                  np.cos((np.pi/5) * self.n) + 
                  np.cos((3*np.pi/10) * self.n))
        return self.x
    
    def compute_dtft_spectrum(self, signal, title_prefix="Signal"):
        """
        Compute and plot the Discrete-Time Fourier Transform spectrum.
        
        Args:
            signal (numpy.ndarray): Input signal
            title_prefix (str): Prefix for plot titles
            
        Returns:
            tuple: (frequencies, complex spectrum)
        """
        omega = np.linspace(0, np.pi, 801)
        X = np.zeros(len(omega), dtype=complex)
        
        # Compute DTFT
        for i, w in enumerate(omega):
            X[i] = np.sum(signal * np.exp(-1j * w * np.arange(len(signal))))
        
        # Plot magnitude and phase spectra
        plt.figure(figsize=(14, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(omega, np.abs(X))
        plt.title(f'Magnitude Spectrum of {title_prefix}')
        plt.xlabel('ω (radians/sample)')
        plt.ylabel('|X(ω)|')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.plot(omega, np.angle(X))
        plt.title(f'Phase Spectrum of {title_prefix}')
        plt.xlabel('ω (radians/sample)')
        plt.ylabel('Phase (radians)')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/{title_prefix.lower()}_spectrum.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        return omega, X
    
    def design_iir_filter(self, R=0.95, center_freq_ratio=1/5):
        """
        Design an IIR (Infinite Impulse Response) filter.
        
        Args:
            R (float): Pole radius (controls filter bandwidth)
            center_freq_ratio (float): Center frequency as fraction of π
            
        Returns:
            tuple: (numerator coefficients, denominator coefficients)
        """
        self.R = R
        self.omega0 = np.pi * center_freq_ratio
        
        # Calculate gain for unity response at center frequency
        self.G = (1 - R) / np.sqrt(1 - 2 * R * np.cos(2 * self.omega0) + R**2)
        
        # Filter coefficients
        self.b = [self.G, 0, 0]  # Numerator (feedforward)
        self.a = [1, -2 * R * np.cos(self.omega0), R**2]  # Denominator (feedback)
        
        return self.b, self.a
    
    def analyze_filter_response(self):
        """
        Analyze and plot the designed filter's frequency response.
        """
        omega, H = freqz(self.b, self.a, worN=801)
        
        plt.figure(figsize=(14, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(omega, np.abs(H), 'b-', linewidth=2)
        plt.axvline(self.omega0, color='r', linestyle='--', alpha=0.7, 
                   label=f'Center frequency: {self.omega0:.3f} rad/sample')
        plt.title('Filter Magnitude Response')
        plt.xlabel('ω (radians/sample)')
        plt.ylabel('|H(e^(jω))|')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(omega, np.angle(H), 'b-', linewidth=2)
        plt.axvline(self.omega0, color='r', linestyle='--', alpha=0.7)
        plt.title('Filter Phase Response')
        plt.xlabel('ω (radians/sample)')
        plt.ylabel('Phase (radians)')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/filter_response.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        return omega, H
    
    def apply_filter(self, input_signal):
        """
        Apply the designed IIR filter to the input signal using difference equation.
        
        Args:
            input_signal (numpy.ndarray): Input signal
            
        Returns:
            numpy.ndarray: Filtered output signal
        """
        self.y = np.zeros(len(input_signal))
        
        # Initialize first two samples
        self.y[0] = 0
        if len(input_signal) > 1:
            self.y[1] = 0
        
        # Apply difference equation: y[n] = -a[1]*y[n-1] - a[2]*y[n-2] + b[0]*x[n]
        for n in range(2, len(input_signal)):
            self.y[n] = (2 * self.R * np.cos(self.omega0) * self.y[n-1] - 
                        self.R**2 * self.y[n-2] + 
                        self.G * input_signal[n])
        
        return self.y
    
    def plot_time_domain_signals(self, samples_to_plot=201):
        """
        Plot time domain representations of input and output signals.
        
        Args:
            samples_to_plot (int): Number of samples to display
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Input signal - first samples
        axes[0, 0].stem(np.arange(samples_to_plot), self.x[:samples_to_plot], 
                       use_line_collection=True)
        axes[0, 0].set_title('Input Signal x[n] (First 201 Samples)')
        axes[0, 0].set_xlabel('Sample Number (n)')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Output signal - first samples
        axes[0, 1].stem(np.arange(samples_to_plot), self.y[:samples_to_plot], 
                       use_line_collection=True)
        axes[0, 1].set_title('Filter Output y[n] (First 201 Samples)')
        axes[0, 1].set_xlabel('Sample Number (n)')
        axes[0, 1].set_ylabel('Amplitude')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Output signal - steady state
        steady_start = 10000
        steady_samples = np.arange(samples_to_plot)
        axes[1, 0].stem(steady_samples, self.y[steady_start:steady_start+samples_to_plot], 
                       use_line_collection=True)
        axes[1, 0].set_title('Filter Output y[n] (Steady-State)')
        axes[1, 0].set_xlabel('Sample Number (relative)')
        axes[1, 0].set_ylabel('Amplitude')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Comparison of input vs output
        comparison_range = slice(0, min(500, len(self.x)))
        axes[1, 1].plot(self.x[comparison_range], 'b-', alpha=0.7, label='Input')
        axes[1, 1].plot(self.y[comparison_range], 'r-', alpha=0.7, label='Output')
        axes[1, 1].set_title('Input vs Output Comparison')
        axes[1, 1].set_xlabel('Sample Number (n)')
        axes[1, 1].set_ylabel('Amplitude')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/time_domain_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_audio_files(self):
        """
        Save input and output signals as WAV audio files for listening analysis.
        """
        # Normalize to 16-bit integer range
        x_norm = (self.x / np.max(np.abs(self.x)) * 32767).astype(np.int16)
        y_norm = (self.y / np.max(np.abs(self.y)) * 32767).astype(np.int16)
        
        # Save WAV files
        input_path = f"{self.output_dir}/input_signal.wav"
        output_path = f"{self.output_dir}/output_signal.wav"
        
        write(input_path, self.fs, x_norm)
        write(output_path, self.fs, y_norm)
        
        print(f"Audio files saved:")
        print(f"  Input signal: {input_path}")
        print(f"  Output signal: {output_path}")
        
        return input_path, output_path
    
    def print_filter_specifications(self):
        """
        Print detailed filter specifications and parameters.
        """
        print("\n" + "="*50)
        print("DIGITAL FILTER SPECIFICATIONS")
        print("="*50)
        print(f"Filter Type: IIR (Infinite Impulse Response)")
        print(f"Sampling Rate: {self.fs} Hz")
        print(f"Signal Duration: {self.duration} seconds")
        print(f"Total Samples: {self.N}")
        print(f"\nFilter Parameters:")
        print(f"  Pole Radius (R): {self.R}")
        print(f"  Center Frequency: {self.omega0:.4f} rad/sample ({self.omega0*self.fs/(2*np.pi):.1f} Hz)")
        print(f"  Gain (G): {self.G:.4f}")
        print(f"\nFilter Coefficients:")
        print(f"  Numerator (b): {self.b}")
        print(f"  Denominator (a): {self.a}")
        print("="*50)


def main():
    """
    Main function demonstrating the complete DSP filter analysis pipeline.
    """
    print("Digital Signal Processing Filter Analysis")
    print("=" * 50)
    
    # Initialize DSP filter
    filter_system = DSPFilter(sampling_rate=20000, duration=2)
    
    # Generate test signal
    print("1. Generating multi-frequency test signal...")
    input_signal = filter_system.generate_test_signal()
    
    # Analyze input signal spectrum
    print("2. Computing input signal spectrum...")
    filter_system.compute_dtft_spectrum(input_signal, "Input Signal")
    
    # Design IIR filter
    print("3. Designing IIR filter...")
    b, a = filter_system.design_iir_filter(R=0.95, center_freq_ratio=1/5)
    
    # Analyze filter response
    print("4. Analyzing filter frequency response...")
    filter_system.analyze_filter_response()
    
    # Apply filter
    print("5. Applying filter to input signal...")
    output_signal = filter_system.apply_filter(input_signal)
    
    # Analyze output signal spectrum
    print("6. Computing output signal spectrum...")
    filter_system.compute_dtft_spectrum(output_signal, "Output Signal")
    
    # Time domain analysis
    print("7. Performing time domain analysis...")
    filter_system.plot_time_domain_signals()
    
    # Save audio files
    print("8. Saving audio files...")
    filter_system.save_audio_files()
    
    # Print specifications
    filter_system.print_filter_specifications()
    
    print(f"\nAnalysis complete! Check the '{filter_system.output_dir}' directory for all generated files.")


if __name__ == "__main__":
    main()