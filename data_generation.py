import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import norm
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PIL import Image as PILImage
import shutil


class SpectralDataGenerator:
    """
    Class to generate and simulate spectral data with realistic characteristics
    such as peaks, baseline drift, and noise.
    """

    def __init__(self, params=None):
        """
        Initialize the spectral data generator with parameters.

        Args:
            params (dict, optional): Dictionary of parameters for data generation
        """
        # Default parameters
        self.default_params = {
            # X-axis parameters
            "x_min": 0.0,  # Start of x range
            "x_max": 10.0,  # End of x range
            "num_points": 1000,  # Number of data points

            # Baseline parameters
            "baseline_type": "polynomial",  # polynomial, exponential, or sinusoidal
            "baseline_params": {
                "polynomial_coeffs": [0.05, -0.01, 0.001],  # For polynomial: [c0, c1, c2, ...]
                "exp_amplitude": 0.1,  # For exponential
                "exp_decay": 0.5,  # For exponential
                "sin_amplitude": 0.05,  # For sinusoidal
                "sin_frequency": 0.5,  # For sinusoidal
                "sin_phase": 0.0  # For sinusoidal
            },

            # Peak parameters
            "num_peaks": 5,  # Number of peaks
            "peak_types": ["gaussian"],  # Types of peaks: gaussian, lorentzian, voigt
            "peak_positions": None,  # If None, will be randomly generated
            "peak_heights": None,  # If None, will be randomly generated
            "peak_widths": None,  # If None, will be randomly generated
            "min_peak_height": 0.2,  # Minimum random peak height
            "max_peak_height": 1.0,  # Maximum random peak height
            "min_peak_width": 0.05,  # Minimum random peak width
            "max_peak_width": 0.2,  # Maximum random peak width

            # Noise parameters
            "noise_level": 0.01,  # Gaussian noise standard deviation
            "noise_type": "gaussian",  # gaussian or poisson

            # Artifact parameters
            "add_spikes": False,  # Whether to add sharp spikes
            "spike_probability": 0.005,  # Probability of a spike at each point
            "max_spike_height": 0.5,  # Maximum spike height

            # Output parameters
            "output_dir": "simulated_data",  # Output directory
            "file_prefix": "sim-spec",  # Prefix for output files
        }

        # Update with user-provided parameters
        self.params = self.default_params.copy()
        if params:
            self.update_params(params)

        # Create output directory structure
        self._create_output_directories()

    def _create_output_directories(self):
        """Create the output directory structure."""
        # Main output directory
        if not os.path.exists(self.params["output_dir"]):
            os.makedirs(self.params["output_dir"])

        # Data directory for CSV files
        data_dir = os.path.join(self.params["output_dir"], "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Peak info directory
        peak_info_dir = os.path.join(self.params["output_dir"], "peak_info")
        if not os.path.exists(peak_info_dir):
            os.makedirs(peak_info_dir)

        # Images directory for plots
        images_dir = os.path.join(self.params["output_dir"], "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

    def update_params(self, new_params):
        """
        Update parameters with new values.

        Args:
            new_params (dict): New parameters to update
        """
        # Update top-level parameters
        for key, value in new_params.items():
            if key == "baseline_params" and isinstance(value, dict):
                # Update nested baseline parameters
                if key not in self.params:
                    self.params[key] = {}
                for subkey, subvalue in value.items():
                    self.params[key][subkey] = subvalue
            else:
                self.params[key] = value

    def generate_x_axis(self):
        """
        Generate evenly spaced x-axis values.

        Returns:
            numpy.ndarray: X-axis values
        """
        return np.linspace(
            self.params["x_min"],
            self.params["x_max"],
            self.params["num_points"]
        )

    def generate_baseline(self, x):
        """
        Generate baseline based on specified type.

        Args:
            x (numpy.ndarray): X-axis values

        Returns:
            numpy.ndarray: Baseline values
        """
        baseline_type = self.params["baseline_type"]
        baseline_params = self.params["baseline_params"]

        if baseline_type == "polynomial":
            # Polynomial baseline: c0 + c1*x + c2*x^2 + ...
            coeffs = baseline_params.get("polynomial_coeffs", [0.0, 0.0])
            baseline = np.zeros_like(x)
            for i, coeff in enumerate(coeffs):
                baseline += coeff * x ** i

        elif baseline_type == "exponential":
            # Exponential baseline: a * exp(-b*x)
            amp = baseline_params.get("exp_amplitude", 0.1)
            decay = baseline_params.get("exp_decay", 0.5)
            baseline = amp * np.exp(-decay * x)

        elif baseline_type == "sinusoidal":
            # Sinusoidal baseline: a * sin(f*x + p)
            amp = baseline_params.get("sin_amplitude", 0.05)
            freq = baseline_params.get("sin_frequency", 0.5)
            phase = baseline_params.get("sin_phase", 0.0)
            baseline = amp * np.sin(2 * np.pi * freq * x + phase)

        else:
            # Default to flat baseline
            baseline = np.zeros_like(x)

        # Ensure baseline is non-negative
        return np.maximum(baseline, 0)

    def generate_gaussian_peak(self, x, position, height, width):
        """
        Generate a Gaussian peak.

        Args:
            x (numpy.ndarray): X-axis values
            position (float): Peak center position
            height (float): Peak height
            width (float): Peak width (sigma)

        Returns:
            numpy.ndarray: Gaussian peak values
        """
        return height * np.exp(-0.5 * ((x - position) / width) ** 2)

    def generate_lorentzian_peak(self, x, position, height, width):
        """
        Generate a Lorentzian peak.

        Args:
            x (numpy.ndarray): X-axis values
            position (float): Peak center position
            height (float): Peak height
            width (float): Peak width (FWHM)

        Returns:
            numpy.ndarray: Lorentzian peak values
        """
        return height * (width ** 2 / ((x - position) ** 2 + width ** 2))

    def generate_voigt_peak(self, x, position, height, width, mixing=0.5):
        """
        Generate a Voigt peak (convolution of Gaussian and Lorentzian).
        Approximated as a weighted sum.

        Args:
            x (numpy.ndarray): X-axis values
            position (float): Peak center position
            height (float): Peak height
            width (float): Peak width
            mixing (float): Mixing parameter between Gaussian and Lorentzian (0-1)

        Returns:
            numpy.ndarray: Voigt peak values
        """
        gaussian = self.generate_gaussian_peak(x, position, height, width)
        lorentzian = self.generate_lorentzian_peak(x, position, height, width)
        return mixing * gaussian + (1 - mixing) * lorentzian

    def generate_peaks(self, x):
        """
        Generate peaks based on specified parameters.

        Args:
            x (numpy.ndarray): X-axis values

        Returns:
            tuple: (peak values, peak information)
        """
        num_peaks = self.params["num_peaks"]
        peak_info = []

        # Check if peak positions are provided, otherwise generate random ones
        if self.params["peak_positions"] is None:
            # Generate random peak positions within x range (with margin)
            margin = 0.1 * (self.params["x_max"] - self.params["x_min"])
            peak_positions = np.random.uniform(
                self.params["x_min"] + margin,
                self.params["x_max"] - margin,
                num_peaks
            )
        else:
            peak_positions = self.params["peak_positions"]
            # Adjust num_peaks if positions are provided
            num_peaks = len(peak_positions)

        # Check if peak heights are provided, otherwise generate random ones
        if self.params["peak_heights"] is None:
            peak_heights = np.random.uniform(
                self.params["min_peak_height"],
                self.params["max_peak_height"],
                num_peaks
            )
        else:
            peak_heights = self.params["peak_heights"]

        # Check if peak widths are provided, otherwise generate random ones
        if self.params["peak_widths"] is None:
            peak_widths = np.random.uniform(
                self.params["min_peak_width"],
                self.params["max_peak_width"],
                num_peaks
            )
        else:
            peak_widths = self.params["peak_widths"]

        # Ensure all arrays have the same length
        num_peaks = min(len(peak_positions), len(peak_heights), len(peak_widths))

        # Initialize the peaks array
        peaks = np.zeros_like(x)

        # Generate each peak
        for i in range(num_peaks):
            position = peak_positions[i]
            height = peak_heights[i]
            width = peak_widths[i]

            # Determine peak type
            peak_types = self.params["peak_types"]
            peak_type = peak_types[i % len(peak_types)]

            # Generate peak based on type
            if peak_type == "gaussian":
                peak = self.generate_gaussian_peak(x, position, height, width)
            elif peak_type == "lorentzian":
                peak = self.generate_lorentzian_peak(x, position, height, width)
            elif peak_type == "voigt":
                peak = self.generate_voigt_peak(x, position, height, width)
            else:
                # Default to gaussian
                peak = self.generate_gaussian_peak(x, position, height, width)

            # Add peak to total
            peaks += peak

            # Save peak information
            peak_info.append({
                "type": peak_type,
                "position": position,
                "height": height,
                "width": width
            })

        return peaks, peak_info

    def add_noise(self, y):
        """
        Add noise to the spectral data.

        Args:
            y (numpy.ndarray): Y-axis values

        Returns:
            numpy.ndarray: Y-axis values with noise
        """
        noise_level = self.params["noise_level"]
        noise_type = self.params["noise_type"]

        if noise_level <= 0:
            return y

        if noise_type == "gaussian":
            # Gaussian noise
            noise = np.random.normal(0, noise_level, size=len(y))
        elif noise_type == "poisson":
            # Poisson noise (scaled by signal intensity)
            noise = np.random.poisson(np.maximum(y, 0) / noise_level) * noise_level - y
        else:
            # Default to gaussian
            noise = np.random.normal(0, noise_level, size=len(y))

        return y + noise

    def add_artifacts(self, x, y):
        """
        Add artifacts like spikes to the spectral data.

        Args:
            x (numpy.ndarray): X-axis values
            y (numpy.ndarray): Y-axis values

        Returns:
            numpy.ndarray: Y-axis values with artifacts
        """
        if not self.params["add_spikes"]:
            return y

        # Add random spikes
        spike_mask = np.random.random(len(x)) < self.params["spike_probability"]
        spike_heights = np.random.uniform(0, self.params["max_spike_height"], size=len(x))
        y_with_spikes = y.copy()
        y_with_spikes[spike_mask] += spike_heights[spike_mask]

        return y_with_spikes

    def generate_spectrum(self):
        """
        Generate a complete spectrum with baseline, peaks, noise, and artifacts.

        Returns:
            tuple: (x, y, components) where components is a dict with individual components
        """
        # Generate x-axis
        x = self.generate_x_axis()

        # Generate baseline
        baseline = self.generate_baseline(x)

        # Generate peaks
        peaks, peak_info = self.generate_peaks(x)

        # Combine baseline and peaks
        y_clean = baseline + peaks

        # Add noise
        y_noisy = self.add_noise(y_clean)

        # Add artifacts
        y_final = self.add_artifacts(x, y_noisy)

        # Return x, y and components for reference
        components = {
            "baseline": baseline,
            "peaks": peaks,
            "peak_info": peak_info,
            "y_clean": y_clean,
            "y_noisy": y_noisy
        }

        return x, y_final, components

    def save_spectrum(self, x, y, filename=None, include_components=False, components=None):
        """
        Save the generated spectrum to a CSV file.

        Args:
            x (numpy.ndarray): X-axis values
            y (numpy.ndarray): Y-axis values
            filename (str, optional): Output filename. If None, a default name will be generated.
            include_components (bool): Whether to save individual components
            components (dict, optional): Components dictionary from generate_spectrum

        Returns:
            str: Saved filename
        """
        # Generate filename if not provided
        if filename is None:
            timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
            filename = f"{self.params['file_prefix']}-{timestamp}.csv"

        # Ensure the filename has a .csv extension
        if not filename.endswith(".csv"):
            filename += ".csv"

        # Full path to data directory
        data_dir = os.path.join(self.params["output_dir"], "data")
        filepath = os.path.join(data_dir, filename)

        # Save main spectrum
        df = pd.DataFrame({"x": x, "y": y})
        df.to_csv(filepath, index=False)

        # Optionally save components
        if include_components and components:
            components_filepath = os.path.join(
                data_dir,
                f"{os.path.splitext(filename)[0]}_components.csv"
            )

            # Create a DataFrame with all components
            df_components = pd.DataFrame({
                "x": x,
                "y": y,
                "baseline": components["baseline"],
                "peaks": components["peaks"],
                "y_clean": components["y_clean"],
                "y_noisy": components["y_noisy"]
            })

            df_components.to_csv(components_filepath, index=False)

            # Save peak information
            peak_info_dir = os.path.join(self.params["output_dir"], "peak_info")
            peak_info_filepath = os.path.join(
                peak_info_dir,
                f"{os.path.splitext(filename)[0]}_peak_info.csv"
            )

            df_peak_info = pd.DataFrame(components["peak_info"])
            df_peak_info.to_csv(peak_info_filepath, index=False)

        return filepath

    def plot_spectrum(self, x, y, components=None, show_components=True, show_peaks=True,
                      title=None, save=False, filename=None):
        """
        Plot the generated spectrum.

        Args:
            x (numpy.ndarray): X-axis values
            y (numpy.ndarray): Y-axis values
            components (dict, optional): Components dictionary from generate_spectrum
            show_components (bool): Whether to show individual components
            show_peaks (bool): Whether to highlight individual peaks
            title (str, optional): Plot title
            save (bool): Whether to save the plot
            filename (str, optional): Output filename for the plot

        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot main spectrum
        ax.plot(x, y, 'b-', label='Spectrum', alpha=0.7)

        if components and show_components:
            # Plot baseline
            ax.plot(x, components["baseline"], 'r--', label='Baseline')

            # Plot clean spectrum (without noise)
            ax.plot(x, components["y_clean"], 'g-', label='Clean Spectrum', alpha=0.5)

        if components and show_peaks:
            # Highlight individual peaks
            for i, peak_info in enumerate(components["peak_info"]):
                position = peak_info["position"]
                height = peak_info["height"]
                width = peak_info["width"]
                peak_type = peak_info["type"]

                # Find nearest index to peak position
                idx = np.abs(x - position).argmin()

                # Only label every other peak to avoid crowding
                if i % 2 == 0:
                    label = f"Peak {i + 1}"
                else:
                    label = None

                # Mark peak position
                ax.plot(position, components["baseline"][idx] + height, 'ro', markersize=8)

                # Annotate peak
                ax.annotate(
                    f"{position:.2f}",
                    (position, components["baseline"][idx] + height),
                    xytext=(0, 10),
                    textcoords="offset points",
                    ha='center',
                    fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
                )

                # Calculate and plot peak region
                # Width factor is different for different peak types
                if peak_type == "gaussian":
                    width_factor = 2.5  # About ±2.5 sigma for 99% of Gaussian peak
                elif peak_type == "lorentzian":
                    width_factor = 5.0  # Lorentzians have longer tails
                else:
                    width_factor = 3.0  # Compromise for Voigt

                peak_start = max(0, np.abs(x - (position - width_factor * width)).argmin())
                peak_end = min(len(x) - 1, np.abs(x - (position + width_factor * width)).argmin())

                # Fill peak area
                ax.fill_between(
                    x[peak_start:peak_end],
                    components["baseline"][peak_start:peak_end],
                    components["y_clean"][peak_start:peak_end],
                    alpha=0.2,
                    color='green',
                    label=label
                )

        # Set title and labels
        if title:
            ax.set_title(title)
        else:
            ax.set_title("Simulated Spectrum")

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)

        # Handle legend entries to avoid duplicates
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')

        plt.tight_layout()

        # Save if requested
        if save:
            if filename is None:
                timestamp = pd.Timestamp.now().strftime("%Y%m%d%H%M%S")
                filename = f"{self.params['file_prefix']}-{timestamp}.png"

            # Ensure the filename has a .png extension
            if not filename.endswith((".png", ".jpg", ".pdf")):
                filename += ".png"

            # Full path to images directory
            images_dir = os.path.join(self.params["output_dir"], "images")
            filepath = os.path.join(images_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')

            return fig, filepath

        return fig, None

    def generate_dataset(self, n_spectra=5, vary_params=True, save=True, plot=True):
        """
        Generate a dataset of multiple spectra with optional parameter variation.

        Args:
            n_spectra (int): Number of spectra to generate
            vary_params (bool): Whether to vary parameters between spectra
            save (bool): Whether to save the spectra
            plot (bool): Whether to plot the spectra

        Returns:
            list: List of generated spectra as (x, y, components) tuples
        """
        spectra = []
        plot_filepaths = []

        for i in range(n_spectra):
            # Optionally vary parameters
            if vary_params and i > 0:
                self._vary_parameters(i)

            # Generate spectrum
            x, y, components = self.generate_spectrum()
            spectra.append((x, y, components))

            # Generate filenames
            csv_filename = f"{self.params['file_prefix']}-{i + 1:02d}.csv"
            plot_filename = f"{self.params['file_prefix']}-{i + 1:02d}.png"

            # Save if requested
            if save:
                self.save_spectrum(x, y, csv_filename, include_components=True, components=components)

            # Plot if requested
            if plot:
                title = f"Simulated Spectrum {i + 1}"
                _, filepath = self.plot_spectrum(
                    x, y, components, title=title,
                    save=save, filename=plot_filename
                )
                if filepath:
                    plot_filepaths.append(filepath)

        # Generate PDF report with all plots
        if save and plot:
            self.generate_pdf_report(plot_filepaths)

        return spectra

    def generate_pdf_report(self, image_filepaths=None):
        """
        Generate a PDF report containing all the PNG images.

        Args:
            image_filepaths (list, optional): List of image filepaths to include

        Returns:
            str: Path to the generated PDF file
        """
        pdf_path = os.path.join(self.params["output_dir"], "report.pdf")

        # If no image filepaths provided, find all PNGs in the images directory
        if not image_filepaths:
            images_dir = os.path.join(self.params["output_dir"], "images")
            image_filepaths = [
                os.path.join(images_dir, f)
                for f in os.listdir(images_dir)
                if f.endswith(".png")
            ]
            image_filepaths.sort()

        if not image_filepaths:
            print("No images found to include in the PDF report.")
            return None

        # Create the PDF document
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter
        )

        # Get styles for text
        styles = getSampleStyleSheet()

        # Create the content for the PDF
        content = []

        # Add a title
        content.append(Paragraph(f"Spectral Data Simulation Report", styles['Title']))
        content.append(Spacer(1, 0.2 * inch))

        # Add information about the simulation parameters
        content.append(Paragraph("Simulation Parameters:", styles['Heading2']))
        content.append(Spacer(1, 0.1 * inch))

        param_text = [
            f"X Range: {self.params['x_min']} to {self.params['x_max']}",
            f"Number of Points: {self.params['num_points']}",
            f"Baseline Type: {self.params['baseline_type']}",
            f"Number of Peaks: {self.params['num_peaks']}",
            f"Peak Types: {', '.join(self.params['peak_types'])}",
            f"Noise Level: {self.params['noise_level']}"
        ]

        for text in param_text:
            content.append(Paragraph(text, styles['Normal']))

        content.append(Spacer(1, 0.5 * inch))

        # Add each image with a caption
        content.append(Paragraph("Generated Spectra:", styles['Heading2']))
        content.append(Spacer(1, 0.2 * inch))

        for i, img_path in enumerate(image_filepaths):
            # Resize the image if necessary
            with PILImage.open(img_path) as img:
                width, height = img.size
                # Adjust width to fit page
                max_width = 7.5 * inch
                if width > max_width:
                    ratio = max_width / width
                    new_width = max_width
                    new_height = height * ratio
                else:
                    new_width = width
                    new_height = height

            # Add the image
            content.append(Image(img_path, width=new_width, height=new_height))

            # Add caption
            caption = f"Spectrum {i + 1}: {os.path.basename(img_path)}"
            content.append(Paragraph(caption, styles['Italic']))

            # Add spacing between images
            content.append(Spacer(1, 0.3 * inch))

        # Build the PDF
        doc.build(content)

        print(f"PDF report generated at: {pdf_path}")
        return pdf_path

    def _vary_parameters(self, index):
        """
        Vary parameters to create diverse spectra.

        Args:
            index (int): Current spectrum index for controlled variation
        """
        # Create variations that make sense for spectral data

        # Vary baseline
        if self.params["baseline_type"] == "polynomial":
            # Vary polynomial coefficients slightly
            coeffs = self.params["baseline_params"]["polynomial_coeffs"].copy()
            for i in range(len(coeffs)):
                coeffs[i] *= np.random.uniform(0.8, 1.2)
            self.params["baseline_params"]["polynomial_coeffs"] = coeffs
        elif self.params["baseline_type"] == "exponential":
            # Vary exponential parameters
            self.params["baseline_params"]["exp_amplitude"] *= np.random.uniform(0.8, 1.2)
            self.params["baseline_params"]["exp_decay"] *= np.random.uniform(0.9, 1.1)
        elif self.params["baseline_type"] == "sinusoidal":
            # Vary sinusoidal parameters
            self.params["baseline_params"]["sin_amplitude"] *= np.random.uniform(0.8, 1.2)
            self.params["baseline_params"]["sin_frequency"] *= np.random.uniform(0.9, 1.1)
            self.params["baseline_params"]["sin_phase"] += np.random.uniform(-0.2, 0.2)

        # Vary number of peaks (but not too much)
        orig_num_peaks = self.params["num_peaks"]
        variation = np.random.randint(-2, 3)  # -2, -1, 0, 1, or 2
        self.params["num_peaks"] = max(1, orig_num_peaks + variation)

        # Vary peak types
        peak_types = ["gaussian", "lorentzian", "voigt"]
        self.params["peak_types"] = np.random.choice(
            peak_types,
            size=min(3, np.random.randint(1, 4)),
            replace=True
        ).tolist()

        # Vary noise level (but keep it reasonable)
        self.params["noise_level"] *= np.random.uniform(0.8, 1.2)

        # Sometimes switch noise type
        if np.random.random() < 0.3:
            noise_types = ["gaussian", "poisson"]
            self.params["noise_type"] = np.random.choice(noise_types)

        # Occasionally add spikes
        if np.random.random() < 0.2:
            self.params["add_spikes"] = not self.params["add_spikes"]


# Main program to generate the dataset
if __name__ == "__main__":
    # Parameters as specified
    params = {
        "x_min": 0.0,
        "x_max": 10.0,
        "num_points": 1000,
        "baseline_type": "exponential",
        "baseline_params": {
            "exp_amplitude": 0.05,
            "exp_decay": 0.2
        },
        "num_peaks": 25,
        "peak_types": ["gaussian"],
        "min_peak_height": 0.02,
        "max_peak_height": 1.0,
        "min_peak_width": 0.005,
        "max_peak_width": 0.15,
        "noise_level": 0.05,
        "add_spikes": True,
        "spike_probability": 0.001,
        "file_prefix": "chromatogram"
    }

    # Create generator with the specified parameters
    generator = SpectralDataGenerator(params)

    # Generate a dataset with 10 spectra
    n_spectra = 10
    print(f"Generating {n_spectra} simulated spectra...")
    spectra = generator.generate_dataset(n_spectra=n_spectra, vary_params=True, save=True, plot=True)

    print(f"Dataset generation complete. {len(spectra)} spectra generated.")
    print("Output directories:")
    print(f"- Data files: {os.path.join(generator.params['output_dir'], 'data')}")
    print(f"- Peak information: {os.path.join(generator.params['output_dir'], 'peak_info')}")
    print(f"- Plot images: {os.path.join(generator.params['output_dir'], 'images')}")
    print(f"- PDF report: {os.path.join(generator.params['output_dir'], 'report.pdf')}")

    print("\nYou can now use these simulated spectra to test your peak detection algorithm.")