# MCAP Profiles - Profile-Activity Matching System 📊

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python package designed for optimal profile-to-activity assignment based on skills matching, developed by Abdel YEZZA (Ph.D). This solution employs advanced algorithms to maximize the correspondence between required activity competencies and available profile skills.

It is designed to provide a comprehensive solution for profile-activity matching, offering multiple models, flexible scaling options, streamlit web interface, a robust logging system, a detailed validation of input data, and a customizable processing of MCAP functions (sum, mean, euclidean and any custom function).

![MCAP Profiles Screenshot](https://github.com/ayezza/profiles_assignment/raw/main/README_assets/screenshot.png)

## 🎯 Key Features

- **Skills Matrix Analysis**: Process and analyze competency-activity (MCA) and competency-profile (MCP) matrices
- **Multiple Model Support**: Five different matching models available (model1 through model5 or any custom function)
- **Flexible Scaling**: Support for different scale types (0-1, free)
- **Web Interface**: Built-in web application using FastAPI and Streamlit
- **Detailed Logging**: Comprehensive logging system for tracking operations
- **Data Validation**: Robust input validation and error handling
- **Customizable Processing**: Support for different MCAP functions (sum, mean, euclidean and any custom function)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd profiles_assignment
```

2. Create and activate a virtual environment (recommended):
```bash
# install venv on Linux/MacOS:
python -m venv venv
source venv/bin/activate  
# to activate on Windows: 
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📦 Dependencies

- streamlit >= 1.24.0
- pandas >= 1.5.0
- scikit-learn
- matplotlib
- fastapi >= 0.104.0
- uvicorn >= 0.24.0
- python-dotenv >= 1.0.0
- python-multipart >= 0.0.6
- sqlalchemy >= 2.0.23

## 🚀 Usage

### Command Line Interface

Basic usage:
```bash
python main.py
```

Advanced usage with custom parameters:
```bash
python main.py --mca path/to/mca.csv --mcp path/to/mcp.csv --model model2 --scale 0-1 --mcap sum
```

### Command Line Arguments

- `--mca`: Path to the MCA (Matrix Competency-Activity) file
- `--mcp`: Path to the MCP (Matrix Competency-Profile) file
- `--model`: Model selection (model1, model2, model3, model4, model5)
- `--scale`: Scale type (0-1 or free)
- `--mcap`: MCAP function type (sum, mean, sqrt custom)

## 📋 Input File Formats

### MCA (Competency-Activity Matrix)
```csv
Activity,Comp1,Comp2,Comp3
Activity1,0.8,0.6,0.7
Activity2,0.5,0.9,0.4
```

### MCP (Competency-Profile Matrix)
```csv
Profile,Comp1,Comp2,Comp3
Profile1,0.7,0.8,0.6
Profile2,0.9,0.5,0.8
```

## 📁 Project Structure

- `src/`: Core source code
  - `core/`: Core processing logic
  - `models/`: Matching model implementations
  - `utils/`: Utility functions and helpers
- `config/`: Configuration files
- `data/`: Input and output data
  - `input/`: Input CSV files
  - `output/`: Generated outputs
- `tests/`: Unit and integration tests
- `web/`: Web interface components

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 More Information

For more detailed examples and explanations, check out the author's article:
[LinkedIn Article](https://www.linkedin.com/feed/update/urn:li:activity:6853567958246027265/)

## ✍️ Author

**Abdel YEZZA (Ph.D)**

*Note: This code is completely free and can be modified with only one condition: DO NOT REMOVE author's name*
