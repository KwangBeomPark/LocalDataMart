# 공개 전 최종 체크리스트 (PUBLIC_RELEASE_CHECKLIST.md)

본 문서는 프로젝트를 외부 GitHub 등에 퍼블릭 공개하기 전에 검수자가 반드시 수행하고 확인해야 할 보안 및 정합성 체크리스트입니다.

---

## 📋 공개 전 확인 필수 항목

### 1. 무결성 자가 진단 통과 여부
- [ ] `python scripts/pre_release_check.py` 명령을 콘솔 또는 데스크톱 GUI에서 실행하여 7가지 진단 항목이 모두 `PASS`를 받는지 검수합니다.

### 2. 소스코드 및 로그 파일 내 절대 경로 노출 배제
- [ ] 로컬 PC의 개발 경로(예: `[local_user_path]`)가 소스코드 내부 주석이나 로그 파일(`refresh_log.csv`, `error_log.txt`)에 유출되어 남아있지 않은지 검사합니다.
- [ ] 소스코드 및 예외 처리 구문(`except Exception`)에서 전체 스택 트레이스를 그대로 파일에 출력하지 않는 구조가 고수되고 있는지 확인합니다.

### 3. 기밀 및 사내 자산 정보 검열
- [ ] 소스코드 및 가상 데이터 스키마 내에 실제 운영 거래처명, 임직원 이메일 주소, 사내 서버 IP나 개발 서버 URL이 포함되지 않았는지 점검합니다.
- [ ] `sample_workspace/` 전체가 `.gitignore`로 격리되어 GitHub 업로드 대상에서 제외되는지 확인합니다. 로컬에 생성된 엑셀 파일은 오직 `create_sample_data.py`로 생성된 가상 모조 데이터여야 합니다.

### 4. 오픈소스 라이선스 정책 합의
- [ ] 사용자가 프로젝트 공식 라이선스로 MIT License를 선택했는지 확인합니다.
- [ ] 프로젝트 루트 디렉토리에 공식 `LICENSE` 파일이 존재하고 MIT License 전문이 포함되어 있는지 확인합니다.

### 5. 미지원/금지 기술의 유입 유무 재확인
- [ ] 파이썬 패키지 의존성 목록(`requirements.txt`) 및 소스코드 전반에 `fastapi`, `flask`, `duckdb`, `parquet`, `pyside6` 등의 금지된 단어가 혼입되지 않았는지 확인합니다. `pyinstaller`는 `scripts/build_installer.py`와 인스톨러 문서에서만 허용합니다.

### 6. Git 저장소 위생 관리 및 캐시 파기
- [ ] 소스코드 및 문서 릴리즈 전 `git status`를 구동하여 런타임 시에 생성된 분석 파일(`column_inventory.xlsx`), 대조 정합성 로그(`validation_log.csv`), 파일 통계 로그(`refresh_log.csv`) 등 임시 산출물들이 트래킹 리스트에서 완벽히 격리(.gitignore 적용)되었는지 검수합니다.
- [ ] 릴리즈 태깅 직전 불필요한 임시 빌드 캐시를 제거하여 깔끔한 패키지 상태를 보존합니다.

### 7. 업로드 가이드 이행 점검
- [ ] [GitHub 업로드 가이드 (GITHUB_RELEASE_GUIDE.md)](GITHUB_RELEASE_GUIDE.md) 상의 수동 깃허브 초기화 및 태깅 지침이 실제 디렉토리 상태와 정합한지 최종 크로스 체크합니다.

### 8. 배포 후 유지보수 체계 정립 확인
- [ ] [유지보수 및 이슈 대응 가이드 (MAINTENANCE.md)](MAINTENANCE.md)를 통해 배포 이후 사용자의 보안 준수 요령(회사 데이터/절대 경로 노출 금지) 및 유의적 버전 관리 지침이 정상 수립되었는지 검토합니다.

### 9. 다른 PC 설치 테스트 가이드 탑재 여부
- [ ] 다른 PC에서 본 저장소를 다운로드/클론했을 때 정상 작동 검증을 수행할 수 있도록 [배포 버전 설치 테스트 가이드 (DISTRIBUTION_TEST_GUIDE.md)](DISTRIBUTION_TEST_GUIDE.md)가 정합하게 작성되어 탑재되었는지 확인합니다.
