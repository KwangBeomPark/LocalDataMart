# 릴리즈 노트: v1.0.0-RC1 (RELEASE_NOTES.md)

본 문서는 Finance DataMart Tool의 첫 번째 릴리즈 후보 버전인 **v1.0.0-RC1 (Release Candidate 1)**에 관한 사양서입니다.

---

## 📦 1. 배포 형태 및 기본 규칙
- **독립 실행형 Setup 및 소스 배포**: 본 릴리즈 버전은 대상 PC에 파이썬이 없어도 더블 클릭만으로 AppData(`%LOCALAPPDATA%\FinanceDataMart`)에 배포되는 독립 실행형 설치 파일 `FinanceDataMart_Setup.exe`를 공식 지원합니다. 또한, 개발자를 위한 순수 소스코드 배포 형태도 지원합니다.
- **가상 데이터 기반**: 테스트 및 동작 검증을 위해 `sample_workspace` 폴더 내에 생성되는 데이터들은 100% 임의 모조된 가상 데이터입니다. (독립 실행형 Setup 실행 시에도 자동으로 설치 폴더에 내장된 샘플이 복원됩니다.)
- **공식 라이선스**: 본 배포판은 MIT License로 공개되며, 라이선스 전문은 프로젝트 루트의 `LICENSE` 파일에 포함되어 있습니다.

---

## 🚀 2. Release Candidate 최종 검증 절차
배포 가용성(Release Candidate) 판정을 확보하기 위해 반드시 다음 5단계 확인 절차를 순차적으로 실행하여 예외가 없음을 입증해야 합니다.

```bash
# 1단계: 가상 샘플 데이터 복원
python scripts/create_sample_data.py

# 2단계: 데이터마트 정제 및 요약 파이프라인 기동
python -m app.main

# 3단계: 컬럼 인벤토리 분석 파일 빌드
python scripts/create_column_inventory.py

# 4단계: 배포 전 무결성 자가 진단 가동 (★ 최종 가용성 판정 지표)
python scripts/pre_release_check.py

# 5단계: 데스크톱 GUI 제어 패널 실행 (수동 기동 및 종료 확인)
python scripts/run_desktop_app.py
```
- **합격 요건**: 4단계 무결성 검증(`pre_release_check.py`) 가동 결과 콘솔에 7개 진단 항목이 모두 **[PASS]**로 떨어지고 프로세스가 종료 코드 `0`으로 완료되어야 배포 후보 요건을 충족합니다.

---

## 📂 3. 주요 산출물 및 로그 위치
- **정제 산출물**: `sample_workspace/03_Clean_Table/` (정제 완료 CSV 2종)
- **요약 리포트**: `sample_workspace/04_Report_View/` (요약 뷰 CSV 7종)
- **진단 및 로그**: `sample_workspace/99_Logs/`
  - `validation_log.csv`: 대조 및 정합성 검사(PASS/FAIL) 내역
  - `refresh_log.csv`: 로딩된 파일 목록 및 행 수
  - `error_log.txt`: 비정상 에러 발생 이력 (시스템 로컬 절대경로 및 전체 스택 트레이스 배제)

---

## 📖 4. 유관 문서 바로가기 링크
- [사용자 가이드 (USER_GUIDE.md)](USER_GUIDE.md)
- [기술적 제약 사항 (KNOWN_LIMITATIONS.md)](KNOWN_LIMITATIONS.md)
- [공개 전 체크리스트 (PUBLIC_RELEASE_CHECKLIST.md)](PUBLIC_RELEASE_CHECKLIST.md)
- [제3자 소프트웨어 고지서 (THIRD_PARTY_NOTICES.md)](THIRD_PARTY_NOTICES.md)
- [유지보수 및 이슈 대응 가이드 (MAINTENANCE.md)](MAINTENANCE.md)

---

## 📝 5. 후속 변경 이력 (Changelog) 기록 방식
- 향후 버그 수정 및 패치 버전(v1.0.1 등) 릴리즈 시, 본 파일 하단에 변경 내역 요약과 수정된 모듈 명세를 추가 기입하여 변경 이력(Changelog)을 유지 보존하십시오.

---

## 📝 v1.0.0-RC2 (2026-06-30) - Phase 23 완료 배포판
- **PowerShell 바로가기 경로 안정성 개선**: 사용자 Windows 계정명에 공백이나 홑따옴표가 들어 있는 경우 바탕화면 바로가기 생성이 실패하던 버그를 홑따옴표 이스케이프 및 `-NoProfile -ExecutionPolicy Bypass` 추가로 완전 해결.
- **AppData 설치 도중 리소스 잠금(PermissionError) 대응**: 설치 타겟 경로의 파일이나 엑셀 템플릿이 켜져 있을 때 발생하는 `PermissionError`를 명확한 안내 팝업과 함께 대기(`input()`)하도록 개선.
- **GUI 기동 크래시 및 오류 팝업 정밀화**:
  - `--noconsole`로 기동 실패 시 아무 팝업 없이 꺼지던 것을 native dialog fallback으로 래핑.
  - GUI 내부 갱신 도중 `SystemExit` 에러 발생 시 단순 코드 반환 대신 `error_log.txt`를 역파싱하여 구체적인 에러 메시지를 다이얼로그로 출력.
  - 다이얼로그 및 오류 화면 내에 로컬 개발 PC의 절대경로나 `traceback` 스택 트레이스 정보가 일체 유출되지 않도록 `sanitize_message()` 적용 강화.
- **외부 PC 설치 검증 보고서 신설**: Python 미설치 환경의 오프라인 Windows 11 PC에서 3대 핵심 GUI 기능 및 pre-release 자가 진단 패스 결과를 수집한 [PHASE23_EXTERNAL_TEST_REPORT.md](PHASE23_EXTERNAL_TEST_REPORT.md) 추가.

---

## 📝 v1.0.0-RC3 (2026-07-01) - Phase 24 완료 배포판 (Actions 검증 PASS)
- **GitHub Actions CI 도입**: 원격 저장소 푸시 및 PR 시 코드 컴파일, 샘플 가상 데이터 생성, 메인 파이프라인 구동, 컬럼 인벤토리 분석, pre-release 무결성 진단을 자동으로 수행하는 `Finance DataMart CI` 연동 (.github/workflows/ci.yml 추가).
- **배포 위생 자동 검사(Release Hygiene Check)**: Git tracked 목록을 역추적하여 `.gitignore` 대상(로컬 격리용 `tool/`, `sample_workspace/`, `build/`, `dist/`, 캐시/로그)이 실수로 업로드되는 것을 CI 상에서 원천 방어 (`scripts/check_release_hygiene.py` 연동).
- **로컬 원클릭 품질 게이트(Local Quality Gate)**: CI와 동일한 7단계의 안전성 검증을 개발자 PC에서 단일 명령어로 원클릭 일괄 수행하는 로컬 전용 래퍼 통합 (`scripts/run_quality_gate.py` 추가).
- **GitHub Actions 원격 검증 PASS 확인**: `Finance DataMart CI` 워크플로우가 `main` 브랜치 커밋 `842c613c5e0f2ba098bb483032c8243c738456a3`에서 PASS 완료.
- **공식 배포 자산 43종 정합성 완성**: 신규 검증 스크립트 2종, CI 구성 파일, Phase 24 원격 CI 결과 보고서를 추가 반영하여 배포 대상을 총 43종 사양으로 갱신 완료.
- **로컬 전용 격리 유지**: `tool/` 폴더 내에 빌드 및 임시 산출물들을 보관하고 git 추적 대상에서 격리하는 배포 위생 원칙 고수.
