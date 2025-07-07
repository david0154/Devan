<p align="center">
  <img src="logo.png" alt="Devan Logo" width="150"/>
</p>

<h1 align="center">🕉️ Devan Programming Language (.Om)</h1>

<p align="center">
  <b>A Sanskrit-based language powered by Python & PHP</b><br/>
  <a href="https://github.com/david0154/Devan"><p align="center">
  <a href="#"><img src="https://img.shields.io/badge/status-active-brightgreen.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/language-Python%20%7C%20PHP-yellow.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/filetype-.Om-lightgrey.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/style-Sanskrit-orange.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20Mac-informational.svg"></a>
  </p>

---

## 🔹Overview

Devan is a Sanskrit-inspired programming language that allows you to write logical code in the sacred style of Sanskrit. It supports both interpreting and compiling into modern languages like Python and PHP. Code files use the .Om extension and are translated using a custom Sanskrit-to-code mapping system.


---

📦 Key Features

🧠 Interpreter for .Om files – Run directly via Python

🛠 Compiler – Convert .Om to .py or .php seamlessly

📜 Sanskrit-to-Code Mapping – Powered by a customizable JSON-based structure

🔄 Auto AI Translation – Translate English input to Sanskrit using offline Indic NLP models

🔐 Local File Encryption – Auto-encrypt original and translated files for privacy

📦 One-Line Installer – Automatically install required Python packages

💻 CLI Tool – Simple commands like devan run and devan compile

🧰 PHP Runtime Support – Execute .Om code in PHP using built-in executor

🧱 Cross-Platform – Works on Windows, macOS, Linux, and Ubuntu



---

## 🧪 Example

**File: `test.Om`**

```sanskrit
आयातः "गणकसंग्रहः"
मान = गणकसंग्रहः.sqrt(१६)
लेखय "उत्तर:", मान

पीएचपी_कोड = "echo sqrt(16);"
चालय "php", पीएचपी_कोड
```

**Output (Python):**

```python
import math
value = math.sqrt(16)
print("उत्तर:", value)
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/david0154/Devan.git
cd Devan
pip install -r requirements.txt
python devan_runner.py run test_files/test.Om
```

---

## 🛠️ CLI Commands

```bash
devan run hello.Om
devan compile hello.Om --lang python
devan compile hello.Om --lang php
```

---

## 📁 Directory Structure

```
Devan/
├── devan_parser.py
├── devan_compiler.py
├── devan_runner.py
├── devan_installer.py
├── devan_php_runner.py
├── devan_stdlib.json
├── requirements.txt
├── logo.png
├── LICENSE
└── test_files/
```

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE).

---

## ✨ Credits

- **Author**: David  
- **Company**: Nexuzy Tech Pvt Ltd  
- **Email**: nexuzypvtltd@gmail.com

---
