# 배포 버전 설치 테스트 가이드 (DISTRIBUTION_TEST_GUIDE.md)

본 문서는 Finance DataMart Tool을 GitHub 공개 저장소에 업로드한 후, **다른 PC(검증 환경)에서 본 소스코드를 다운로드/클론하여 정상 작동하는지 설치 테스트를 진행하기 위한 단계별 검증 지침서**입니다.

모든 명령어는 Windows PowerShell 환경을 기준으로 기술되었습니다.

---

## 🚫 1. 배포 사양 및 전제 조건
1. **자가 설치 인스톨러 지원**: 본 프로젝트는 AppData 설치를 자동화하는 `FinanceDataMart_Installer.exe`를 지원합니다. 단, 대상 PC에 Python 3.8 이상이 설치되어 있고 `py` 또는 `python` 명령이 PATH에서 실행 가능해야 합니다.
2. **Source-only 배포 병행**: 수동 수정을 희망하는 개발자를 위해 순수 소스코드 형태의 배포도 병행합니다. (Python 3.8 이상 필요)
3. **가상 데이터 모델**: 본 저장소에는 실제 사내 데이터가 포함되어 있지 않습니다. 테스트 구동에 사용되는 데이터와 설정 파일은 `scripts/create_sample_data.py` 스크립트를 통해 로컬에서 가상으로 모조 생성됩니다.
4. **MIT 라이선스**: 본 프로젝트는 `LICENSE` 파일에 기재된 MIT 라이선스 규정을 따릅니다.

---

## 🚀 2. 다른 PC에서의 설치 테스트 및 검증 흐름

### 방법 A: 자가 설치 인스톨러를 이용한 자동 설치 (권장)
1. GitHub Releases 페이지에서 `FinanceDataMart_Installer.exe`를 다운로드합니다.
2. 다운로드한 인스톨러를 더블 클릭하여 실행합니다.
   - 프로그램이 실행되면 자동으로 사용자의 **AppData** 로컬 폴더(`C:\Users\<username>\AppData\Local\FinanceDataMart`)에 배포 자산 36종을 복사합니다.
   - 해당 폴더 내에 `.venv` 가상환경을 구축하고 `pip install` 및 `create_sample_data.py`를 순차 가동합니다.
   - 완료되면 사용자 바탕화면(Desktop)에 `FinanceDataMart` 바로가기 아이콘이 자동 생성됩니다.
3. 바탕화면의 바로가기를 더블 클릭하여 GUI 앱이 정상적으로 뜨는지 교차 검증합니다.

### 방법 B: 수동 소스코드 설치 및 검증 흐름
새로운 PC에서 터미널(PowerShell)을 열고 프로젝트 루트 디렉토리로 이동한 뒤, 아래 8단계 지침을 순차적으로 기동하십시오.

### 1단계: 파이썬 가상환경(`.venv`) 생성
로컬 개발 환경과 타 패키지 간 충돌을 방지하기 위해 격리된 가상환경을 생성합니다.
```powershell
python -m venv .venv
```

### 2단계: 가상환경 활성화
Windows PowerShell의 실행 정책(Execution Policy)을 우회하면서 가상환경을 정상 기동합니다.
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```
*(성공 시 프롬프트 좌측에 `(.venv)` 접두사가 표시됩니다.)*

### 3단계: 외부 의존성(Pandas, OpenPyXL) 라이브러리 설치
`requirements.txt`에 명시된 패키지들을 로컬 가상환경에 설치합니다.
```powershell
pip install -r requirements.txt
```

### 4단계: 가상 샘플 데이터 및 설정 템플릿 복구
깃 트래킹에서 격리된 `sample_workspace` 폴더 트리와 가상 엑셀 데이터(1~2월 Sales_Closing, AR_Detail) 및 정제용 `config.xlsx` 기본 템플릿을 자동으로 재생성합니다.
```powershell
python scripts/create_sample_data.py
```

### 5단계: 데이터마트 정제 및 요약 파이프라인 구동 (CLI 실행)
생성된 가상 엑셀 데이터를 config 매핑 기준에 맞춰 정제하여 Clean Table CSV를 빌드하고, Report View 요약 및 금액 합계 Reconciliation 정합성 대조를 가동합니다.
```powershell
python -m app.main
```

### 6단계: 신규 파일 분석용 컬럼 인벤토리 엑셀 생성
Raw 엑셀 시트들의 스키마 구조를 분석하여 컬럼 목록을 담은 인벤토리 파일을 추출합니다.
```powershell
python scripts/create_column_inventory.py
```

### 7단계: 배포 전 무결성 자가 진단 실행
코드 컴파일, 결과물 실존, 오류 기록, 정합성 성공 등 7개 영역의 무결성을 검증합니다.
```powershell
python scripts/pre_release_check.py
```
*(최종적으로 콘솔에 7개 항목 전체 **[PASS]**가 출력되는지 점검하십시오.)*

### 8단계: 데스크톱 GUI 모듈 로드 가용성 사전 검증
tkinter 기반의 데스크톱 GUI 앱 진입반이 정상적으로 컴파일 및 임포트되는지 파이썬 한 줄 스크립트로 동작성을 진단합니다.
```powershell
python -c "from app.ui_app import DataMartUI; print('UI import ok')"
```
*(화면에 `UI import ok` 문구가 에러 없이 출력되면 GUI 앱 가동 준비가 완료된 것입니다.)*

---

## 📂 3. GitHub 업로드 대상 자산 및 격리(제외) 대상 정의

수동으로 GitHub 리포지토리에 푸시할 때 업로드되는 대상과 로컬 전용 격리 대상은 다음과 같습니다. 사용자는 `.gitignore` 설정에 의해 격리 대상이 유출되지 않도록 유지해야 합니다.

### A. GitHub 업로드 대상 (RELEASE_MANIFEST.md 기준 36종 자산)
- 핵심 소스코드: `app/*.py` (11종), `scripts/*.py` (6종)
- 마스터 문서: `README.md`, `LICENSE`, `requirements.txt`, `.gitignore`
- 상세 안내서: `USER_GUIDE.md`, `KNOWN_LIMITATIONS.md`, `MAINTENANCE.md`, `RELEASE_NOTES.md`, `THIRD_PARTY_NOTICES.md`
- 배포/검증 지침서: `GITHUB_RELEASE_GUIDE.md`, `PUBLIC_RELEASE_CHECKLIST.md`, `RELEASE_MANIFEST.md`, `OFFICIAL_RELEASE_HANDOFF.md`, `POST_RELEASE_CHECKLIST.md`, `LICENSE_DECISION_GUIDE.md`, `DISTRIBUTION_TEST_GUIDE.md` (본 문서)
- GitHub Release 첨부 파일: `dist/FinanceDataMart_Installer.exe`는 저장소 커밋 대상이 아니라 Release asset으로만 업로드합니다.

### B. 로컬 격리 및 제외 대상 (GitHub 업로드 절대 금지)
- 파이썬 가상환경: `.venv/`, `venv/`, `env/` 등
- 컴파일 캐시: `__pycache__/`, `*.pyc`, `*.pyo`
- 로컬 테스트 작업공간 전체: `sample_workspace/`
  - `01_Input_Raw/`의 가상 Raw Excel 파일
  - `90_Config/config.xlsx`
  - `03_Clean_Table/`, `04_Report_View/`의 CSV 결과물
  - `90_Config/column_inventory.xlsx`
  - `99_Logs/`의 실행 로그
- IDE 로컬 설정: `.vscode/`, `.idea/`, `.gemini/`
- PyInstaller 로컬 빌드 산출물: `build/`, `dist/`, `*.spec` (단, `dist/FinanceDataMart_Installer.exe`는 GitHub Release asset으로 별도 첨부 가능)

`sample_workspace/`는 `python scripts/create_sample_data.py` 실행 시 다른 PC에서 다시 생성되는 폴더이므로 배포 저장소에는 포함하지 않습니다.
