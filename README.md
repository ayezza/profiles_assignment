# MCAP Profiles 📊

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

An innovative Python package for optimal profile-to-activity assignment based on skills matching. This solution leverages advanced algorithms to maximize the correspondence between required activity competencies and available profile skills.

## ✨ Features

- Skills matrix analysis
- Automatic profile assignment
- Multiple evaluation scale support
- Detailed reporting generation
- Intuitive command-line interface
- Data-driven decision making
- Customizable matching algorithms

## 🚀 Installation

```bash
pip install mcap-profiles
```

## 📖 Usage

### Basic Usage

```bash
mcap
```

### Advanced Usage

```bash
mcap --mca path/to/mca.csv --mcp path/to/mcp.csv --scale free
```

### Available Options

```bash
mcap --help
```

## 📋 Input File Formats

### MCA (Competency-Activity Matrix)

Required CSV format:

```csv
Activity,Comp1,Comp2,Comp3
Act1,2,4,3
Act2,3,2,5
```

### MCP (Competency-Profile Matrix)

Required CSV format:

```csv
Profile,Comp1,Comp2,Comp3
Prof1,2,5,3
Prof2,3,1,4
```

## 📁 Project Structure

```
mcap-profiles/
├── LICENSE
├── MANIFEST.in
├── README.md
├── setup.py
├── .gitignore
├── main.py
├── config/
│   └── mylogger.ini
├── data/
│   ├── input/
│   │   ├── mca_01.csv
│   │   └── mcp_01.csv
│   └── output/
└── src/
    ├── __init__.py
    ├── core/
    ├── models/
    └── utils/
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🔍 Documentation

For detailed documentation and examples, visit our [documentation page](https://github.com/yourusername/mcap-profiles/wiki).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📫 Contact & Support

- Create an issue for bug reports or feature requests
- For major changes, please open an issue first to discuss what you would like to change
- Join our [community discussions](https://github.com/yourusername/mcap-profiles/discussions)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape MCAP Profiles
- Special thanks to the open-source community for their invaluable tools and libraries


