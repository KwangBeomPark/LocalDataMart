# AI_CODE_MAP.MD

> 이 파일은 Finance DataMart Tool의 코드 구조, 모듈 책임, 데이터 흐름, Config 구조, 주의점을 정리한 코드맵이다.  
> AI 코딩 도구는 코드를 수정하기 전에 반드시 이 파일을 읽고, 구조 변경 후에는 이 파일을 업데이트한다.

---

## 1. 프로젝트 개요

프로젝트명: **Finance DataMart Tool**

목적:

여러 월별 Excel Raw Data 파일을 폴더 단위로 읽고, Excel Config 기준으로 필요한 컬럼만 선택·정제·통합하여 Clean Table과 Report View를 생성하는 로컬 데이터마트 도구를 만든다.

초기 목표:

```text
Sales_Closing 데이터 그룹 하나를 대상으로
Raw Excel → Clean CSV → Summary CSV
흐름을 구현한다.
```

장기 목표:

```text
여러 데이터 그룹을 Config 기반으로 처리하고,
비개발자도 사용할 수 있는 데스크탑 앱으로 발전시킨다.
```

---

## 2. 현재 개발 단계

현재 단계:

```text
Phase 0 ~ Phase 20 배포 버전 GitHub 업로드 및 다른 PC 설치 테스트 준비
```

현재 구현 우선순위:

1. 프로젝트 기본 구조 생성
2. Config 구조 설계
3. Sales_Closing 샘플 데이터 처리
4. AR_Detail 샘플 데이터 처리
5. Clean CSV 생성
6. Report View CSV 생성
7. sum/count Report View 설정 검증
8. Column Inventory 생성
9. 로그 생성

현재 단계에서 제외:

```text
복잡한 GUI
DuckDB
Parquet
exe 패키징
다중 데이터 그룹 대규모 확장
복잡한 Validation Rule
실제 회사 데이터 처리
```

---

## 3. 권장 프로젝트 폴더 구조

초기 권장 구조:

```text
FinanceDataMartTool/
│
├─ myAGENT.MD
├─ AI_CODE_MAP.MD
├─ PROJECT_ROADMAP.MD
├─ README.md
├─ RELEASE_NOTES.md
├─ THIRD_PARTY_NOTICES.md
├─ USER_GUIDE.md
├─ KNOWN_LIMITATIONS.md
├─ PUBLIC_RELEASE_CHECKLIST.md
├─ GITHUB_RELEASE_GUIDE.md
├─ MAINTENANCE.md
├─ RELEASE_MANIFEST.md
├─ OFFICIAL_RELEASE_HANDOFF.md
├─ POST_RELEASE_CHECKLIST.md
├─ LICENSE_DECISION_GUIDE.md
├─ LICENSE
├─ DISTRIBUTION_TEST_GUIDE.md
├─ requirements.txt
├─ .gitignore
│
├─ app/
│   ├─ __init__.py
│   ├─ main.py
│   ├─ config_loader.py
│   ├─ file_scanner.py
│   ├─ excel_reader.py
│   ├─ transformer.py
│   ├─ report_generator.py
│   ├─ validator.py
│   ├─ logger_setup.py
│   ├─ column_inventory.py
│   ├─ ui_app.py
│   └─ models.py
│
├─ scripts/
│   ├─ create_sample_data.py
│   ├─ create_column_inventory.py
│   ├─ run_desktop_app.py
│   └─ pre_release_check.py
│
├─ templates/
│   └─ config_template.xlsx
│
├─ sample_workspace/
│   ├─ 01_Input_Raw/
│   │   ├─ Sales_Closing/
│   │   └─ AR_Detail/
│   ├─ 03_Clean_Table/
│   ├─ 04_Report_View/
│   ├─ 90_Config/
│   │   └─ config.xlsx
│   └─ 99_Logs/
│
└─ tests/
    └─ sample_data/
```

---

## 4. Runtime Workspace 구조

실제 사용 시에는 로컬 폴더 또는 네트워크 드라이브에 Workspace를 둔다.

예상 구조:

```text
Finance_DataMart_Workspace/
│
├─ 01_Input_Raw/
│   ├─ Sales_Closing/
│   ├─ AR_Detail/
│   ├─ Profitability/
│   ├─ Inventory/
│   └─ VAT_Check/
│
├─ 03_Clean_Table/
│   ├─ sales_closing_clean.csv
│   └─ ar_detail_clean.csv
│
├─ 04_Report_View/
│   ├─ sales_by_customer.csv
│   ├─ sales_by_model.csv
│   ├─ sales_by_customer_model.csv
│   ├─ ar_by_customer.csv
│   ├─ ar_by_aging_bucket.csv
│   ├─ sales_invoice_count_by_customer.csv
│   └─ ar_invoice_count_by_customer.csv
│
├─ 90_Config/
│   └─ config.xlsx
│
└─ 99_Logs/
    ├─ refresh_log.csv
    ├─ validation_log.csv
    └─ error_log.txt
```

초기 개발에서는 `sample_workspace/`를 기준으로 테스트한다.

---

## 5. 전체 데이터 흐름

MVP 데이터 흐름:

```text
1. config.xlsx 읽기
2. Source_Config에서 active = Y data_group 폴더 정보 확인
3. Raw Excel 파일 목록 스캔
4. Column_Mapping에서 keep = Y 컬럼 확인
5. Raw Excel에서 필요한 컬럼만 읽기
6. 표준 컬럼명으로 변경
7. 필수 컬럼 검증
8. audit 컬럼 추가
   - source_file
   - loaded_at
9. data_group별 Clean CSV 생성
10. Report_View 기준으로 group_by / aggregation 실행
11. Summary CSV 생성
12. 로그 저장
```

---

## 6. 모듈별 역할

## 6.1 `app/main.py`

역할:

- 프로그램 실행 진입점
- 전체 workflow orchestration
- config 읽기
- 데이터 그룹별 처리 순서 호출
- 에러 발생 시 로그 처리

초기 책임:

```text
load_config()
scan_source_files()
load_and_transform_files()
write_clean_table()
generate_report_views()
write_logs()
```

주의:

- 모든 비즈니스 로직을 main.py에 넣지 않는다.
- main.py는 흐름 제어만 담당한다.

---

## 6.2 `app/config_loader.py`

역할:

- `config.xlsx` 읽기
- `Source_Config`, `Column_Mapping`, `Report_View` Sheet 파싱
- Config DataFrame 반환
- 기본 Config 검증

주요 함수 후보:

```python
load_config(config_path)
load_source_config(config_path)
load_column_mapping(config_path)
load_report_view_config(config_path)
validate_config_sheets(config_path)
```

주의:

- Config Sheet 이름은 상수로 관리한다.
- Sheet가 없으면 명확한 에러 메시지를 반환한다.
- Config 구조를 코드에 과도하게 하드코딩하지 않는다.

---

## 6.3 `app/file_scanner.py`

역할:

- Source_Config 기준으로 Raw 폴더 스캔
- file_pattern에 맞는 Excel 파일 목록 반환
- 처리 대상 파일 정렬
- 향후 파일 변경 감지 확장

주요 함수 후보:

```python
scan_source_files(source_config_row)
get_excel_files(folder_path, file_pattern)
```

초기 처리 대상 확장자:

```text
.xlsx
.xlsm
```

향후 확장:

```text
.csv
.xlsb
```

주의:

- Raw 파일은 수정하지 않는다.
- 임시 파일 또는 Excel lock 파일은 제외한다.
- 예: `~$filename.xlsx` 제외

---

## 6.4 `app/excel_reader.py`

역할:

- Excel 파일 읽기
- 필요한 컬럼만 선택해서 읽기
- Sheet명, header_row 적용
- 파일별 DataFrame 반환

주요 함수 후보:

```python
read_excel_file(file_path, sheet_name, header_row, use_columns)
read_selected_columns(file_path, source_config, column_mapping)
```

주의:

- 가능한 경우 필요한 컬럼만 읽는다.
- Raw 파일 전체를 무조건 읽지 않는다.
- 파일 읽기 실패 시 어떤 파일에서 실패했는지 로그에 남긴다.

---

## 6.5 `app/transformer.py`

역할:

- Raw 컬럼명을 standard_column으로 변경
- 데이터 타입 변환
- audit 컬럼 추가
- derived column 생성
- Clean Table DataFrame 생성

주요 함수 후보:

```python
apply_column_mapping(df, column_mapping)
standardize_columns(df, column_mapping)
convert_data_types(df, column_mapping)
add_audit_columns(df, source_file)
add_period_columns(df, source_config)
combine_dataframes(dataframes)
```

초기 파생 컬럼 후보:

```text
posting_month
source_file
loaded_at
```

주의:

- 변환 규칙은 Config를 우선한다.
- 하드코딩된 특정 회사 로직을 넣지 않는다.

---

## 6.6 `app/report_generator.py`

역할:

- Clean Table 기준으로 Report View 생성
- Report_View Config 파싱
- group_by와 measures 처리
- Summary CSV 저장

주요 함수 후보:

```python
generate_report_views(clean_tables, report_view_config, output_folder)
parse_group_by(group_by_text)
parse_measures(measures_text)
generate_summary(df, group_by, measures)
write_report_csv(df, output_file)
```

초기 지원 aggregation:

```text
sum
count
```

향후 지원 aggregation:

```text
average
count_distinct
min
max
weighted_avg
```

주의:

- Report View는 Raw 파일이 아니라 Clean Table을 기준으로 생성한다.
- 새로운 report view는 Config 한 줄 추가로 생성 가능해야 한다.

---

## 6.7 `app/validator.py`

역할:

- Config 검증
- 필수 컬럼 검증
- Output 생성 여부 검증
- 원본(Raw Excel)과 Clean Table 간의 행 수(Row Count), 필수 컬럼 결측(Null Check), measure 합계(Sum Check) 대조 검증 (Reconciliation)

주요 함수 후보:

```python
validate_raw_columns(df, required_columns, file_name)
validate_outputs(clean_table_paths, report_view_paths)
validate_reconciliation(active_sources, df_mapping, clean_tables)
```

초기 Validation:

```text
필수 Sheet 존재 여부
필수 컬럼 존재 여부
필수 Config 값 누락 여부
Raw 폴더 존재 여부
Output 생성 여부
```

향후 Validation:

```text
row_count 비교
amount_total 비교
duplicate key 확인
date type 확인
number type 확인
```

---

## 6.8 `app/logger_setup.py`

역할:

- 로그 설정
- refresh_log.csv 작성
- validation_log.csv 작성
- error_log.txt 작성

주요 함수 후보:

```python
setup_logger(log_folder)
write_refresh_log(log_records, log_folder)
write_validation_log(validation_records, log_folder)
write_error_log(error, log_folder)
```

로그 원칙:

- 민감한 line-level data를 기록하지 않는다.
- 파일명, row count, status, message 중심으로 기록한다.
- 실패 시 사용자가 이해할 수 있는 메시지를 남긴다.

---

## 6.9 `app/models.py`

역할:

- Config row 구조를 dataclass로 정의
- 필요 시 type hint용 모델 정의

후보 모델:

```python
SourceConfig
ColumnMapping
ReportViewConfig
ProcessResult
ValidationResult
```

MVP에서는 dataclass가 과도하면 생략 가능하다.  
단, 구조가 복잡해지면 models.py를 사용한다.

---

## 6.10 `app/column_inventory.py`

역할:

- Raw Excel 파일들의 헤더 및 컬럼 데이터 스캔
- 데이터 형태(Type), 고유 값 샘플링, 결측치(Null) 개수 및 비율 산출
- `column_inventory.xlsx` 파일 생성

주요 함수:

```python
- infer_column_type(series)
- collect_sample_values(series, max_samples)
- generate()
```

---

## 6.11 `app/ui_app.py`

역할:

- tkinter 기반 Desktop UI 홈 구성
- 비개발자용 데이터마트 새로고침(Refresh), 컬럼 인벤토리 분석(Generate Inventory) 버튼 연동
- Windows 탐색기를 활용한 산출물 폴더, 로그 폴더, 설정 엑셀 파일 바로가기 제공
- 비동기식 명령 실행 구조를 통한 UI 정지(Freeze) 및 중복 클릭 방지 처리

주요 함수:

```python
launch()
on_refresh()
on_generate_inventory()
_open_path(path)
```

---

## 7. Config 구조

초기 Config 파일:

```text
sample_workspace/90_Config/config.xlsx
```

필수 Sheet:

```text
Source_Config
Column_Mapping
Report_View
```

---

## 7.1 Source_Config

목적:

어떤 데이터 그룹이 어떤 폴더와 파일을 읽는지 정의한다.

필드:

| 필드명 | 설명 |
|---|---|
| active | Y/N |
| data_group | 데이터 그룹명 |
| folder_path | Raw 파일 폴더 |
| file_pattern | 파일 패턴 |
| sheet_name | 읽을 Sheet명 |
| header_row | 헤더 행 번호 |
| period_source | 기간 기준 |
| load_mode | 적재 방식 |

초기 예시:

```text
active: Y
data_group: Sales_Closing
folder_path: sample_workspace/01_Input_Raw/Sales_Closing
file_pattern: *.xlsx
sheet_name: Data
header_row: 1
period_source: filename
load_mode: replace_by_period
```

---

## 7.2 Column_Mapping

목적:

Raw 컬럼 중 어떤 컬럼을 유지하고 어떤 표준 컬럼명으로 바꿀지 정의한다.

필드:

| 필드명 | 설명 |
|---|---|
| data_group | 데이터 그룹명 |
| keep | Y/N |
| raw_column | 원본 컬럼명 |
| standard_column | 표준 컬럼명 |
| role | key/dimension/date/date_group/measure/audit |
| data_type | text/number/date/datetime |
| required | Y/N |
| aggregation | none/sum/count/average 등 |

초기 예시:

```text
Sales_Closing | Y | Invoice No | invoice_no | key | text | Y | none
Sales_Closing | Y | Customer Code | customer_code | dimension | text | Y | none
Sales_Closing | Y | Model | model | dimension | text | N | none
Sales_Closing | Y | Posting Date | posting_date | date | date | Y | none
Sales_Closing | Y | Net Sales | net_sales | measure | number | Y | sum
Sales_Closing | Y | Qty | qty | measure | number | N | sum
```

---

## 7.3 Report_View

목적:

Clean Table에서 어떤 Summary 파일을 만들지 정의한다.

필드:

| 필드명 | 설명 |
|---|---|
| active | Y/N |
| view_name | Report View 이름 |
| source_table | 기준 Clean Table |
| group_by | 그룹핑 컬럼 |
| measures | 집계 컬럼 및 방식 |
| filter | 필터 조건 |
| output_file | 생성 파일명 |

초기 예시:

```text
sales_by_customer
source_table: sales_closing_clean
group_by: posting_month, customer_code
measures: net_sales:sum, qty:sum
output_file: sales_by_customer.csv
```

---

## 8. 초기 Clean Table 구조

초기 파일:

```text
sales_closing_clean.csv
```

초기 표준 컬럼 후보:

```text
invoice_no
customer_code
customer_name
model
product_group
posting_date
posting_month
net_sales
qty
source_file
loaded_at
```

주의:

- Clean Table에는 필요한 컬럼만 남긴다.
- Raw 전체 컬럼을 저장하지 않는다.
- source_file과 loaded_at은 추적을 위해 추가한다.

---

## 9. 초기 Report View 구조

초기 생성 대상:

```text
sales_by_customer.csv
sales_by_model.csv
sales_by_customer_model.csv
```

### sales_by_customer.csv

group_by:

```text
posting_month, customer_code
```

measures:

```text
net_sales:sum, qty:sum
```

### sales_by_model.csv

group_by:

```text
posting_month, model
```

measures:

```text
net_sales:sum, qty:sum
```

### sales_by_customer_model.csv

group_by:

```text
posting_month, customer_code, model
```

measures:

```text
net_sales:sum, qty:sum
```

---

## 10. 향후 데이터 그룹 확장

MVP 이후 확장 후보:

```text
AR_Detail
Profitability
Inventory
VAT_Check
Claims
```

확장 원칙:

- 새 데이터 그룹을 추가해도 엔진 구조는 바꾸지 않는다.
- Config에 data_group을 추가하는 방식으로 확장한다.
- 데이터 그룹별 특수 로직은 최소화한다.
- 특수 로직이 필요하면 명확히 분리한다.

---

## 11. 성능 개선 방향

MVP에서는 CSV와 pandas 중심으로 구현한다.

향후 데이터량이 커지면 다음을 검토한다.

```text
필요 컬럼만 읽기 강화
파일 변경 감지
CSV → Parquet
pandas groupby → DuckDB SQL
처리된 파일 registry 생성
로컬 temp 처리 후 네트워크 드라이브에 결과 저장
```

주의:

- 성능 개선은 MVP가 동작한 이후에 한다.
- DuckDB와 Parquet는 처음부터 넣지 않는다.

---

## 12. GUI 확장 방향

Phase 8에서는 tkinter 기반 최소 Desktop UI만 제공한다.

향후 버튼형 UI 후보:

```text
[Scan Columns]
[Open Config]
[Refresh DataMart]
[Generate Reports]
[Open Output Folder]
[Open Log Folder]
```

GUI 구현 후보:

```text
tkinter
PySide6
```

GUI는 내부 엔진이 안정된 후 추가한다.

---

## 13. 배포 방향

현재 배포 방향은 **다른 PC 설치 테스트용 source-only 배포 버전 업로드**이다.

목표:

```text
GitHub에는 배포 테스트에 필요한 소스코드와 문서만 업로드한다.
사용자는 다른 PC에서 clone/download 후 Python 환경을 구성해 실제 설치성과 실행성을 확인한다.
테스트 결과와 불편 사항을 피드백으로 모아 다음 개발 단계의 개선 범위를 결정한다.
```

현재 포함 대상:

```text
app/
scripts/
requirements.txt
README.md
USER_GUIDE.md
RELEASE_MANIFEST.md
GITHUB_RELEASE_GUIDE.md
PUBLIC_RELEASE_CHECKLIST.md
POST_RELEASE_CHECKLIST.md
MIT LICENSE
기타 공개/유지보수 문서
```

현재 제외 대상:

```text
sample_workspace 런타임 산출 CSV/log/xlsx
__pycache__
.venv / .env
실제 회사 데이터
내부 절대경로
개인 PC 전용 파일
```

초기 실행은 Python script로 수행한다.

향후:

```text
PyInstaller로 exe 생성
sample_workspace 포함
templates 포함
USER_GUIDE.md 작성
GitHub Release 구성 또는 GitHub 저장소 업로드
```

배포 버전 업로드 전 확인:

```text
실제 회사 데이터 없음
실제 내부 경로 없음
샘플 데이터 익명화
LICENSE 추가
THIRD_PARTY_NOTICES.md 추가 검토
```

---

## 14. 주의해야 할 설계 리스크

### 14.1 과도한 초기 설계

리스크:

처음부터 GUI, DuckDB, Parquet, 다중 데이터 그룹을 모두 넣으면 프로젝트가 커지고 작동하는 MVP가 늦어진다.

대응:

Sales_Closing 하나만 먼저 구현한다.

### 14.2 Raw 컬럼 전체 관리

리스크:

컬럼이 많아지면 Config가 관리 불가능해진다.

대응:

keep = Y 컬럼만 Config에서 관리한다.

### 14.3 회사 전용 로직 하드코딩

리스크:

GitHub 공개가 어려워지고 다른 데이터에 적용하기 어려워진다.

대응:

범용 명칭과 Config 기반 처리를 유지한다.

### 14.4 Raw Data 수정

리스크:

원본 훼손, 감사 추적 실패, 사용자 신뢰 하락.

대응:

Raw Data는 읽기 전용으로 처리한다.

---

## 15. 변경 시 업데이트 규칙

다음 변경이 발생하면 이 파일을 업데이트한다.

```text
새 모듈 추가
모듈 역할 변경
폴더 구조 변경
Config Sheet 변경
Clean Table 구조 변경
Report View 구조 변경
주요 workflow 변경
새 데이터 그룹 추가
```

정확한 라인 번호는 기록하지 않는다.  
구조와 책임 중심으로 기록한다.

---

## 16. 현재 상태 요약

현재 상태:

```text
Phase 20 완료 (배포 버전 GitHub 업로드 및 다른 PC 설치 테스트 준비 완료)
```

현재 목표:

```text
Phase 21 타 PC 설치 테스트 피드백 반영 및 다음 기능 개발 범위 논의
```

완료된 작업:

```text
1. 프로젝트 루트 및 app/ 모듈 폴더 생성
2. requirements.txt 및 .gitignore 작성
3. 가상 Config(config.xlsx) 및 Raw Excel 데이터 2개(1~2월) 생성 유틸리티 스크립트 작성
4. Config 기반 데이터 스캔, 정제 및 Clean Table CSV(sales_closing_clean.csv) 병합 저장 흐름 구현
5. Report_View 3종(Customer별, Model별, Customer+Model별) 일괄 집계 및 Summary CSV 생성
6. 로그 시스템 구축(refresh_log.csv, validation_log.csv, error_log.txt) 및 최종 결과 Validation PASS 완료
7. Config 시트별 Y/N 플래그 유효성 검증 및 Report_View 내 오타 시 가용 컬럼 안내 등 에러 상세화 완료
8. Column Inventory 기능(column_inventory.xlsx 자동 추출) 신설 및 스키마 분석 검증 성공
9. 다중 데이터 소스 그룹(Sales_Closing, AR_Detail)의 스캔, 정제 및 요약 통합 파이프라인 연동 성공
10. Report View Engine 설정 조기 검증(source_table 존재, group_by/measures 컬럼 실존, sum/count 함수 유효성) 및 count 집계 리포트 2종 생성 검증 성공
11. 원본 Excel과 Clean Table CSV 간의 행 수 대조, 필수 컬럼 결측치 대조, measure(Net Sales, Amount) 컬럼 합계 오차 대조 Reconciliation 정합성 검증 완료
12. tkinter 기반 최소 Desktop UI 제어 패널(Refresh, Generate Inventory, 파일/폴더 바로가기) 및 subprocess 비동기 처리 연동 완료
13. 배포 전 무결성 자가 진단 스크립트(scripts/pre_release_check.py) 작성 및 GUI 연동(Run Pre-release Check 버튼 추가) 완료
14. 사용자 가이드(USER_GUIDE.md), 기술적 제약 사항(KNOWN_LIMITATIONS.md), 공개 전 체크리스트(PUBLIC_RELEASE_CHECKLIST.md) 작성 완료
15. 릴리즈 노트(RELEASE_NOTES.md, v1.0.0-RC1), 제3자 고지서(THIRD_PARTY_NOTICES.md) 신규 작성 및 .gitignore 캐시 제외 처리 최신화 완료
16. GitHub 수동 업로드 및 최초 릴리즈 가이드(GITHUB_RELEASE_GUIDE.md) 신규 작성 및 공개 체크리스트 보완 완료
17. 유지보수 및 보안 가이드라인(MAINTENANCE.md) 신규 작성 및 공개 체크리스트/릴리즈노트 변경이력 지침 보완 완료
18. 배포 대상 파일 33종의 리스트 정합성을 명세하는 공식 배포 매니페스트(RELEASE_MANIFEST.md) 갱신 완료
19. 공개 업로드 직전 최종 수동 점검 및 라이선스 탑재 완료 요약서(OFFICIAL_RELEASE_HANDOFF.md) 갱신 완료
20. 공개 업로드 직후 원격 리포지토리 위생 및 배포 격리성 검사용 사후 체크리스트(POST_RELEASE_CHECKLIST.md) 갱신 완료
21. 라이선스 최종 결정 가이드(LICENSE_DECISION_GUIDE.md) 신규 작성 및 사용자가 선택한 MIT License 파일 공식 추가 완료
22. 다른 PC에서의 수동 설치 테스트 및 검증 절차서(DISTRIBUTION_TEST_GUIDE.md) 신규 작성 완료
```
```
