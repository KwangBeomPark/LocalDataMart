# myAGENT.MD

> 이 파일은 현재 로컬 프로젝트 전용 AI 개발 지침이다.  
> Codex, Antigravity, Copilot, 기타 AI 코딩 도구는 작업 전에 반드시 이 파일과 `AI_CODE_MAP.MD`, `PROJECT_ROADMAP.MD`를 먼저 읽는다.

---

## 1. 프로젝트 정체성

프로젝트명: **Finance DataMart Tool**

이 프로젝트는 여러 개의 Excel Raw Data 파일을 폴더 단위로 관리하고, 사용자가 정의한 Config 기준에 따라 필요한 컬럼만 선택·정제·통합한 뒤, Excel 리포트에서 바로 사용할 수 있는 Clean Table과 Report View를 생성하는 로컬 데이터마트 도구이다.

초기 사용 목적은 재무·회계·영업관리·채권관리·기획 업무 자동화이지만, 특정 회사나 특정 ERP에 종속되지 않는 범용 프로그램으로 개발한다.

이 프로젝트는 다음 성격을 가진다.

- Local Excel DataMart Builder
- Folder-based Excel Consolidation Tool
- Config-driven Report View Generator
- Lightweight Data Preparation Tool for Excel Users

---

## 2. 가장 중요한 개발 원칙

이 프로젝트는 처음부터 완성형 앱으로 만들지 않는다.

현재 목표는 **작게 작동하는 MVP**를 만드는 것이다.

AI는 다음 원칙을 반드시 따른다.

1. 작은 단위로 구현한다.
2. 한 번에 많은 기능을 추가하지 않는다.
3. 현재 단계에서 필요 없는 복잡한 GUI, DuckDB, Parquet, exe 패키징은 만들지 않는다.
4. 먼저 `Sales_Closing` 샘플 데이터 하나로 전체 흐름을 검증한다.
5. 동작하는 MVP가 완성되기 전까지 구조를 과도하게 확장하지 않는다.
6. 사용자는 Python 코드를 수정하지 않고 Excel Config만 수정하는 방향으로 설계한다.
7. Raw Data는 절대 수정하지 않는다.
8. 실제 회사명, 거래처명, 금액, 내부 경로, 실제 업무 데이터는 저장소에 넣지 않는다.
9. GitHub 공개 가능성을 항상 고려한다.
10. 변경 후에는 관련 문서를 업데이트한다.

---

## 3. 현재 단계

현재 단계는 **Phase 20 배포 버전 GitHub 업로드 및 다른 PC 설치 테스트 준비 완료 단계**이다.

현재 집중 범위는 다음과 같다.

```text
Phase 0~1: 프로젝트 초기화 및 Sales_Closing MVP 구현
Phase 2~19: Config 검증, Column Inventory, 다중 data_group, Report View, Reconciliation, 최소 Desktop UI, 배포 전 무결성 점검, Source-only Release Candidate 문서 정리, GITHUB 수동 업로드 가이드, 유지보수 지침(MAINTENANCE.md), 공식 배포 매니페스트(RELEASE_MANIFEST.md), 최종 공식 배포 핸드오프 지침(OFFICIAL_RELEASE_HANDOFF.md), 사후 점검 체크리스트(POST_RELEASE_CHECKLIST.md), 라이선스 결정 가이드(LICENSE_DECISION_GUIDE.md) 구성 및 MIT License 공식 적용 완료
Phase 20: 타 PC에서 소스코드를 받아 가상환경 구축, 의존성 설치, 데이터마트 가동, 컬럼 인벤토리 추출, 무결성 자가 진단, GUI 가용성 사전 검증까지 전 과정을 검증할 수 있도록 배포 가이드라인(DISTRIBUTION_TEST_GUIDE.md) 신설 및 33종 자산 명세 정비 완료
```

현재 만들 대상은 아래 흐름이다.

```text
Raw Excel files
    ↓
config.xlsx
    ↓
Column_Mapping
    ↓
sales_closing_clean.csv
    ↓
Report_View
    ↓
sales_by_customer.csv
sales_by_model.csv
sales_by_customer_model.csv
```

현재 단계에서 하지 말아야 할 것:

```text
복잡한 GUI 개발
DuckDB 적용
Parquet 적용
다중 데이터 그룹 전체 구현
복잡한 Validation Engine
실제 회사 데이터 연결
exe 패키징
Power BI 연동
ODBC 연결
```

---

## 4. AI 작업 시작 규칙

AI는 새 작업을 시작할 때 반드시 다음 순서를 따른다.

1. `myAGENT.MD`를 읽는다.
2. `AI_CODE_MAP.MD`를 읽는다.
3. `PROJECT_ROADMAP.MD`를 읽는다.
4. 현재 프로젝트 폴더 구조를 확인한다.
5. 현재 단계가 무엇인지 확인한다.
6. 가장 작은 안전한 다음 작업을 정한다.
7. 필요한 파일만 수정한다.
8. 수정 후 실행 가능한 테스트 또는 확인 방법을 제시한다.
9. 구조나 파일 역할이 바뀌면 `AI_CODE_MAP.MD`를 업데이트한다.
10. 단계나 우선순위가 바뀌면 `PROJECT_ROADMAP.MD`를 업데이트한다.

AI는 사용자의 명시적 요청 없이 프로젝트 전체를 새로 설계하거나 대규모 리팩터링하지 않는다.

---

## 5. 코드 언어와 문서 언어

코드, 함수명, 변수명, 클래스명, 폴더명, 테이블명은 영문을 사용한다.

예:

```text
config_loader.py
file_scanner.py
excel_reader.py
transformer.py
report_generator.py
sales_closing_clean.csv
sales_by_customer.csv
```

문서, 개발 지침, 코드맵, 로드맵은 한국어로 작성한다.

예:

```text
myAGENT.MD
AI_CODE_MAP.MD
PROJECT_ROADMAP.MD
```

README는 초기에는 한국어로 작성하고, GitHub 공개 단계에서 영어 README를 추가할 수 있다.

---

## 6. 민감정보 및 공개 가능성 원칙

이 프로젝트는 회사 업무에서 사용할 수 있지만, GitHub 공개 가능성을 고려해야 한다.

저장소에는 절대 다음 정보를 포함하지 않는다.

- 실제 회사명
- 실제 거래처명
- 실제 공급업체명
- 실제 직원명
- 실제 제품명
- 실제 매출, 채권, 수익성, 세금 관련 금액
- 내부 네트워크 드라이브 경로
- 내부 ERP 화면명 또는 내부 시스템 세부 구조
- 실제 보고서 양식
- 실제 계약조건
- 실제 세무·회계 판단 자료

샘플 데이터는 반드시 가상 데이터로 만든다.

예시 명칭:

```text
Customer A
Customer B
Model X100
Product Group A
Sales Region 1
```

---

## 7. Raw Data 처리 원칙

Raw Data는 원본 파일 그대로 보존한다.

프로그램은 Raw Data를 읽기만 한다.

금지:

```text
Raw Excel 파일 직접 수정
Raw Excel 파일에 시트 추가
Raw Excel 파일명 자동 변경
Raw Excel 파일 내부 값 수정
```

허용:

```text
Raw 파일 읽기
필요 컬럼만 선택
Clean Table 생성
Report View 생성
로그 생성
```

Raw Data는 많고 복잡할 수 있으므로, 기본 원칙은 다음이다.

```text
Config에 등록된 컬럼만 사용한다.
등록되지 않은 Raw 컬럼은 기본적으로 무시한다.
```

---

## 8. Config 중심 설계 원칙

사용자는 Python 코드를 수정하지 않아야 한다.

다음 항목은 Config에서 관리되어야 한다.

- 데이터 그룹명
- Raw 폴더 경로
- 파일 패턴
- Sheet 이름
- Header row
- 유지할 Raw 컬럼
- 표준 컬럼명
- 데이터 타입
- 필수 여부
- 컬럼 역할
- 집계 방식
- Report View의 group_by
- Report View의 measures
- Output 파일명

초기 Config 파일명:

```text
config.xlsx
```

초기 필수 Sheet:

```text
Source_Config
Column_Mapping
Report_View
```

향후 추가 가능 Sheet:

```text
Field_Dictionary
Validation_Rule
App_Settings
```

하지만 MVP에서는 필수 Sheet 3개만 우선 구현한다.

---

## 9. Column Mapping 원칙

Raw 파일은 컬럼이 매우 많을 수 있다.

따라서 모든 컬럼을 Config에 기록하지 않는다.

기본 방식:

```text
Raw 컬럼 100개
→ 필요한 컬럼 10~20개만 Column_Mapping에 등록
→ 나머지는 자동 Ignore
```

Column_Mapping은 열 번호가 아니라 컬럼명 기준으로 처리한다.

비추천:

```text
A열 = invoice_no
B열 = customer_code
C열 = net_sales
```

추천:

```text
raw_column = Invoice No
standard_column = invoice_no
```

예외적으로 헤더가 없는 고정 양식 파일만 열 번호 방식을 검토할 수 있다.

---

## 10. 컬럼 역할 정의

컬럼의 역할은 다음 기준을 따른다.

| role | 의미 |
|---|---|
| key | 중복 판단 또는 고유 식별에 사용 |
| dimension | 리포트 그룹핑, 필터 기준 |
| date | 날짜 컬럼 |
| date_group | 월, 분기 등 파생 기간 컬럼 |
| measure | 합계, 평균, 건수 등 집계 대상 숫자 |
| audit | source_file, loaded_at 등 추적용 컬럼 |

집계는 `measure` 컬럼만 대상으로 한다.

`dimension`은 group_by 기준으로 사용한다.

`audit`은 Clean Table에는 남길 수 있지만, Summary Report에는 기본적으로 포함하지 않는다.

---

## 11. Report View 설계 원칙

Report View는 Clean Table 기준으로 생성한다.

Raw 파일을 직접 읽어 Summary를 만들지 않는다.

하나의 Clean Table에서 여러 Report View를 만들 수 있어야 한다.

예:

```text
sales_closing_clean.csv
    ↓
sales_by_customer.csv
sales_by_model.csv
sales_by_customer_model.csv
```

Report_View Config에는 다음 항목을 둔다.

```text
active
view_name
source_table
group_by
measures
filter
output_file
```

예:

```text
view_name: sales_by_customer
source_table: sales_closing_clean
group_by: posting_month, customer_code
measures: net_sales:sum, qty:sum
output_file: sales_by_customer.csv
```

---

## 12. MVP Output 원칙

초기 출력은 CSV 중심으로 한다.

초기 Output:

```text
sales_closing_clean.csv
sales_by_customer.csv
sales_by_model.csv
sales_by_customer_model.csv
refresh_log.csv
validation_log.csv
```

CSV 파일은 Excel에서 바로 열 수 있어야 한다.

필요하면 UTF-8 BOM을 적용한다.

초기에는 복잡한 서식이 있는 Excel output을 만들지 않는다.

---

## 13. 로그 원칙

모든 실행은 로그를 남긴다.

최소 로그:

```text
refresh_log.csv
validation_log.csv
error_log.txt
```

로그에는 다음을 포함할 수 있다.

```text
run_id
run_datetime
data_group
source_file
status
row_count
output_file
message
```

로그에는 실제 민감한 line-level data를 기록하지 않는다.

---

## 14. Validation 원칙

초기 Validation은 단순하게 시작한다.

MVP 필수 검증:

1. Config 파일 존재 여부
2. Source_Config Sheet 존재 여부
3. Column_Mapping Sheet 존재 여부
4. Report_View Sheet 존재 여부
5. Raw 폴더 존재 여부
6. 필수 컬럼 존재 여부
7. Clean Table 생성 여부
8. Report View 생성 여부

향후 검증:

```text
Raw row count vs Clean row count
금액 합계 검증
중복 key 검증
날짜 형식 검증
숫자 형식 검증
신규 컬럼 탐지
Config 오류 검증
```

---

## 15. 코드 작성 원칙

Python 코드는 읽기 쉽게 작성한다.

필수 원칙:

- `pathlib` 사용
- 함수는 작게 작성
- 한 파일에 모든 로직을 넣지 않음
- Config loading, scanning, reading, transformation, reporting, logging 분리
- 하드코딩 경로 금지
- 실제 회사 경로 금지
- 타입 힌트 사용 권장
- 비즈니스 로직에는 짧은 주석 작성
- 복잡한 추상화보다 명확한 함수 우선

---

## 16. 권장 모듈 구조

초기 권장 구조:

```text
app/
├─ main.py
├─ config_loader.py
├─ file_scanner.py
├─ excel_reader.py
├─ transformer.py
├─ report_generator.py
├─ validator.py
├─ logger_setup.py
└─ models.py
```

각 모듈의 역할은 `AI_CODE_MAP.MD`에 따른다.

---

## 17. 테스트 원칙

실제 회사 데이터로 테스트하지 않는다.

테스트는 `sample_workspace` 또는 `tests/sample_data`의 가상 데이터로 한다.

MVP 테스트 기준:

```text
1. 샘플 Raw Excel 2~3개 생성
2. config.xlsx 생성
3. 프로그램 실행
4. sales_closing_clean.csv 생성 확인
5. sales_by_customer.csv 생성 확인
6. sales_by_model.csv 생성 확인
7. sales_by_customer_model.csv 생성 확인
8. 로그 생성 확인
```

---

## 18. AI가 절대 하지 말아야 할 것

AI는 다음 작업을 임의로 하지 않는다.

```text
프로젝트 전체 구조 재작성
GUI부터 구현
DuckDB부터 적용
Parquet부터 적용
실제 회사 데이터 샘플 생성
회사명 또는 실제 거래처명 삽입
Config 구조를 불필요하게 복잡하게 확장
사용자 확인 없이 파일명 대량 변경
기능 하나를 위해 과도한 프레임워크 도입
Raw 파일 수정
```

---

## 19. AI가 변경 후 반드시 해야 할 것

다음 경우에는 문서를 업데이트한다.

| 상황 | 업데이트 대상 |
|---|---|
| 모듈 추가/삭제 | AI_CODE_MAP.MD |
| 폴더 구조 변경 | AI_CODE_MAP.MD |
| Config Sheet 구조 변경 | AI_CODE_MAP.MD, PROJECT_ROADMAP.MD |
| 개발 단계 변경 | PROJECT_ROADMAP.MD |
| 주요 원칙 변경 | myAGENT.MD |
| 기능 완료 | PROJECT_ROADMAP.MD |

---

## 20. 현재 작업 초점

현재 AI가 집중해야 하는 것은 다음이다.

```text
Phase 20:
- 타 PC 검증을 위한 설치 테스트 지침서(DISTRIBUTION_TEST_GUIDE.md) 신설 및 33종 파일 매니페스트 정합성 조율
- 가상환경 활성화 정책 및 GUI 임포트 가용성 검증 파트를 PowerShell 기준으로 수립
```

현재 단계의 성공 기준:

```text
다른 PC 환경에서 본 저장소를 다운로드/클론한 후 의존성 설치부터 데이터마트 기동 및 UI 임포트 사전 검증까지의 수동 흐름이 DISTRIBUTION_TEST_GUIDE.md에 완비되고, pre_release_check.py가 100% [PASS]를 출력하여 저장소가 공식 테스트 릴리즈 대기 상태임을 검증한다.
```
