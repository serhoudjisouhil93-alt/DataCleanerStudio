import sys
import os
import pandas as pd
import numpy as np

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableView, QFileDialog, QMessageBox,
    QComboBox, QFrame, QSplitter, QHeaderView, QGroupBox, QSpinBox, QCheckBox
)

# ==========================================
# CLEAN DARK THEME STYLESHEET
# ==========================================
DARK_STYLE = """
QMainWindow {
    background-color: #121214;
}
QWidget {
    font-family: "Segoe UI", -apple-system, sans-serif;
    font-size: 12px;
    color: #e2e8f0;
}

/* Header & Panels */
QFrame#TopBar {
    background-color: #1a1a1e;
    border-bottom: 1px solid #2d2d35;
}
QGroupBox {
    font-weight: bold;
    color: #38bdf8;
    border: 1px solid #27272a;
    border-radius: 6px;
    margin-top: 6px;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}

/* Inputs & Buttons */
QPushButton {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 4px;
    padding: 6px 12px;
    color: #f4f4f5;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #3f3f46;
}
QPushButton#PrimaryBtn {
    background-color: #0284c7;
    border: 1px solid #0369a1;
}
QPushButton#PrimaryBtn:hover {
    background-color: #0369a1;
}
QComboBox, QLineEdit, QSpinBox {
    background-color: #09090b;
    border: 1px solid #3f3f46;
    border-radius: 4px;
    padding: 4px 8px;
    color: #f4f4f5;
}

/* Data Table */
QTableView {
    background-color: #18181b;
    border: 1px solid #27272a;
    gridline-color: #27272a;
    color: #f4f4f5;
    selection-background-color: #0284c7;
    selection-color: #ffffff;
}
QHeaderView::section {
    background-color: #27272a;
    color: #38bdf8;
    font-weight: 600;
    padding: 6px;
    border: 1px solid #18181b;
}

/* Status Bar */
QLabel#StatLabel {
    color: #94a3b8;
    font-size: 11px;
}
"""

# ==========================================
# FAST TABLE MODEL FOR PREVIEWING
# ==========================================
class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame()):
        super().__init__()
        self._df = df

    def rowCount(self, parent=QModelIndex()):
        return len(self._df)

    def columnCount(self, parent=QModelIndex()):
        return len(self._df.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            val = self._df.iloc[index.row(), index.column()]
            return "" if pd.isna(val) else str(val)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._df.columns[section])
            if orientation == Qt.Vertical:
                return str(section + 1)
        return None

    def update_data(self, new_df):
        self.beginResetModel()
        self._df = new_df.copy()
        self.endResetModel()

# ==========================================
# MAIN APP
# ==========================================
class SimpleDataCleaner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataCleaner Studio")
        self.resize(1200, 750)
        self.setStyleSheet(DARK_STYLE)

        self.df_original = pd.DataFrame()
        self.df_clean = pd.DataFrame()
        self.table_model = PandasModel()

        self._build_ui()

    def _build_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # 1. TOP FILE BAR
        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        top_lay = QHBoxLayout(top_bar)
        top_lay.setContentsMargins(12, 10, 12, 10)
        top_lay.setSpacing(12)

        btn_open = QPushButton("📁 Load Dataset")
        btn_open.clicked.connect(self.load_dataset)
        top_lay.addWidget(btn_open)

        self.lbl_file = QLabel("No file loaded")
        self.lbl_file.setStyleSheet("color: #a1a1aa; font-style: italic;")
        top_lay.addWidget(self.lbl_file)

        top_lay.addStretch()

        btn_reset = QPushButton("↺ Revert to Original")
        btn_reset.clicked.connect(self.reset_dataset)
        top_lay.addWidget(btn_reset)

        btn_export = QPushButton("💾 Export Clean File")
        btn_export.setObjectName("PrimaryBtn")
        btn_export.clicked.connect(self.export_dataset)
        top_lay.addWidget(btn_export)

        root.addWidget(top_bar)

        # 2. MAIN BODY (LEFT CONTROLS / RIGHT PREVIEW)
        body = QWidget()
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(12, 12, 12, 12)
        body_lay.setSpacing(12)

        # LEFT SIDE PANEL: CLEANING TOOLS
        tools_panel = QWidget()
        tools_panel.setFixedWidth(320)
        tools_lay = QVBoxLayout(tools_panel)
        tools_lay.setContentsMargins(0, 0, 0, 0)
        tools_lay.setSpacing(10)

        # --- Quick Auto Clean ---
        group_auto = QGroupBox("One-Click Magic Clean")
        auto_lay = QVBoxLayout(group_auto)
        btn_auto = QPushButton("⚡ Auto-Clean All (Recommended)")
        btn_auto.setObjectName("PrimaryBtn")
        btn_auto.clicked.connect(self.auto_clean_all)
        auto_lay.addWidget(btn_auto)
        tools_lay.addWidget(group_auto)

        # --- Text & Header Fixes ---
        group_text = QGroupBox("Headers & Text Formatting")
        text_lay = QVBoxLayout(group_text)

        btn_fix_headers = QPushButton("Clean Column Names (lowercase/snake_case)")
        btn_fix_headers.clicked.connect(self.clean_headers)
        text_lay.addWidget(btn_fix_headers)

        btn_trim_str = QPushButton("Trim Leading/Trailing Whitespace")
        btn_trim_str.clicked.connect(self.trim_spaces)
        text_lay.addWidget(btn_trim_str)

        tools_lay.addWidget(group_text)

        # --- Missing Values & Duplicates ---
        group_rows = QGroupBox("Duplicates & Missing Values")
        rows_lay = QVBoxLayout(group_rows)

        btn_drop_dups = QPushButton("Remove Duplicate Rows")
        btn_drop_dups.clicked.connect(self.drop_duplicates)
        rows_lay.addWidget(btn_drop_dups)

        fill_box = QHBoxLayout()
        self.cmb_null_strategy = QComboBox()
        self.cmb_null_strategy.addItems(["Drop Null Rows", "Fill 0 / N/A", "Fill Mean (Numeric)"])
        fill_box.addWidget(self.cmb_null_strategy)

        btn_nulls = QPushButton("Apply")
        btn_nulls.clicked.connect(self.handle_nulls)
        fill_box.addWidget(btn_nulls)
        rows_lay.addLayout(fill_box)

        tools_lay.addWidget(group_rows)

        # --- Column Management ---
        group_cols = QGroupBox("Column Tools")
        cols_lay = QVBoxLayout(group_cols)

        cols_lay.addWidget(QLabel("Select Column:"))
        self.cmb_columns = QComboBox()
        cols_lay.addWidget(self.cmb_columns)

        btn_drop_col = QPushButton("Drop Selected Column")
        btn_drop_col.clicked.connect(self.drop_column)
        cols_lay.addWidget(btn_drop_col)

        btn_auto_types = QPushButton("Auto-Convert Data Types")
        btn_auto_types.clicked.connect(self.convert_types)
        cols_lay.addWidget(btn_auto_types)

        tools_lay.addWidget(group_cols)
        tools_lay.addStretch()

        body_lay.addWidget(tools_panel)

        # RIGHT SIDE: TABLE PREVIEW & STATS
        preview_panel = QWidget()
        prev_lay = QVBoxLayout(preview_panel)
        prev_lay.setContentsMargins(0, 0, 0, 0)
        prev_lay.setSpacing(6)

        # Stats Bar
        self.lbl_stats = QLabel("Rows: 0 | Columns: 0 | Missing Values: 0 | Duplicates: 0")
        self.lbl_stats.setObjectName("StatLabel")
        prev_lay.addWidget(self.lbl_stats)

        # Table View
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        prev_lay.addWidget(self.table_view)

        body_lay.addWidget(preview_panel)
        root.addWidget(body)

    # ==========================================
    # DATA LOADING & EXPORT
    # ==========================================
    def load_dataset(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Dataset", "", "Data Files (*.csv *.xlsx *.xls *.parquet *.tsv *.txt)"
        )
        if not path:
            return

        try:
            ext = os.path.splitext(path)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(path)
            elif ext in (".xlsx", ".xls"):
                df = pd.read_excel(path)
            elif ext == ".parquet":
                df = pd.read_parquet(path)
            elif ext in (".tsv", ".txt"):
                df = pd.read_csv(path, sep="\t")
            else:
                return

            self.df_original = df.copy()
            self.df_clean = df.copy()
            self.lbl_file.setText(os.path.basename(path))
            self.refresh_ui()

        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load file:\n{str(e)}")

    def export_dataset(self):
        if self.df_clean.empty:
            QMessageBox.warning(self, "Export Warning", "No data to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Export Cleaned File", "clean_dataset.csv", "CSV (*.csv);;Excel (*.xlsx);;Parquet (*.parquet)"
        )
        if not path:
            return

        try:
            if path.endswith(".xlsx"):
                self.df_clean.to_excel(path, index=False)
            elif path.endswith(".parquet"):
                self.df_clean.to_parquet(path, index=False)
            else:
                self.df_clean.to_csv(path, index=False)

            QMessageBox.information(self, "Export Success", f"File saved successfully to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export file:\n{str(e)}")

    def reset_dataset(self):
        if not self.df_original.empty:
            self.df_clean = self.df_original.copy()
            self.refresh_ui()

    # ==========================================
    # CLEANING ACTIONS
    # ==========================================
    def auto_clean_all(self):
        if self.df_clean.empty:
            return
        # 1. Clean header names
        self.df_clean.columns = (
            self.df_clean.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"[^\w\s]", "", regex=True)
            .str.replace(r"\s+", "_", regex=True)
        )
        # 2. Trim string columns
        str_cols = self.df_clean.select_dtypes(include=["object"]).columns
        for col in str_cols:
            self.df_clean[col] = self.df_clean[col].astype(str).str.strip()
            self.df_clean[col] = self.df_clean[col].replace({"nan": np.nan, "None": np.nan, "": np.nan})

        # 3. Drop exact duplicates
        self.df_clean.drop_duplicates(inplace=True)

        # 4. Infer data types
        self.df_clean = self.df_clean.infer_objects()

        self.refresh_ui()

    def clean_headers(self):
        if self.df_clean.empty:
            return
        self.df_clean.columns = (
            self.df_clean.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"[^\w\s]", "", regex=True)
            .str.replace(r"\s+", "_", regex=True)
        )
        self.refresh_ui()

    def trim_spaces(self):
        if self.df_clean.empty:
            return
        str_cols = self.df_clean.select_dtypes(include=["object"]).columns
        for col in str_cols:
            self.df_clean[col] = self.df_clean[col].astype(str).str.strip()
            self.df_clean[col] = self.df_clean[col].replace({"nan": np.nan, "": np.nan})
        self.refresh_ui()

    def drop_duplicates(self):
        if self.df_clean.empty:
            return
        self.df_clean.drop_duplicates(inplace=True)
        self.refresh_ui()

    def handle_nulls(self):
        if self.df_clean.empty:
            return
        strat = self.cmb_null_strategy.currentText()
        if strat == "Drop Null Rows":
            self.df_clean.dropna(inplace=True)
        elif strat == "Fill 0 / N/A":
            num_cols = self.df_clean.select_dtypes(include=[np.number]).columns
            obj_cols = self.df_clean.select_dtypes(include=["object"]).columns
            self.df_clean[num_cols] = self.df_clean[num_cols].fillna(0)
            self.df_clean[obj_cols] = self.df_clean[obj_cols].fillna("N/A")
        elif strat == "Fill Mean (Numeric)":
            num_cols = self.df_clean.select_dtypes(include=[np.number]).columns
            self.df_clean[num_cols] = self.df_clean[num_cols].fillna(self.df_clean[num_cols].mean())

        self.refresh_ui()

    def drop_column(self):
        col = self.cmb_columns.currentText()
        if col and col in self.df_clean.columns:
            self.df_clean.drop(columns=[col], inplace=True)
            self.refresh_ui()

    def convert_types(self):
        if self.df_clean.empty:
            return
        for col in self.df_clean.columns:
            # Try numeric
            converted_num = pd.to_numeric(self.df_clean[col], errors="ignore")
            if not converted_num.equals(self.df_clean[col]):
                self.df_clean[col] = converted_num
                continue
            # Try datetime
            try:
                converted_dt = pd.to_datetime(self.df_clean[col], errors="raise")
                self.df_clean[col] = converted_dt
            except Exception:
                pass
        self.refresh_ui()

    # ==========================================
    # UI STATE UPDATE
    # ==========================================
    def refresh_ui(self):
        self.table_model.update_data(self.df_clean)

        # Update columns dropdown
        self.cmb_columns.clear()
        self.cmb_columns.addItems([str(c) for c in self.df_clean.columns])

        # Update stats
        rows = len(self.df_clean)
        cols = len(self.df_clean.columns)
        nulls = self.df_clean.isna().sum().sum()
        dups = self.df_clean.duplicated().sum()

        self.lbl_stats.setText(
            f"Rows: {rows:,}  |  Columns: {cols:,}  |  Missing Values: {nulls:,}  |  Duplicates: {dups:,}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SimpleDataCleaner()
    win.show()
    sys.exit(app.exec())