# PROJECT_ROADMAP.MD

> 이 문서는 Finance DataMart Tool의 단계별 개발 로드맵이다.  
> 목적은 프로젝트가 처음부터 복잡해지지 않도록 현재 단계의 초점을 명확히 하고, 향후 확장 방향을 관리하는 것이다.

---

## 1. 프로젝트 방향

Finance DataMart Tool은 여러 Excel Raw Data 파일을 폴더에 저장하고, 사용자가 정의한 Config 기준으로 필요한 컬럼만 정리한 뒤, Excel에서 바로 사용할 수 있는 Clean Table과 Report View를 생성하는 로컬 데이터마트 도구이다.

초기에는 재무·회계·영업관리·채권관리·기획 업무를 염두에 두지만, 특정 회사 전용 도구가 아니라 GitHub에 공개해도 문제 없는 범용 프로그램으로 개발한다.

핵심 방향:

```text
Raw Excel files
    ↓
Config.xlsx
    ↓
Clean Table
    ↓
Report View
    ↓
Excel Pivot / Report / Dashboard
```

---

## 2. 제품 컨셉

이 도구는 다음과 같은 문제를 해결한다.

```text
월별 Raw Excel 파일이 많다.
Raw 파일의 컬럼이 너무 많다.
실제 리포트에는 일부 컬럼만 필요하다.
Power Query에서 매번 처리하면 느리고 복잡하다.
팀원들이 같은 기준으로 데이터를 정리하기 어렵다.
같은 데이터로 여러 형태의 Summary가 필요하다.
```

이 도구의 역할:

```text
Raw 파일은 그대로 보존한다.
필요 컬럼만 선택한다.
표준 컬럼명으로 바꾼다.
Clean Table을 만든다.
Report View를 여러 개 만든다.
Excel은 최종 Output만 읽는다.
```

---

## 3. 공개 가능한 범용 앱 원칙

처음부터 GitHub 공개 가능성을 고려한다.

저장소에 포함하지 않을 것:

```text
실제 회사명
실제 거래처명
실제 공급업체명
실제 제품명
실제 금액
내부 네트워크 경로
내부 ERP 구조
내부 보고서 양식
회사 고유 업무 규칙
```

사용할 표현:

```text
Sales_Closing
AR_Detail
Profitability
Inventory
VAT_Check
Customer
Product
Model
Amount
Quantity
```

코드는 영문으로 작성한다.

문서와 지침은 한국어로 작성한다.

---

## 4. 전체 개발 원칙

이 프로젝트는 점진적으로 개발한다.

가장 중요한 원칙:

```text
먼저 작게 작동하게 만든다.
그 다음 Config를 안정화한다.
그 다음 여러 Report View를 만든다.
그 다음 데이터 그룹을 늘린다.
마지막에 GUI와 성능 개선을 한다.
```

하지 말아야 할 접근:

```text
처음부터 완성형 GUI 만들기
처음부터 DuckDB/Parquet 넣기
처음부터 모든 데이터 그룹 구현하기
처음부터 복잡한 Validation Engine 만들기
처음부터 회사 실제 데이터 연결하기
```

---

## 5. 현재 단계

현재 상태:

```text
Status: Phase 20 Completed / Phase 21 Setup
Current Focus: Phase 20 -> Phase 21

현재 집중할 일:

1. Phase 20 (배포 버전 GitHub 업로드 및 다른 PC 설치 테스트 준비) 완료
   - 다른 PC에서의 수동 설치 테스트 및 검증 지침서(DISTRIBUTION_TEST_GUIDE.md) 신설 및 33종 자산 매니페스트 동기화 완료
2. Phase 21 (타 PC 설치 테스트 피드백 반영 및 다음 기능 개발 범위 논의) 준비
```

현재 성공 기준:

```text
샘플 Raw Excel 파일 여러 개를 폴더에 넣고 프로그램을 실행하면,
config.xlsx 기준으로 필요한 컬럼만 남긴 sales_closing_clean.csv와
3개의 Summary CSV가 생성된다.
```

---

## 6. Phase 0 - 프로젝트 초기화

## 목표

AI 코딩 도구가 프로젝트 방향을 잃지 않도록 기본 문서, 폴더 구조, 실행 기반을 만든다.

## 작업 항목

```text
■ myAGENT.MD 작성
■ AI_CODE_MAP.MD 작성
■ PROJECT_ROADMAP.MD 작성
■ README.md 초안 작성
■ requirements.txt 작성
■ .gitignore 작성
■ app/ 폴더 생성
■ sample_workspace/ 폴더 생성
■ templates/ 폴더 생성
■ tests/ 폴더 생성
```

## 산출물

```text
myAGENT.MD
AI_CODE_MAP.MD
PROJECT_ROADMAP.MD
README.md
requirements.txt
.gitignore
app/
templates/
sample_workspace/
tests/
```

## 완료 기준

```text
프로젝트 루트 구조가 준비되어 있다.
AI 지침 문서가 존재한다.
실제 회사 데이터가 포함되어 있지 않다.
Codex 또는 다른 AI가 현재 목표를 이해할 수 있다.
```

---

## 7. Phase 1 - Sales_Closing MVP

## 목표

하나의 데이터 그룹만 대상으로 전체 흐름을 작동시킨다.

대상 데이터 그룹:

```text
Sales_Closing
```

## 입력

```text
sample_workspace/01_Input_Raw/Sales_Closing/
```

월별 Excel 파일 예시:

```text
Sales_Closing_2026_01.xlsx
Sales_Closing_2026_02.xlsx
Sales_Closing_2026_03.xlsx
```

## Config

```text
sample_workspace/90_Config/config.xlsx
```

필수 Sheet:

```text
Source_Config
Column_Mapping
Report_View
```

## 출력

```text
sample_workspace/03_Clean_Table/sales_closing_clean.csv
sample_workspace/04_Report_View/sales_by_customer.csv
sample_workspace/04_Report_View/sales_by_model.csv
sample_workspace/04_Report_View/sales_by_customer_model.csv
sample_workspace/99_Logs/refresh_log.csv
sample_workspace/99_Logs/validation_log.csv
```

## 주요 기능

```text
■ Source_Config 읽기
■ Column_Mapping 읽기
■ Report_View 읽기
■ Sales_Closing 폴더 스캔
■ Excel 파일 여러 개 읽기
■ keep = Y 컬럼만 선택
■ standard_column으로 컬럼명 변경
■ 필수 컬럼 검증
■ source_file, loaded_at 추가
■ posting_month 생성
■ sales_closing_clean.csv 생성
■ Report_View 기준 Summary 생성
■ 로그 생성
```

## 완료 기준

```text
Raw Excel 여러 개가 하나의 Clean CSV로 통합된다.
필요 컬럼만 남는다.
표준 컬럼명이 적용된다.
거래선별 Summary가 생성된다.
모델별 Summary가 생성된다.
거래선+모델별 Summary가 생성된다.
로그가 생성된다.
```

---

## 8. Phase 2 - Config 사용성 개선

## 목표

사용자가 Python 코드를 수정하지 않고 Config만으로 데이터 처리 기준을 조정할 수 있게 한다.

## 작업 항목

```text
□ config_template.xlsx 생성
□ Source_Config 예시 정리
□ Column_Mapping 예시 정리
□ Report_View 예시 정리
□ role 값 표준화
□ aggregation 값 표준화
■ Config 오류 메시지 개선 (Y/N 플래그 검증 및 에러 정보 상세화 완료)
□ Config 설명 문서 작성
```

## 개선 방향

Config는 사용자가 보는 핵심 UI 역할을 한다.

따라서 다음을 고려한다.

```text
드롭다운 값
필수 입력 컬럼 표시
예시 행 제공
설명 컬럼 제공
잘못된 값에 대한 경고
```

## 완료 기준

```text
사용자가 config.xlsx만 수정해서
컬럼 선택과 리포트 구조를 바꿀 수 있다.
```

---

## 9. Phase 3 - Column Inventory 기능

## 목표

Raw 파일 컬럼이 많을 때 사용자가 필요한 컬럼을 쉽게 찾을 수 있도록 한다.

## 기능

```text
■ Raw 파일 샘플 스캔
■ 컬럼 목록 추출
■ 샘플 값 추출
■ 데이터 타입 추정
■ 빈값 비율 계산
■ 추천 role 생성
■ column_inventory.xlsx 생성
```

## Output

```text
sample_workspace/90_Config/column_inventory.xlsx
```

## 완료 기준

```text
사용자가 Raw 파일의 전체 컬럼을 쉽게 검토하고,
필요한 컬럼만 Column_Mapping에 반영할 수 있다.
```

---

## 10. Phase 4 - 다중 데이터 그룹 지원

## 목표

Sales_Closing 외 다른 데이터 그룹도 같은 엔진으로 처리할 수 있게 한다.

## 후보 데이터 그룹

```text
AR_Detail
Profitability
Inventory
VAT_Check
Claims
```

## 원칙

```text
새 데이터 그룹을 추가할 때 Python 코드를 크게 수정하지 않는다.
Source_Config와 Column_Mapping 추가로 처리 가능해야 한다.
Report_View 추가로 Output을 만들 수 있어야 한다.
```

## 완료 기준

```text
최소 2개 이상의 data_group이 같은 엔진으로 처리된다.
Sales_Closing 전용 하드코딩이 제거된다.
```

---

## 11. Phase 5 - Report View Engine 고도화

## 목표

같은 Clean Table에서 여러 리포트를 자유롭게 생성한다.

## 지원할 Summary 예시

```text
sales_by_customer
sales_by_model
sales_by_customer_model
sales_by_channel
sales_by_product_group
sales_by_month_customer_model
```

## 지원할 집계 방식

초기:

```text
sum
count
```

향후:

```text
average
count_distinct
min
max
weighted_avg
```

## 완료 기준

```text
Report_View에 한 줄을 추가하면 새로운 Summary CSV가 생성된다.
```

---

## 12. Phase 6 - Validation 및 Reconciliation 강화

## 목표

생성된 데이터의 신뢰성을 높인다.

## 검증 항목

```text
필수 컬럼 누락
Raw row count vs Clean row count
금액 합계 비교
중복 key 확인
날짜 형식 오류
숫자 형식 오류
신규 컬럼 발견
Config 누락 또는 오타
```

## 완료 기준

```text
사용자가 처리 성공/실패와 경고 사항을 쉽게 이해할 수 있다.
```

---

## 13. Phase 7 - 성능 개선

## 목표

데이터가 많아져도 빠르게 작동하게 한다.

## 개선 후보

```text
필요 컬럼만 읽기 최적화
이미 처리한 파일 재처리 방지
file_registry 도입
CSV → Parquet 전환 검토
pandas groupby → DuckDB SQL 검토
로컬 temp 처리 후 네트워크 드라이브 결과 저장
```

## 주의

DuckDB와 Parquet는 강력하지만, MVP가 안정된 이후에 적용한다.

## 완료 기준

```text
대량 파일 처리 시간이 실무적으로 허용 가능한 수준이다.
```

---

## 14. Phase 8 - Desktop UI

## 목표

비개발자 팀원이 쉽게 실행할 수 있는 데스크탑 앱 형태로 발전시킨다.

## 초기 UI 후보

```text
[Scan Columns]
[Open Config]
[Refresh DataMart]
[Generate Reports]
[Open Output Folder]
[Open Log Folder]
```

## 구현 후보

```text
tkinter
PySide6
```

## 주의

GUI는 내부 엔진이 안정된 후 추가한다.

## 완료 기준

```text
사용자가 명령어를 몰라도 프로그램을 실행할 수 있다.
```

---

## 15. Phase 9 - 안정성 극대화 및 배포 전 준비

## 목표

배포나 공개 준비 전에 현재 산출물, 로그, 금지 기술 유입, 내부 경로 노출 여부를 단순한 스크립트로 점검한다.

## 작업 항목

```text
■ scripts/pre_release_check.py 작성
■ 필수 산출물 존재 여부 확인
■ validation_log.csv FAIL 여부 확인
■ error_log.txt 무오류 상태 확인
■ 금지 기술 키워드 유입 여부 확인
■ 로그 내 내부 절대경로 및 상세 콜스택 노출 여부 확인
■ Raw Excel 파일 읽기 가능 여부 확인
■ tkinter UI의 Run Pre-release Check 버튼 연동
```

## 완료 기준

```text
python scripts/pre_release_check.py 실행 시 현재 Phase 0~8 산출물과 로그 상태를 PASS/FAIL로 확인할 수 있다.
exe 패키징, 설치 프로그램, GitHub Actions 구성은 포함하지 않는다.
```

---

## 16. Phase 10 - GitHub 공개 준비

## 목표

일반 사용자도 이해할 수 있는 공개 프로젝트로 정리한다.

## 작업 항목

```text
□ 공개용 README 정리
□ 샘플 데이터 가상화 확인
□ 회사 정보 제거 확인
□ 내부 경로 제거 확인
□ 설치 방법 작성
□ 사용 방법 작성
□ FAQ 작성
□ Known Limitations 작성
□ 스크린샷 또는 GIF 준비
```

## 공개 전 점검

```text
□ 실제 회사명 없음
□ 실제 거래처명 없음
□ 실제 제품명 없음
□ 실제 금액 없음
□ 내부 네트워크 경로 없음
□ 내부 보고서 양식 없음
□ 실제 업무 데이터 없음
```

---

## 17. 현재 당장 하지 않을 것

현재 단계에서는 다음을 하지 않는다.

```text
GUI
DuckDB
Parquet
ODBC
Power BI 연동
클라우드 서버
SharePoint 연동
복잡한 인증 체계
사용자 권한 관리
회사 실제 데이터 기반 샘플
```

이 항목들은 프로젝트가 안정된 후 별도 Phase에서 검토한다.

---

## 18. 현재 단계의 개발 체크리스트

Codex 또는 AI 코딩 도구가 가장 먼저 수행할 체크리스트:

```text
□ 프로젝트 폴더 구조 생성
□ requirements.txt 작성
□ app/__init__.py 생성
□ app/main.py 생성
□ app/config_loader.py 생성
□ app/file_scanner.py 생성
□ app/excel_reader.py 생성
□ app/transformer.py 생성
□ app/report_generator.py 생성
□ app/validator.py 생성
□ app/logger_setup.py 생성
□ sample_workspace 구조 생성
□ config_template.xlsx 생성
□ 샘플 Sales_Closing Excel 파일 생성
□ Phase 1 workflow 구현
□ 샘플 실행 결과 확인
```

---

## 19. 장기 비전

장기적으로 이 프로젝트는 다음과 같은 범용 앱이 될 수 있다.

```text
Local DataMart Builder
Excel Reporting Companion
Config-driven Data Preparation Tool
Lightweight BI Preparation Layer
Folder-based Report Automation Tool
```

그러나 장기 비전 때문에 현재 단계가 복잡해져서는 안 된다.

현재 단계의 핵심은 단 하나다.

```text
Sales_Closing 샘플 데이터를 Config 기반으로 읽고,
Clean CSV와 Summary CSV를 안정적으로 생성한다.
```

---

## 20. 로드맵 관리 원칙

이 문서는 프로젝트 진행에 따라 업데이트한다.

업데이트 기준:

```text
Phase 완료
Phase 범위 변경
새 기능 추가 결정
현재 단계 변경
보류 기능 추가
GitHub 공개 방향 변경
```

항상 현재 단계가 무엇인지 명확히 적고, AI가 미래 기능을 현재 단계에 섞어 넣지 않도록 관리한다.
