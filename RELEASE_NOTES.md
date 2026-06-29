# 릴리즈 노트: v1.0.0-RC1 (RELEASE_NOTES.md)

본 문서는 Finance DataMart Tool의 첫 번째 릴리즈 후보 버전인 **v1.0.0-RC1 (Release Candidate 1)**에 관한 사양서입니다.

---

## 📦 1. 배포 형태 및 기본 규칙
- **Source-only 배포**: 본 릴리즈 버전은 오직 소스코드 형태로만 배포되며, 독립형 실행 파일(`.exe`) 또는 자동 설치 프로그램(installer)은 현재 내장 및 지원하지 않습니다.
- **가상 데이터 기반**: 테스트 및 동작 검증을 위해 `sample_workspace` 폴더 내에 생성되는 데이터들은 100% 임의 모조된 가상 데이터입니다.
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
