# Finance DataMart Tool 사용자 가이드 (USER_GUIDE.md)

본 가이드는 Finance DataMart Tool을 처음 사용하는 사용자 및 비개발자를 위한 상세 사용 설명서입니다. 본 도구는 복잡한 데이터베이스 서버 없이도 엑셀 설정에 기반하여 여러 원본 엑셀 데이터를 정제하고 요약 리포트를 생성해 줍니다.

---

## 📌 1. 프로젝트 목적 및 핵심 정제 원칙
1. **Raw Excel 보존 원칙**: 입력되는 원본 Excel 파일들은 절대 직접 수정하지 않으며 오직 읽기 전용으로만 파싱합니다.
2. **Config 기반 keep = Y 컬럼 선택**: `config.xlsx` 파일의 `Column_Mapping` 시트에 지정된 `keep = Y` 컬럼들만 남겨 정제 데이터를 구성합니다.
3. **가상 데이터 사용**: 기본 생성되는 `sample_workspace` 폴더 내의 데이터들은 회사의 실제 기업명, 거래처명, 제품명, 금액을 배제한 임의의 가상 데이터(Sample Data)입니다.

---

## 🛠️ 2. 환경 설정 및 설치
본 프로그램은 Python 3.10 이상 환경을 기준으로 테스트되었으며, Pandas와 OpenPyXL 패키지를 사용합니다.

```bash
# 1. 의존성 패키지 설치
pip install -r requirements.txt
```

---

## 🚀 3. 단계별 실행 방법

### 1단계: 가상 샘플 데이터 및 설정 생성
처음 실행하거나 초기 테스트 시 가상의 Raw 데이터와 설정 파일을 재생성합니다:
```bash
python scripts/create_sample_data.py
```
- **생성 위치**: `sample_workspace/90_Config/config.xlsx` 및 `sample_workspace/01_Input_Raw/`

### 2단계: 데이터마트 정제 및 요약 실행 (CLI)
설정 파일 기준에 맞춰 데이터를 클리닝하고 요약 리포트를 일괄 생성합니다:
```bash
python -m app.main
```
- 원본 행수와 정제 행수, 수치 합계가 오차 0.01 범위 내로 정확한지 Reconciliation(대조) 작업이 자동으로 수행됩니다.

### 3단계: 컬럼 인벤토리 분석 실행
신규 데이터 소스가 들어왔을 때, 컬럼 구성과 데이터 타입을 미리 파악하여 설정을 돕는 인벤토리를 생성합니다:
```bash
python scripts/create_column_inventory.py
```
- **생성 위치**: `sample_workspace/90_Config/column_inventory.xlsx`

### 4단계: 데스크톱 GUI 제어 패널 실행 (선택)
CLI 타이핑 없이 원클릭 마우스 조작으로 데이터마트를 구동할 수 있습니다:
```bash
python scripts/run_desktop_app.py
```
- 화면에서 데이터마트 정제, 컬럼 인벤토리 생성, 배포전 무결성 검증, 결과/로그 폴더 단축 경로 열기가 가능합니다.

### 5단계: 배포 전 무결성 자가 진단 실행
배포 전 금지 키워드 유입, 절대경로 노출, 에러 발생 상태 등을 검진합니다:
```bash
python scripts/pre_release_check.py
```

---

## 📂 4. 주요 산출물 위치
- **정제된 원본 데이터**: `sample_workspace/03_Clean_Table/`
  - `sales_closing_clean.csv`: 매출 정제 데이터
  - `ar_detail_clean.csv`: 채권 정제 데이터
- **요약 리포트 (Summary)**: `sample_workspace/04_Report_View/`
  - `sales_by_customer.csv`: 월별/거래처별 매출 합계
  - `sales_by_model.csv`: 월별/모델별 매출 합계
  - `sales_by_customer_model.csv`: 월별/거래처/모델 조합 매출
  - `ar_by_customer.csv`: 거래처별 잔액
  - `ar_by_aging_bucket.csv`: 연체 버킷별 채권
  - `sales_invoice_count_by_customer.csv`: 인보이스 거래 건수 count
  - `ar_invoice_count_by_customer.csv`: 채권 발생 건수 count

---

## 📝 5. 로그 확인 및 예외 조치 방법
로그 폴더 `sample_workspace/99_Logs/` 에서 시스템 상태와 진단 결과를 확인합니다:
1. **refresh_log.csv**: 파일 단위 처리 결과(성공 여부 및 로드된 행 수) 기록
2. **validation_log.csv**: 최종 산출물 및 수치 대조 정합성(PASS/FAIL) 기록
3. **error_log.txt**: 오작동 발생 시 내부 절대 경로가 노출되지 않는 형태의 간결한 에러 메시지 기록
