# Finance DataMart Tool (MVP)

이 도구는 여러 월별 Excel Raw Data 파일을 폴더 단위로 관리하고, 사용자가 정의한 Excel Config 기준에 따라 필요한 컬럼만 정제·통합한 뒤, Excel 등 리포트 도구에서 즉시 활용할 수 있는 Clean Table과 Report View(Summary)를 생성하는 로컬 데이터마트 빌더의 최소 기능 제품(MVP)입니다.

현재 구현된 단계는 **Phase 0 ~ Phase 22 Python 미설치 PC용 독립 실행 배포판 및 설치파일 준비**로, `Sales_Closing` 및 `AR_Detail` 가상 데이터를 기반으로 전체적인 데이터 흐름(Raw Excel → Config → Clean CSV → Summary CSV)이 작동하며, Config 무결성 검증, Reconciliation(대조 정합성 검증), tkinter 기반 Desktop UI, pre-release 자가 무결성 진단 스크립트, MIT 라이선스 파일, 다른 PC 설치 테스트 가이드, 그리고 AppData 설치용 독립 실행 Setup 파일이 정립되어 있습니다. GitHub 저장소에는 소스코드와 문서를 올리고, GitHub Release에는 선택적으로 `FinanceDataMart_Setup.exe`를 첨부합니다.

## 📖 배포 문서 가이드
보다 상세한 동작 이해와 제한 사항 확인을 위해 아래 문서를 참고하십시오:
- [GitHub 업로드 가이드 (GITHUB_RELEASE_GUIDE.md)](GITHUB_RELEASE_GUIDE.md): 수동 저장소 연동 및 최초 배포 태깅 절차
- [릴리즈 노트 (RELEASE_NOTES.md)](RELEASE_NOTES.md): v1.0.0-RC1 사양 및 Release Candidate 확인 절차
- [제3자 소프트웨어 고지서 (THIRD_PARTY_NOTICES.md)](THIRD_PARTY_NOTICES.md): 외부 오픈소스 패키지(Pandas, OpenPyXL) 라이선스 정보
- [사용자 가이드 (USER_GUIDE.md)](USER_GUIDE.md): 스크립트 실행 순서, 설정 매핑, 결과 분석 안내
- [기술 제약 사항 (KNOWN_LIMITATIONS.md)](KNOWN_LIMITATIONS.md): Pandas 인메모리 대용량 제한, 미지원 연동 플랫폼 안내
- [공개 전 체크리스트 (PUBLIC_RELEASE_CHECKLIST.md)](PUBLIC_RELEASE_CHECKLIST.md): GitHub 배포 전 보안 및 검열 점검사항
- [유지보수 및 이슈 대응 가이드 (MAINTENANCE.md)](MAINTENANCE.md): 배포 후 버그 핫픽스 및 이슈 보안 규정
- [릴리즈 매니페스트 (RELEASE_MANIFEST.md)](RELEASE_MANIFEST.md): 공식 배포 파일 목록 정의서
- [공식 배포 핸드오프 지침서 (OFFICIAL_RELEASE_HANDOFF.md)](OFFICIAL_RELEASE_HANDOFF.md): 공개 업로드 전 최종 수동 점검 요약서
- [공개 후 초기 확인 체크리스트 (POST_RELEASE_CHECKLIST.md)](POST_RELEASE_CHECKLIST.md): 공개 업로드 직후 위생 및 동작 재검토용 체크리스트
- [라이선스 최종 결정 가이드 (LICENSE_DECISION_GUIDE.md)](LICENSE_DECISION_GUIDE.md): 사용자의 오픈소스 라이선스 검토 및 결정용 안내서
- [MIT License (LICENSE)](LICENSE): 프로젝트 공식 오픈소스 라이선스 전문
- [배포 버전 설치 테스트 가이드 (DISTRIBUTION_TEST_GUIDE.md)](DISTRIBUTION_TEST_GUIDE.md): 타 PC 환경에서 소스코드를 받아 설치 및 기동을 수동 검증하기 위한 PowerShell 가이드라인

---

## 🚫 중요 원칙 및 제약 사항 (절대 준수)
- **공식 라이선스**: 본 프로젝트는 MIT License로 배포되며, 재배포 시 루트의 `LICENSE` 고지 전문을 유지해야 합니다.
- **CLI 우선 및 최소 UI 제공**: 기본 실행은 CLI 스크립트 기반이며, 보조 수단으로 tkinter 기반 최소 Desktop UI를 제공합니다. `FinanceDataMart_Setup.exe`는 Python 런타임과 의존 라이브러리를 포함한 독립 실행형 AppData 설치 파일이며, 설치 후 `%LOCALAPPDATA%\FinanceDataMart\FinanceDataMart.exe`를 실행합니다.
- **Lightweight 스택**: DuckDB, Parquet와 같은 중량 데이터베이스나 바이너리 포맷은 배제하고, Pandas와 CSV 파일 포맷만을 활용합니다.
- **원본 보존**: Raw Excel 파일은 **읽기 전용**으로만 처리하며, 값을 수정하거나 시트를 추가하지 않습니다.
- **익명 데이터**: 저장소 내에는 회사 실명, 실제 매출 금액 등 어떠한 실제 민감 정보도 포함하지 않으며, 오직 가상 데이터(Customer A, M-100 등)로만 테스트를 진행합니다.

---

## 🛠️ 설치 및 사전 준비

본 프로젝트는 두 가지 설치 방식을 지원합니다.

### 방법 A: 독립 실행형 Setup 인스톨러 사용 (권장 - 파이썬 미설치 PC 및 격리 환경)
GitHub Releases에서 제공하는 `FinanceDataMart_Setup.exe`를 다운로드하여 실행하면, 대상 PC에 **Python이 설치되어 있지 않고 인터넷 연결이 끊겨 있어도** 사용자의 **AppData** 로컬 폴더(`%LOCALAPPDATA%\FinanceDataMart`)에 실제 GUI 단일 실행 파일(`FinanceDataMart.exe`), 마스터 가이드 문서, 그리고 가상 샘플 데이터마트 구조(`sample_workspace`)를 1초 만에 자동 배치하고 바탕화면에 실행 바로가기를 생성합니다.

> [!WARNING]
> Windows 환경에 따라 최초 설치 실행 시 코드 서명 미지원을 이유로 **Windows SmartScreen(보호 팝업)** 창이 뜰 수 있습니다. 이 경우 "추가 정보 ➔ 실행"을 클릭하여 설치를 진행하십시오.

### 방법 B: 소스코드 수동 설치 (Windows PowerShell 기준)
본 프로젝트는 **Python 3.8 이상** 환경에서 구동됩니다. 다른 PC에서 수동 설치 및 검증을 진행할 때는 패키지 충돌 방지를 위해 아래와 같이 파이썬 가상환경을 활성화한 뒤 의존 패키지를 설치하십시오.
```powershell
# 1. 가상환경 생성
python -m venv .venv

# 2. 가상환경 활성화 (PowerShell 권한 우회 포함)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1

# 3. 필요한 외부 라이브러리 설치
pip install -r requirements.txt
```
*(기본 의존성: `pandas`, `openpyxl`)*

---

## 🚀 실행 방법

### 1단계: 가상 샘플 데이터 및 설정 생성
테스트를 위해 가상 폴더 구조를 만들고, `config.xlsx` 및 2026년 1~2월의 가상 Raw Excel 파일을 자동으로 생성합니다.
```bash
python scripts/create_sample_data.py
```
실행이 완료되면 `sample_workspace/` 하위에 다음과 같은 가상 인프라가 구성됩니다:
- `01_Input_Raw/Sales_Closing/`: 가상 매출 엑셀 파일들
- `01_Input_Raw/AR_Detail/`: 가상 매출 채권 엑셀 파일들
- `90_Config/config.xlsx`: Source Config, Column Mapping, Report View 정의가 포함된 설정 파일

`sample_workspace/`는 다른 PC에서 `scripts/create_sample_data.py`로 재생성하는 로컬 테스트 작업공간이며, GitHub 업로드 대상에는 포함하지 않습니다.

### 2단계: 데이터마트 실행 (Refresh)
아래 명령어를 실행하여 Raw 엑셀 데이터를 정제하고 요약 리포트를 일괄 생성합니다:
```bash
python -m app.main
```

### 3단계: 컬럼 인벤토리 추출 (선택사항)
새로운 Raw Excel 파일이 추가되어 전체 컬럼 내역과 타입 추론 정보를 요약해야 할 때 아래 명령을 실행합니다:
```bash
python scripts/create_column_inventory.py
```
생성된 인벤토리 파일(`column_inventory.xlsx`)을 참고하여 `config.xlsx`의 `Column_Mapping` 시트를 손쉽게 작성할 수 있습니다.

### 4단계: 데스크톱 UI 기동 (선택사항)
비개발자 또는 간편한 조작을 위해 GUI 제어 화면을 띄워 데이터마트를 관리할 수 있습니다:
```bash
python scripts/run_desktop_app.py
```
실행하면 단일 UI 윈도우 창이 나타나며, 데이터마트 갱신, 컬럼 인벤토리 분석, 결과물/로그/설정 파일 탐색 작업을 마우스 클릭으로 수행할 수 있습니다.

### 5단계: 배포 전 무결성 검증 (선택사항)
배포/릴리즈 전 최종 상태를 검사하여 금지 기술 유입, 절대경로 노출, 에러 발생 상태 등을 원클릭 진단할 수 있습니다:
```bash
python scripts/pre_release_check.py
```
데스크톱 GUI 앱 내의 `Run Pre-release Check` 버튼을 눌러서 실행할 수도 있으며, 검증 내역은 `sample_workspace/99_Logs/pre_release_check_log.txt`에 기록됩니다.

---

## 📂 예상 산출물 목록 (Outputs)
프로그램 실행이 끝나면 `sample_workspace/` 내에 아래 결과물이 자동으로 생성됩니다.

1. **정제 및 병합 데이터 (Clean Table)**
   - `sample_workspace/03_Clean_Table/sales_closing_clean.csv` (매출 마감 정제 데이터)
   - `sample_workspace/03_Clean_Table/ar_detail_clean.csv` (매출 채권 정제 데이터)
     - Config의 컬럼 매핑 기준에 맞춰 필터링되고, 표준 컬럼명 및 데이터 타입 캐스팅이 완료된 파일입니다.
     - `posting_month` (기간 파생 컬럼), `source_file`, `loaded_at` (audit 추적 컬럼)이 자동으로 추가됩니다.

2. **요약 보고서 (Report View)**
   - `sample_workspace/04_Report_View/sales_by_customer.csv`: 월별/거래처별 매출 및 수량 합계
   - `sample_workspace/04_Report_View/sales_by_model.csv`: 월별/모델별 매출 및 수량 합계
   - `sample_workspace/04_Report_View/sales_by_customer_model.csv`: 월별/거래처별/모델별 매출 및 수량 합계
   - `sample_workspace/04_Report_View/ar_by_customer.csv`: 월별/거래처별 매출 채권 잔액 요약
   - `sample_workspace/04_Report_View/ar_by_aging_bucket.csv`: 월별/에이징 버킷별(연체 구간별) 채권 잔액 요약
   - `sample_workspace/04_Report_View/sales_invoice_count_by_customer.csv`: 월별/거래처별 매출 인보이스 건수 (count)
   - `sample_workspace/04_Report_View/ar_invoice_count_by_customer.csv`: 월별/거래처별 채권 인보이스 건수 (count)

3. **기록 및 진단 로그 (Logs)**
   - `sample_workspace/99_Logs/refresh_log.csv`: 개별 파일 단위 처리 성공/실패 여부, 처리 건수 기록
   - `sample_workspace/99_Logs/validation_log.csv`: 최종 산출물(Clean CSV, Summary CSVs) 및 설정 무결성 검증 결과 기록
   - `sample_workspace/99_Logs/error_log.txt`: 비정상 에러 발생 시 내부 절대경로를 제외한 사용자 확인용 오류 메시지 기록

---

## ⚠️ 설정 오류 및 예외 로그 확인 방법

사용자가 `config.xlsx` 파일 설정을 기입할 때 다음과 같은 실수를 하면 콘솔 및 로그에 에러 원인이 명확히 기재됩니다:
1. **잘못된 플래그 입력 (Y/N가 아닌 값)**: `config_loader` 검증을 통해 어떤 시트, 어떤 행의 컬럼값에서 오류가 발생했는지 알려줍니다. (예: `In sheet 'Column_Mapping', column 'keep' contains an invalid value 'MAYBE'`)
2. **컬럼명 오타 혹은 누락**: Clean Table에 없는 그룹핑/집계 컬럼을 `Report_View`에 적은 경우, 에러 메시지를 통해 사용 가능한 전체 컬럼 목록(`Available columns`)을 제공합니다.
3. **요약(measures) 집계 포맷 오류**: `net_sales:sum` 처럼 `열이름:집계함수` 형식이 아니거나 지원되지 않는 집계 함수인 경우 친절한 안내 문구와 예시를 표기합니다.
4. **Reconciliation 대조 정합성 실패**: 원본 Excel 데이터와 생성된 Clean Table 간의 행 수(Row Count) 및 수치 합계(Sum)의 소수점 2자리 오차가 0.01을 초과하는 불일치가 날 경우 `FAIL` 로그와 오차 수치를 리포팅합니다.

모든 실행 결과 및 에러는 `sample_workspace/99_Logs/validation_log.csv` 와 `error_log.txt`에 일목요연하게 저장되므로 실행 실패 시 해당 로그를 참고하시기 바랍니다.
