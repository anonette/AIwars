# Encoding Requirements and Setup Instructions

## Overview

The AI Debate System uses Unicode characters (emojis) for visual formatting. This document provides guidance on ensuring proper encoding support across different environments.

## Encoding Requirements

### Minimum Requirements
- **Character Encoding**: UTF-8
- **Python Version**: 3.8+ (with full Unicode support)
- **Terminal**: Must support UTF-8 encoding
- **File System**: Must support UTF-8 filenames and content

### Recommended Setup
- **Python**: 3.9+ for better Unicode handling
- **Terminal**: Windows Terminal, iTerm2, or modern Linux terminals
- **Font**: A font with comprehensive emoji support (e.g., Noto Color Emoji, Segoe UI Emoji)

## Platform-Specific Setup

### Windows

#### 1. Enable UTF-8 in Command Prompt/PowerShell
```powershell
# Set console to UTF-8
chcp 65001
```

#### 2. Set Environment Variable (Permanent)
```powershell
# Add to system environment variables
[System.Environment]::SetEnvironmentVariable('PYTHONIOENCODING', 'utf-8', 'User')
```

#### 3. Use Windows Terminal (Recommended)
- Download from Microsoft Store
- Supports UTF-8 by default
- Better emoji rendering

### macOS

macOS terminals generally support UTF-8 by default. If you encounter issues:

```bash
# Add to ~/.bash_profile or ~/.zshrc
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8
```

### Linux

Most modern Linux distributions support UTF-8. To ensure proper configuration:

```bash
# Check current locale
locale

# If not UTF-8, set it
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf-8

# Make permanent by adding to ~/.bashrc
echo 'export LANG=en_US.UTF-8' >> ~/.bashrc
echo 'export LC_ALL=en_US.UTF-8' >> ~/.bashrc
echo 'export PYTHONIOENCODING=utf-8' >> ~/.bashrc
```

## Python Environment Setup

### 1. Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Encoding Support
```python
# Test script to verify encoding
python -c "print('Emoji test: 🇺🇸 💎 🔍 ✓')"
```

## Configuration Options

### Disable Emojis (Fallback Mode)

If your environment doesn't support emojis, configure the system to use ASCII-only mode:

#### Option 1: Environment Variable
```bash
export DEBATE_NO_EMOJIS=1
```

#### Option 2: Config File
Edit `config.yaml`:
```yaml
formatting:
  display:
    enable_emojis: false  # Disable emojis globally
```

#### Option 3: Runtime Parameter
```python
# When initializing the formatter
formatter_config = {
    'enable_emojis': False,
    'log_safe_mode': True
}
```

## Logging Configuration

The system automatically uses log-safe (ASCII) formatting for log files:

```yaml
formatting:
  logging:
    emoji_mode: "replace"  # Options: "strip", "replace", "keep"
    log_safe_mode: true    # Always use ASCII for logs
```

## Troubleshooting

### Issue: UnicodeEncodeError
**Solution**: Set PYTHONIOENCODING environment variable
```bash
export PYTHONIOENCODING=utf-8
```

### Issue: Emojis Display as Boxes
**Solution**: Install a font with emoji support
- Windows: Segoe UI Emoji (included)
- macOS: Apple Color Emoji (included)
- Linux: `sudo apt install fonts-noto-color-emoji`

### Issue: Terminal Shows Garbled Characters
**Solution**: Ensure terminal is set to UTF-8
```bash
# Check terminal encoding
echo $LANG
# Should show something like: en_US.UTF-8
```

### Issue: Log Files Have Encoding Errors
**Solution**: The system should automatically use ASCII-safe logging. If not:
1. Check `config.yaml` formatting.logging.log_safe_mode is `true`
2. Ensure log file handlers specify UTF-8 encoding

## Testing Your Setup

Run the formatter test suite to verify everything works:

```bash
# Run all tests
python test_formatter.py

# Test emoji handling specifically
python -m unittest test_formatter.TestEmojiHandling -v

# Test the formatter with sample output
python debate_formatter.py
```

## IDE/Editor Configuration

### VS Code
Add to settings.json:
```json
{
    "files.encoding": "utf8",
    "terminal.integrated.unicode.version": "11"
}
```

### PyCharm
- Settings → Editor → File Encodings
- Set "Global Encoding" and "Project Encoding" to UTF-8

### Sublime Text
- Preferences → Settings
- Add: `"default_encoding": "UTF-8"`

## Docker Support

If using Docker, ensure UTF-8 locale:

```dockerfile
# In Dockerfile
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8
```

## CI/CD Considerations

For GitHub Actions or other CI systems:

```yaml
# .github/workflows/test.yml
env:
  PYTHONIOENCODING: utf-8
  LANG: en_US.UTF-8
```

## Performance Notes

- Emoji processing has minimal performance impact
- Log-safe mode (ASCII) is slightly faster
- Structured logging (JSON) is best for analysis
- Use `strip_emojis()` for data processing pipelines

## Further Reading

- [Python Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
- [UTF-8 Everywhere Manifesto](https://utf8everywhere.org/)
- [Emoji Unicode Standards](https://unicode.org/emoji/techindex.html)