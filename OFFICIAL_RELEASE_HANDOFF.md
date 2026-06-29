# 공식 배포 핸드오프 지침서 (OFFICIAL_RELEASE_HANDOFF.md)

본 문서는 Finance DataMart Tool을 GitHub 퍼블릭 저장소에 최종 업로드 및 릴리즈하기 직전, 사용자가 확인하고 수행해야 할 **최종 수동 점검 및 배포 절차 요약서**입니다.

---

## 🔒 1. 라이선스 정책 확정
- **공식 라이선스 상태**: **MIT License 확정 (LICENSE 파일 포함)**
- **탑재 사항**:
  - 사용자가 프로젝트 공식 라이선스로 MIT License를 선택했습니다.
  - 선택된 라이선스의 공식 전문은 프로젝트 루트의 `LICENSE` 파일에 포함되어 있습니다.

---

## 📦 2. 배포 사양 최종 선언
본 프로젝트는 소스코드 배포판을 기본으로 하며, GitHub Release asset으로 AppData 설치용 `FinanceDataMart_Installer.exe`를 선택 제공할 수 있습니다. 아래 제약을 재확인하십시오.
- **완전 독립형 앱 아님**: 인스톨러는 AppData 복사, `.venv` 생성, 의존성 설치, 샘플 생성, 바로가기 생성을 자동화하지만 대상 PC에 Python 3.8 이상과 인터넷 연결이 필요합니다.
- **CI/CD 자동화 배제**: GitHub Actions 워크플로우 또는 테스트 파이프라인 연동 기능은 포함되어 있지 않으며, 배포는 전적으로 사용자의 수동 명령어 기반으로 가동됩니다.
- **플랫폼 제약성**: DuckDB, Parquet, Power BI, ODBC, SharePoint 연동은 포함되어 있지 않습니다.

---

## 📋 3. 공식 릴리즈 업로드 직전 수동 확인 사항
사용자는 배포 커밋을 작성하기 전 다음 사항을 자가 검수해야 합니다.
1. **무결성 진단 100% PASS**:
   - `python scripts/pre_release_check.py` 진단 결과가 7개 항목 모두 **[PASS]**를 기록하는지 최종 점검합니다.
2. **저장소 위생 정리 (임시 산출물 완전 배제)**:
   - `sample_workspace/` 이하에 생성된 런타임 결과물(`.csv`, `.xlsx`, `error_log.txt`)이 `.gitignore` 처리에 의해 트래킹에서 제외되었는지 검사합니다.
3. **가상 데이터 세트 원칙 준수**:
   - `sample_workspace/01_Input_Raw/` 내부에 실제 사내 매출 데이터나 임직원 개인정보 파일이 존재하지 않는지 스캔하고, 오직 `scripts/create_sample_data.py`로 생성된 가상 샘플 데이터만 기재되어 있는지 확인합니다.

---

## 🛠️ 4. 수동 Git 배포 명령어 퀵 레퍼런스
사용자가 직접 로컬 터미널에서 순차 실행해야 하는 Git 커맨드 예시입니다. (실제 에이전트 내에서는 동작하지 않으며, 사용자가 직접 기동합니다.)

```bash
# 1단계: 로컬 상태 확인
git status --short --ignored

# 2단계: Git 로컬 저장소 초기화 및 브랜치명 설정
git init -b main

# 3단계: 원격 GitHub 저장소 매핑
git remote add origin https://github.com/사용자계정/LocalDataMart.git

# 4단계: RELEASE_MANIFEST.md의 32종 공식 파일 추가
git add .

# 5단계: 첫 번째 공식 릴리즈 커밋 작성
git commit -m "Release v1.0.0-RC1 with AppData installer support"

# 6단계: 릴리즈 태깅 (Release Candidate 1)
git tag -a v1.0.0-RC1 -m "Release Candidate 1"

# 7단계: 원격 저장소로 코드 및 태그 푸시
git push -u origin main
git push origin --tags
```
