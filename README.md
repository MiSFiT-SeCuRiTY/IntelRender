# IntelRender

> **A powerful, offline, single-file report rendering and analysis utility for Kali Linux and other Python 3 environments.**

IntelRender converts raw report/data files into clean, human-readable output while preserving the underlying information. It is designed for security researchers, OSINT analysts, developers, incident responders, students, and anyone who regularly works with large or messy report files.

**Version:** `1.0.0`  
**License:** Choose a license for your repository (MIT is recommended if you want a permissive open-source license).

---

## ✨ Features

### 🔐 Login Protection
- Startup login screen.
- Default credentials:
  - **Username:** `1`
  - **Password:** `1`
- Failed-login handling.
- No online authentication or account required.

> **Security note:** The default credentials are intentionally simple for the initial release. If you distribute IntelRender publicly, change the credentials or implement a stronger authentication mechanism before using it for sensitive data.

### 📂 Multi-Format Input

IntelRender can automatically detect and process:

| Input | Support |
|---|---|
| JSON | ✅ |
| JSON Lines / NDJSON | ✅ |
| CSV | ✅ |
| TSV | ✅ |
| XML | ✅ |
| YAML | ✅* |
| INI / config files | ✅ |
| ENV files | ✅ |
| TXT | ✅ |
| Log-style text | ✅ |
| Unknown text files | ✅ |

\* YAML support uses PyYAML when it is installed.

### 🧠 Automatic Format Detection
IntelRender can determine a file's likely format using:
- File extension.
- File contents.
- JSON structure.
- Delimiter detection.
- XML/YAML characteristics.
- Text fallback for unknown formats.

You normally do **not** need to tell IntelRender what type of file you selected.

### 📊 Human-Readable Rendering
Deeply nested data is reorganized into an easier-to-read structure.

Example:

```json
{
  "target": {
    "name": "example.com",
    "ports": [
      80,
      443
    ]
  }
}
```

can be rendered into a readable report such as:

```text
Record 1
────────────────────────────────────────
Target
  Name: example.com
  Ports
    [1]: 80
    [2]: 443
```

### 🚀 Large-File Friendly Processing
IntelRender is designed to avoid unnecessary full-file loading.

It supports streaming-style processing for:
- JSON Lines / NDJSON.
- CSV/TSV.
- XML records.
- Plain text.
- Log files.
- Batch operations.

For very large files, IntelRender processes records progressively where the format allows it.

> A truly infinite file cannot be completely converted because storage and execution time are finite, but IntelRender does not impose an arbitrary "maximum number of lines" limit on normal streaming input.

### 🔎 Search
Search through reports without manually opening them.

Supported features include:
- Case-insensitive searching.
- Regular-expression searching.
- Line/record context.
- Large-file streaming search.

### 👁️ Preview
Preview a file before converting it.

Useful for quickly checking:
- Whether IntelRender detected the correct format.
- Whether the file is readable.
- What the first records/lines look like.

### 🔬 File Inspection
Inspect useful metadata before processing.

IntelRender can report:
- Full file path.
- File size.
- Detected format.
- Encoding.
- Modification time.
- SHA-256 hash.
- Line count for text-like files.
- Record count where practical.
- Top-level keys or columns when applicable.

### 📦 Batch Conversion
Convert an entire directory instead of selecting files one by one.

Options can include:
- Multiple files.
- Recursive directory scanning.
- Automatic format detection.
- Common output naming.
- Skipping unsupported/binary files.
- Continuing after an individual conversion error.

### 📝 Multiple Output Formats

IntelRender lets **you explicitly select the output format**.

Available output formats:

| Output | Extension | Best for |
|---|---|---|
| Text | `.txt` | Terminal/readable reports |
| Markdown | `.md` | GitHub/documentation |
| HTML | `.html` | Browser viewing |
| JSON | `.json` | Programmatic processing |
| CSV | `.csv` | Spreadsheet/data analysis |
| XML | `.xml` | Structured interchange |

### 🛡️ Offline by Design
IntelRender does not require:
- API keys.
- Cloud services.
- A remote server.
- Paid subscriptions.
- Online authentication.
- A database.

Your report files can remain completely local.

---

# 🖥️ Interface

IntelRender is designed as an interactive terminal application rather than a collection of complicated commands.

Typical workflow:

```text
┌──────────────────────────────────────┐
│              IntelRender             │
├──────────────────────────────────────┤
│  1. Convert a report                 │
│  2. Batch convert directory          │
│  3. Inspect / analyze file           │
│  4. Preview file                     │
│  5. Search within report             │
│  6. Settings                         │
│  7. Help                             │
│  8. Exit                             │
└──────────────────────────────────────┘
```

The application uses ANSI terminal colors and a custom IntelRender banner for a Kali-friendly interface.

---

# ⚙️ Requirements

## Minimum

- Python **3.9+**
- Linux/macOS/Windows terminal with ANSI color support.
- Read/write permissions for the files and directories being processed.

## Recommended

- Kali Linux
- Python 3.11+
- UTF-8 terminal
- A terminal window wide enough for the IntelRender banner.

No API key is required.

---

# 📥 Installation

## Option 1 — Clone the Repository

```bash
git clone https://github.com/MiSFiT-SeCuRiTY/IntelRender.git
cd IntelRender
```

Then run:

```bash
python3 intelrender.py
```

---

## Option 2 — Run the Script Directly

If you already have `intelrender.py`:

```bash
python3 intelrender.py
```

You can also make it executable:

```bash
chmod +x intelrender.py
```

Then:

```bash
./intelrender.py
```

---

# 🐍 Optional YAML Support

YAML processing requires **PyYAML**.

On Kali Linux:

```bash
sudo apt install python3-yaml
```

Or with pip:

```bash
python3 -m pip install PyYAML
```

IntelRender remains usable without PyYAML. Other supported formats do not depend on it.

---

# 🔐 First Launch

Start IntelRender:

```bash
python3 intelrender.py
```

The login screen will appear.

Default login:

```text
Username: 1
Password: 1
```

After successful authentication, IntelRender opens the main menu.

---

# 🚀 Basic Usage

## 1. Convert a Report

Select:

```text
1. Convert a report
```

IntelRender will ask for the input file.

Example:

```text
Enter report path:
 /home/user/reports/scan.json
```

IntelRender then:

1. Validates the path.
2. Detects the input format.
3. Detects a compatible encoding.
4. Reads the report.
5. Normalizes its structure.
6. Lets you choose an output format.
7. Creates the rendered report.

Example output:

```text
/home/user/reports/scan_rendered.html
```

---

# 📄 Supported Input Examples

## JSON

```json
{
  "target": "example.com",
  "status": "complete",
  "ports": [80, 443]
}
```

IntelRender can restructure the nested information into a readable report.

---

## JSON Lines / NDJSON

```text
{"host":"192.168.1.1","port":80}
{"host":"192.168.1.2","port":443}
{"host":"192.168.1.3","port":22}
```

Each line is treated as an individual record.

This format is particularly useful for very large datasets because records can be processed progressively.

---

## CSV

```csv
host,port,service
192.168.1.1,80,http
192.168.1.2,443,https
192.168.1.3,22,ssh
```

IntelRender detects the table structure and can produce human-readable or structured output.

---

## TSV

```text
host	port	service
192.168.1.1	80	http
192.168.1.2	443	https
```

Tab-separated data is handled separately from comma-separated data.

---

## XML

```xml
<report>
    <target>example.com</target>
    <status>complete</status>
</report>
```

IntelRender converts the XML tree into its normalized representation.

---

## YAML

```yaml
target: example.com
status: complete
ports:
  - 80
  - 443
```

Requires PyYAML.

---

## Plain Text / Logs

```text
[INFO] Starting scan
[INFO] Target: example.com
[INFO] Port 80 open
[INFO] Port 443 open
[INFO] Scan complete
```

Text and log files can be processed line-by-line.

---

# 📝 Output Formats

## TXT

Best for:
- Terminal reading.
- Sharing simple reports.
- Archiving human-readable results.

Example:

```text
IntelRender Report
==================

Input:
  scan.json

Format:
  JSON

Records:
  1

Record 1
--------
Target: example.com
Status: complete
```

---

## Markdown

Best for:
- GitHub.
- Documentation.
- Security reports.
- Notes.

Example:

```markdown
# IntelRender Report

## Record 1

- Target: `example.com`
- Status: `complete`
```

---

## HTML

Best for:
- Browser viewing.
- Presenting reports.
- Offline report sharing.

HTML output is generated locally and can be opened without an internet connection.

Example:

```bash
xdg-open report.html
```

---

## JSON

Best for:
- Automation.
- Further processing.
- Importing into another program.

The output preserves structured information instead of reducing everything to plain text.

---

## CSV

Best for:
- Excel.
- LibreOffice Calc.
- Data analysis.
- Flat tabular datasets.

Nested values are flattened where necessary to make them usable in a table.

---

## XML

Best for:
- Structured data interchange.
- Applications that require XML.
- Archival workflows.

---

# 🔎 Search

Choose:

```text
5. Search within report
```

Enter the path and search term.

Example:

```text
Search term: example.com
```

IntelRender scans the file and reports matching content.

For supported searches, regular expressions can also be used.

Example regex:

```text
192\.168\.\d+\.\d+
```

This can locate IPv4 addresses in text-based reports.

---

# 👁️ Preview

Choose:

```text
4. Preview file
```

Enter the report path.

IntelRender shows an initial portion of the file/records so you can inspect it before conversion.

Preview is especially useful for:
- Unknown extensions.
- Huge reports.
- Logs.
- Newly generated scan output.
- Checking format detection.

---

# 🔬 Inspect / Analyze

Choose:

```text
3. Inspect / analyze file
```

IntelRender gathers file information without requiring you to manually inspect the report.

Example:

```text
File:
  /home/user/reports/scan.json

Size:
  2.4 MB

Format:
  JSON

Encoding:
  UTF-8

SHA-256:
  ...

Modified:
  ...

Records:
  ...

Top-level keys:
  target
  status
  ports
```

This is useful when you receive an unfamiliar report and want to understand it before rendering it.

---

# 📦 Batch Conversion

Choose:

```text
2. Batch convert directory
```

Enter a directory:

```text
/home/user/reports/
```

IntelRender scans the directory and processes supported files.

Depending on the selected settings, recursive scanning can include subdirectories:

```text
reports/
├── scan1.json
├── scan2.csv
├── logs.txt
└── archived/
    ├── report.xml
    └── data.ndjson
```

Output files are generated alongside their corresponding input files unless you specify another destination through the application's available options.

---

# 📁 Output Naming

By default, IntelRender avoids replacing the original report.

Example:

```text
original.json
```

becomes:

```text
original_rendered.html
```

The original file remains untouched.

This prevents accidental destruction of source evidence/data.

---

# ⚠️ Overwriting Protection

IntelRender is designed to avoid accidentally overwriting your source report.

If the requested output already exists, the application can ask for confirmation before replacing it.

**Always keep the original source files when they contain evidence or important research data.**

---

# 🧮 Large File Handling

IntelRender is intended for both small reports and large datasets.

Streaming-friendly formats include:

- NDJSON.
- CSV.
- TSV.
- TXT.
- Logs.

For example, a multi-gigabyte NDJSON file can be processed record-by-record instead of requiring the entire file to be loaded into memory.

Conceptually:

```text
Large file
    │
    ▼
Read record
    │
    ▼
Normalize
    │
    ▼
Render/write
    │
    ▼
Read next record
    │
    └──────────────►
```

This makes the tool much more suitable for large report collections than a simple script based entirely around:

```python
data = json.load(file)
```

---

# 🧠 How IntelRender Processes Data

The processing pipeline is approximately:

```text
Input File
    │
    ▼
Path Validation
    │
    ▼
Format Detection
    │
    ▼
Encoding Detection
    │
    ▼
Parser
    │
    ▼
Normalized Records
    │
    ├── Human-readable renderer
    ├── Markdown renderer
    ├── HTML renderer
    ├── JSON renderer
    ├── CSV renderer
    └── XML renderer
    │
    ▼
Output File
```

This separation allows different input formats to be represented consistently.

---

# 🧩 Format Detection

IntelRender uses multiple indicators instead of blindly trusting a filename extension.

For example:

```text
report.dat
```

may actually contain JSON.

The tool can inspect its content and determine that it is structured JSON rather than automatically treating it as a generic text file.

When a format cannot be confidently identified, IntelRender falls back to text processing when possible.

---

# 🔤 Encoding Handling

IntelRender attempts common encodings such as:

1. UTF-8 with BOM.
2. UTF-8.
3. CP1252.
4. Latin-1 fallback.

This makes it more tolerant of reports generated by different applications and operating systems.

---

# 🛠️ Settings

Choose:

```text
6. Settings
```

Settings can be stored locally under:

```text
~/.intelrender/
```

The configuration file is:

```text
~/.intelrender/config.json
```

Possible preferences include:
- Default output format.
- Preview size.
- Recursive batch behavior.
- Timestamped output names.
- Color preferences.

No cloud configuration is required.

---

# 🆘 Help

Choose:

```text
7. Help
```

for built-in information about:
- Supported formats.
- Usage.
- Output types.
- Large-file processing.
- Common problems.

---

# ❌ Error Handling

IntelRender attempts to fail gracefully rather than crashing on the first malformed file.

Examples include:

### File does not exist

```text
Error: File not found.
```

### Permission problem

```text
Error: Permission denied.
```

### Invalid JSON

```text
Error: Unable to parse JSON.
```

### Unsupported YAML dependency

```text
YAML support requires PyYAML.
```

### Invalid output location

The application reports the problem and allows you to retry.

During batch processing, an error in one file should not unnecessarily prevent the remaining files from being processed.

---

# 🔐 Privacy

IntelRender is designed as a local/offline utility.

It does not need to send your reports to:
- IntelRender servers.
- Third-party APIs.
- Cloud storage.
- Analytics services.

Your files remain on your machine unless **you** choose to copy or upload the generated reports elsewhere.

This makes IntelRender suitable for workflows involving sensitive local reports, provided your own machine and output handling are properly secured.

---

# 🛡️ Security / Ethical Use

IntelRender is a **report processing and rendering tool**.

It does not need to perform:
- Exploitation.
- Password attacks.
- Network attacks.
- Malware deployment.
- Unauthorized access.

It is suitable for processing reports produced by legitimate security assessments, OSINT workflows, system administration, research, development, and other authorized activities.

Always make sure you have permission to process and distribute the data you are working with.

---

# 📚 Example Workflow

A typical security-research workflow might look like:

```text
Collect report
     │
     ▼
report.json
     │
     ▼
IntelRender
     │
     ├── Inspect
     │
     ├── Preview
     │
     ├── Search
     │
     └── Convert
             │
             ├── report_rendered.txt
             ├── report_rendered.md
             ├── report_rendered.html
             └── report_rendered.csv
```

You can keep the original report untouched while generating multiple representations for different purposes.

---

# 📂 Recommended Project Structure

Because IntelRender is designed as a single-file application, the minimum repository can be extremely simple:

```text
IntelRender/
├── intelrender.py
├── README.md
└── LICENSE
```

Optional:

```text
IntelRender/
├── intelrender.py
├── README.md
├── LICENSE
├── CHANGELOG.md
└── .gitignore
```

---

# 🚀 Running From Any Directory

You can place the executable script somewhere in your PATH.

For example:

```bash
mkdir -p ~/.local/bin
cp intelrender.py ~/.local/bin/intelrender
chmod +x ~/.local/bin/intelrender
```

Then add `~/.local/bin` to your PATH if necessary.

After that:

```bash
intelrender
```

can launch IntelRender from other directories.

---

# 🧪 Testing

Before using IntelRender with important reports, test it against representative files.

Example:

```bash
mkdir -p test_reports
```

Create a JSON file:

```bash
printf '{"target":"example.com","ports":[80,443]}\n' > test_reports/test.json
```

Run IntelRender:

```bash
python3 intelrender.py
```

Then:
1. Log in.
2. Select **Convert a report**.
3. Select `test_reports/test.json`.
4. Choose an output format.
5. Open the generated report.

---

# 🐛 Troubleshooting

## `python3: command not found`

Install Python:

```bash
sudo apt update
sudo apt install python3
```

---

## Permission denied

Make the script executable:

```bash
chmod +x intelrender.py
```

Then:

```bash
./intelrender.py
```

---

## YAML files are not detected/parsed

Install PyYAML:

```bash
sudo apt install python3-yaml
```

or:

```bash
python3 -m pip install PyYAML
```

---

## Colors look incorrect

Make sure your terminal supports ANSI escape sequences.

Modern Kali terminals normally support them.

If your terminal has unusual color behavior, run IntelRender in a standard terminal emulator and check the application's color setting.

---

## Unicode banner looks broken

Use a UTF-8 terminal.

Check:

```bash
locale
```

A UTF-8 locale should normally contain values such as:

```text
LANG=en_US.UTF-8
```

Your exact locale may differ.

---

# ⚡ Performance Notes

IntelRender is optimized around practical report processing rather than artificial benchmark numbers.

Performance depends on:

- File size.
- Number of records.
- Nesting depth.
- Output format.
- Storage speed.
- CPU.
- Available memory.
- Complexity of the source structure.

Streaming formats such as NDJSON, CSV, TSV, and plain text are especially suitable for very large files.

Structured formats such as a single enormous JSON object or deeply nested document may inherently require more memory because the parser must understand the complete structure.

---

# 🧱 Design Goals

IntelRender is built around several principles:

### 1. Simple

A beginner should be able to launch it and work through menus.

### 2. Offline

No server should be required for normal operation.

### 3. Portable

The core application should remain a single Python script.

### 4. Format-Agnostic

Reports should not need to be manually converted before processing.

### 5. Large-File Friendly

Avoid unnecessary memory usage whenever the source format permits streaming.

### 6. Safe

Source reports should not be overwritten accidentally.

### 7. Useful

Inspection, preview, search, batch conversion, and multiple output formats make IntelRender useful beyond one-time conversion.

---

# 🔮 Future Development Ideas

Possible future releases may add:

- More structured log parsers.
- Additional report formats.
- Advanced filtering.
- Column selection.
- Custom templates.
- More HTML themes.
- PDF report generation.
- Statistics and visual summaries.
- Plugin-style format handlers.
- More granular export controls.
- Improved streaming JSON support.
- Configuration profiles.
- Report comparison/diff mode.
- Duplicate report detection.
- Automatic report categorization.

These are potential roadmap items and are not necessarily included in v1.0.0.

---

# 🤝 Contributing

Contributions are welcome.

A typical contribution workflow:

```bash
git clone https://github.com/YOUR_USERNAME/IntelRender.git
cd IntelRender
```

Create a branch:

```bash
git checkout -b feature/my-feature
```

Make your changes and test them.

Then:

```bash
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
```

Open a Pull Request on GitHub.

When contributing, please try to:
- Keep IntelRender dependency-light.
- Preserve the menu-driven workflow.
- Avoid unnecessary network requirements.
- Keep large-file processing in mind.
- Handle malformed input gracefully.
- Document new features.
- Test existing functionality before submitting changes.

---

# 📜 License

This project does not specify a license automatically.

If you want others to freely use, modify, and redistribute IntelRender, the **MIT License** is a common choice.

Add a `LICENSE` file to the repository and update this section to match the license you choose.

---

# ⭐ Credits

**IntelRender**  
A single-file report rendering and analysis utility.

Built with:

- Python 3
- Python Standard Library
- Optional PyYAML for YAML support

No API.  
No server.  
No paid service.  
No database required.

---

# 📌 Quick Reference

| Task | Menu |
|---|---|
| Convert one report | `1` |
| Convert a directory | `2` |
| Inspect a file | `3` |
| Preview a file | `4` |
| Search a report | `5` |
| Change settings | `6` |
| Open help | `7` |
| Exit | `8` |

Default login:

```text
Username: 1
Password: 1
```

Launch:

```bash
python3 intelrender.py
```

Executable mode:

```bash
chmod +x intelrender.py
./intelrender.py
```

---

# 🧠 IntelRender in One Sentence

**IntelRender turns messy local reports and structured data into readable, searchable, portable reports without requiring an API, server, subscription, or complicated command-line workflow.**

---

<p align="center">
  <b>IntelRender v1.0.0</b><br>
  Local • Offline • Menu-Driven • Multi-Format
</p>
