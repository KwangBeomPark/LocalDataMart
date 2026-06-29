from pathlib import Path
import pandas as pd

def create_folders():
    """기본 MVP 디렉토리 구조를 생성합니다. (AR_Detail 폴더 추가)"""
    workspace_dir = Path("sample_workspace")
    folders = [
        workspace_dir / "01_Input_Raw" / "Sales_Closing",
        workspace_dir / "01_Input_Raw" / "AR_Detail",
        workspace_dir / "03_Clean_Table",
        workspace_dir / "04_Report_View",
        workspace_dir / "90_Config",
        workspace_dir / "99_Logs"
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"Folder created: {folder}")

def create_config_excel():
    """sample_workspace/90_Config/config.xlsx 파일을 생성합니다. (AR_Detail 설정 포함)"""
    config_path = Path("sample_workspace/90_Config/config.xlsx")
    
    # 1. Source_Config Sheet Data
    source_config_data = {
        "active": ["Y", "Y"],
        "data_group": ["Sales_Closing", "AR_Detail"],
        "folder_path": [
            "sample_workspace/01_Input_Raw/Sales_Closing",
            "sample_workspace/01_Input_Raw/AR_Detail"
        ],
        "file_pattern": ["*.xlsx", "*.xlsx"],
        "sheet_name": ["Data", "Data"],
        "header_row": [1, 1],
        "period_source": ["filename", "filename"],
        "load_mode": ["replace_by_period", "replace_by_period"]
    }
    df_source = pd.DataFrame(source_config_data)

    # 2. Column_Mapping Sheet Data
    column_mapping_data = {
        "data_group": ["Sales_Closing"] * 6 + ["AR_Detail"] * 6,
        "keep": ["Y"] * 12,
        "raw_column": [
            # Sales_Closing
            "Invoice No", "Customer Code", "Model", "Posting Date", "Net Sales", "Qty",
            # AR_Detail
            "Invoice No", "Customer Code", "Posting Date", "Due Date", "Amount", "Aging Bucket"
        ],
        "standard_column": [
            # Sales_Closing
            "invoice_no", "customer_code", "model", "posting_date", "net_sales", "qty",
            # AR_Detail
            "invoice_no", "customer_code", "posting_date", "due_date", "amount", "aging_bucket"
        ],
        "role": [
            # Sales_Closing
            "key", "dimension", "dimension", "date", "measure", "measure",
            # AR_Detail
            "key", "dimension", "date", "date", "measure", "dimension"
        ],
        "data_type": [
            # Sales_Closing
            "text", "text", "text", "date", "number", "number",
            # AR_Detail
            "text", "text", "date", "date", "number", "text"
        ],
        "required": [
            # Sales_Closing
            "Y", "Y", "N", "Y", "Y", "N",
            # AR_Detail
            "Y", "Y", "Y", "N", "Y", "Y"
        ],
        "aggregation": [
            # Sales_Closing
            "none", "none", "none", "none", "sum", "sum",
            # AR_Detail
            "none", "none", "none", "none", "sum", "none"
        ]
    }
    df_mapping = pd.DataFrame(column_mapping_data)

    # 3. Report_View Sheet Data
    report_view_data = {
        "active": ["Y"] * 7,
        "view_name": [
            "sales_by_customer", "sales_by_model", "sales_by_customer_model",
            "ar_by_customer", "ar_by_aging_bucket",
            "sales_invoice_count_by_customer", "ar_invoice_count_by_customer"
        ],
        "source_table": [
            "sales_closing_clean", "sales_closing_clean", "sales_closing_clean",
            "ar_detail_clean", "ar_detail_clean",
            "sales_closing_clean", "ar_detail_clean"
        ],
        "group_by": [
            "posting_month, customer_code", 
            "posting_month, model", 
            "posting_month, customer_code, model",
            "posting_month, customer_code",
            "posting_month, aging_bucket",
            "posting_month, customer_code",
            "posting_month, customer_code"
        ],
        "measures": [
            "net_sales:sum, qty:sum", 
            "net_sales:sum, qty:sum", 
            "net_sales:sum, qty:sum",
            "amount:sum",
            "amount:sum",
            "invoice_no:count",
            "invoice_no:count"
        ],
        "filter": [""] * 7,
        "output_file": [
            "sales_by_customer.csv", 
            "sales_by_model.csv", 
            "sales_by_customer_model.csv",
            "ar_by_customer.csv",
            "ar_by_aging_bucket.csv",
            "sales_invoice_count_by_customer.csv",
            "ar_invoice_count_by_customer.csv"
        ]
    }
    df_report = pd.DataFrame(report_view_data)

    with pd.ExcelWriter(config_path, engine="openpyxl") as writer:
        df_source.to_excel(writer, sheet_name="Source_Config", index=False)
        df_mapping.to_excel(writer, sheet_name="Column_Mapping", index=False)
        df_report.to_excel(writer, sheet_name="Report_View", index=False)
    
    print(f"Config Excel created: {config_path}")

def create_raw_excel_files():
    """Sales_Closing 및 AR_Detail 하위에 가상 Raw Excel 파일들을 생성합니다."""
    # 1. Sales_Closing 가상 데이터 생성
    sc_dir = Path("sample_workspace/01_Input_Raw/Sales_Closing")
    
    jan_sales = {
        "Invoice No": ["INV-2026-0001", "INV-2026-0002", "INV-2026-0003", "INV-2026-0004", "INV-2026-0005"],
        "Customer Code": ["CUST001", "CUST002", "CUST001", "CUST003", "CUST002"],
        "Model": ["M-100", "M-200", "M-200", "M-100", "M-100"],
        "Posting Date": ["2026-01-05", "2026-01-10", "2026-01-15", "2026-01-20", "2026-01-25"],
        "Net Sales": [1200000, 850000, 1700000, 500000, 600000],
        "Qty": [10, 5, 10, 4, 5],
        "Dummy Column": ["Ignore A", "Ignore B", "Ignore C", "Ignore D", "Ignore E"]
    }
    pd.DataFrame(jan_sales).to_excel(sc_dir / "Sales_Closing_2026_01.xlsx", sheet_name="Data", index=False)
    print(f"Sample Raw Excel created: {sc_dir / 'Sales_Closing_2026_01.xlsx'}")

    feb_sales = {
        "Invoice No": ["INV-2026-0006", "INV-2026-0007", "INV-2026-0008", "INV-2026-0009", "INV-2026-0010"],
        "Customer Code": ["CUST001", "CUST003", "CUST002", "CUST001", "CUST003"],
        "Model": ["M-100", "M-200", "M-200", "M-300", "M-100"],
        "Posting Date": ["2026-02-02", "2026-02-08", "2026-02-14", "2026-02-20", "2026-02-28"],
        "Net Sales": [1300000, 900000, 1800000, 2200000, 400000],
        "Qty": [11, 5, 10, 8, 3],
        "Dummy Column": ["Ignore F", "Ignore G", "Ignore H", "Ignore I", "Ignore J"]
    }
    pd.DataFrame(feb_sales).to_excel(sc_dir / "Sales_Closing_2026_02.xlsx", sheet_name="Data", index=False)
    print(f"Sample Raw Excel created: {sc_dir / 'Sales_Closing_2026_02.xlsx'}")

    # 2. AR_Detail 가상 데이터 생성
    ar_dir = Path("sample_workspace/01_Input_Raw/AR_Detail")
    
    jan_ar = {
        "Invoice No": ["INV-2026-0001", "INV-2026-0002", "INV-2026-0003", "INV-2026-0004", "INV-2026-0005"],
        "Customer Code": ["CUST001", "CUST002", "CUST001", "CUST003", "CUST002"],
        "Posting Date": ["2026-01-05", "2026-01-10", "2026-01-15", "2026-01-20", "2026-01-25"],
        "Due Date": ["2026-02-05", "2026-02-10", "2026-02-15", "2026-02-20", "2026-02-25"],
        "Amount": [5000000, 3000000, 4500000, 1500000, 2000000],
        "Aging Bucket": ["30-60 Days", "30-60 Days", "30-60 Days", "30-60 Days", "30-60 Days"],
        "Dummy Column": ["Dummy X", "Dummy Y", "Dummy Z", "Dummy W", "Dummy V"]
    }
    pd.DataFrame(jan_ar).to_excel(ar_dir / "AR_Detail_2026_01.xlsx", sheet_name="Data", index=False)
    print(f"Sample Raw Excel created: {ar_dir / 'AR_Detail_2026_01.xlsx'}")

    feb_ar = {
        "Invoice No": ["INV-2026-0006", "INV-2026-0007", "INV-2026-0008", "INV-2026-0009", "INV-2026-0010"],
        "Customer Code": ["CUST001", "CUST003", "CUST002", "CUST001", "CUST003"],
        "Posting Date": ["2026-02-02", "2026-02-08", "2026-02-14", "2026-02-20", "2026-02-28"],
        "Due Date": ["2026-03-02", "2026-03-08", "2026-03-14", "2026-03-20", "2026-03-28"],
        "Amount": [6000000, 2500000, 3500000, 7000000, 1200000],
        "Aging Bucket": ["1-30 Days", "1-30 Days", "1-30 Days", "1-30 Days", "1-30 Days"],
        "Dummy Column": ["Dummy T", "Dummy S", "Dummy R", "Dummy Q", "Dummy P"]
    }
    pd.DataFrame(feb_ar).to_excel(ar_dir / "AR_Detail_2026_02.xlsx", sheet_name="Data", index=False)
    print(f"Sample Raw Excel created: {ar_dir / 'AR_Detail_2026_02.xlsx'}")

def generate_all_samples(dest_dir=None):
    """지정 디렉토리 기준(또는 현재 기준)으로 전체 폴더 및 샘플 데이터 구조를 생성합니다."""
    create_folders()
    create_config_excel()
    create_raw_excel_files()
    print("All sample data and configuration generated successfully!")

if __name__ == "__main__":
    generate_all_samples()
