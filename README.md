<div align="center">

# Timewarrior Tag Comparator 🕒

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Timewarrior](https://img.shields.io/badge/timewarrior-compatible-orange.svg?style=for-the-badge)](https://timewarrior.net/)

A command-line tool to compare time tracked between different Timewarrior tags and analyze your time usage
</div>

## 🚀 Features

- Compare tracked time between any two tags with signed differences
- View total tracked time across all tags for the current day
- Smart handling of ongoing tracking sessions
- Helpful suggestions when tags have no tracked time
- Robust error handling and user-friendly messages
- Clean and informative output format

## 📋 Prerequisites

- Python 3.6 or higher
- [Timewarrior](https://timewarrior.net/) installed and configured
  ```bash
  # Ubuntu/Debian
  sudo apt install timewarrior
  
  # Fedora
  sudo dnf install timew
  
  # macOS
  brew install timewarrior
  ```

## 💻 Installation

1. Clone this repository:
```bash
git clone https://github.com/tom-doerr/timewarrior-tag-comparator.git
cd timewarrior-tag-comparator
```

2. Make the script executable:
```bash
chmod +x tag_time_diff.py
```

3. Optionally, add to your PATH for system-wide access:
```bash
sudo ln -s "$(pwd)/tag_time_diff.py" /usr/local/bin/timew-compare
```

## 🎯 Usage

### Start Tracking Time

First, start tracking time with Timewarrior:
```bash
timew start coding              # Start tracking 'coding'
timew start meeting coding      # Track multiple tags
timew stop                      # Stop tracking
```

### Compare Two Tags

Compare time between any two tags:
```bash
./tag_time_diff.py coding meeting
```

Example output:
```
Time for coding: 02:15:30
Time for meeting: 01:30:00
Difference (coding compared to meeting): 00:45:30
```

### View Total Time

See total tracked time for all tags today:
```bash
./tag_time_diff.py -t
```

Example output:
```
Total tracked time for all tags: 03:45:30
```

### Help

View all available options:
```bash
./tag_time_diff.py --help
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add some feature'`
4. Push to your fork: `git push origin feature-name`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Timewarrior](https://timewarrior.net/) for the excellent time tracking tool
- The Python community for the amazing standard library
- All contributors who help improve this tool

<div align="center">

Made with ❤️ by [Tom Dörr](https://github.com/tom-doerr)

</div>

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

Made with ❤️ by [Tom Dörr](https://github.com/tom-doerr)

</div>
