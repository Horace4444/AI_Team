import subprocess
import sys

# List of required packages
required_packages = [
    "colorama",
    "pygments",
    "tavily-python",
    "pillow",
    "anthropic",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "plotly",
    "scipy",
    "statsmodels",
    "yfinance",
    "quantlib", 
    "dash"
]

# Function to install a package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install each package
for package in required_packages:
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} is not installed. Installing now...")
        try:
            install_package(package)
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            print("Attempting to resolve dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--use-feature=2020-resolver"])
        except Exception as e:
            print(f"An unexpected error occurred while installing {package}: {e}")

print("All required packages are installed.")
