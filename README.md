<div align="center">

# Timewarrior Tag Comparator 🕒

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Timewarrior](https://img.shields.io/badge/timewarrior-compatible-orange.svg?style=for-the-badge)](https://timewarrior.net/)

A command-line tool to compare time tracked between different Timewarrior tags
</div>

## 🚀 Features

- Compare tracked time between any two tags
- View total tracked time across all tags
- Clean and informative output format
- Handles cases with no tracked time
- Easy-to-use command-line interface

## 📋 Prerequisites

- Python 3.6 or higher
- Timewarrior installed and configured
- Basic command-line knowledge

## 💻 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/timewarrior-tag-comparator.git
cd timewarrior-tag-comparator
```

2. Make the script executable:
```bash
chmod +x tag_time_diff.py
```

## 🎯 Usage

### Compare Two Tags

```bash
./tag_time_diff.py tag1 tag2
```

### View Total Time

```bash
./tag_time_diff.py -t
```

### Help

```bash
./tag_time_diff.py --help
```

## 📝 Example Output

```
Time for work: 05:30:00
Time for study: 03:15:00
Absolute difference between work and study: 02:15:00
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Timewarrior](https://timewarrior.net/) for the excellent time tracking tool
- The Python community for the amazing standard library

<div align="center">

Made with ❤️ by [Your Name]

</div>
