# ⚡ DataCleaner Studio

An offline, high-performance desktop utility built with **PySide6** and **Pandas** to automate raw data wrangling, missing value handling, and format conversions in seconds.

🔗 **Live Website & Download:** [siserhoudji.netlify.app](https://siserhoudji.netlify.app)

---

## Key Features

* **⚡ Smart Header Normalization:** Converts column titles into standard `snake_case`.
* **📁 Multi-Format Ingestion:** Direct reading and exporting for `.csv`, `.xlsx`, `.parquet`, and `.tsv`.
* **📊 Real-Time Telemetry:** Live tracking of row counts, column counts, missing values, and duplicate rows.
* **🔒 100% Offline & Local:** Processes data directly on CPU memory without external server transfers.

---

## Tech Stack

* **GUI Framework:** PySide6 (Qt for Python)
* **Data Processing:** Pandas, NumPy, OpenPyXL
* **Executable Packaging:** PyInstaller
* **Web Landing Page:** HTML5, Custom CSS3, Modern JavaScript

---

## Local Development Setup

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/datacleaner-studio.git](https://github.com/YOUR_USERNAME/datacleaner-studio.git)

# Navigate into directory
cd datacleaner-studio

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
