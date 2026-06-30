# 유지보수 및 이슈 대응 가이드 (MAINTENANCE.md)

본 문서는 Finance DataMart Tool을 GitHub 공개 저장소로 배포한 이후, 버그 핫픽스, 후속 릴리즈 갱신 및 사용자의 이슈 보고 요령을 통제하기 위한 **운영 관리 가이드라인**입니다.

---

## 🔒 1. 이슈/버그 리포트 작성 시 보안 수칙 (필수 준수)
오픈소스 리포지토리에 이슈를 등록하거나 풀 리퀘스트(PR)를 작성할 때는 **사내 중요 자산 및 기밀 정보 노출 방지**를 위해 다음 수칙을 철저하게 준수해야 합니다.

1. **사내 운영 데이터 및 절대 경로 노출 절대 금지**:
   - 에러가 발생한 원본 엑셀 데이터 파일(`Sales_Closing_*.xlsx` 등)을 이슈 화면에 직접 업로드하지 마십시오.
   - 예외 내용 기술 시 로컬 절대 경로(예: `[local_user_path]`)가 포함되지 않도록 마스킹 처리하여 기재하십시오.
2. **로그 전체 복사 붙여넣기 금지**:
   - `error_log.txt` 또는 터미널 상세 디버그 콜스택 전문을 무분별하게 복사하여 업로드하지 마십시오. 사내 시스템 명칭이나 민감한 업무 프로세스가 역추적될 수 있습니다.
   - **조치 요령**: 에러 메시지의 대표 내용(예: `ValueError: Columns mismatch in custom sheet`) 수준으로 요약하여 작성하십시오.
3. **가상 재현 환경 구성**:
   - 재현 단계를 묘사할 때는 오직 가상 데이터(Customer A, Product M-100 등)만을 예시로 차용하십시오.

---

## 🚀 2. 핫픽스 및 패치 릴리즈 가이드
버그 수정이나 로컬 기능 패치를 수행한 후 원격 저장소에 반영(Release)하기 전에 반드시 아래 절차를 수행해야 합니다.

1. **가상 데이터 테스트 원칙**:
   - 핫픽스 유효성 테스트 시 절대로 실제 회사 데이터를 개발 로컬 트리에 보관하지 않으며, `scripts/create_sample_data.py`로 생성된 가상 샘플 데이터만을 사용하여 검증을 이행합니다.
2. **무결성 자가 진단 의무 수행**:
   - 코드 수정 완료 후 원격 브랜치에 커밋/푸시하기 전, 프로젝트 루트에서 반드시 다음 진단을 구동합니다.
   ```bash
   python scripts/pre_release_check.py
   ```
   - **통과 요건**: 7가지 자동 진단 영역이 전부 **[PASS]**를 기록하고 종료 코드 `0`으로 완결되는지 교차 확인해야만 릴리즈 가용성을 획득합니다.
3. **로컬 캐시 및 결과물 정비**:
   - `git status --short --ignored`를 조회하여 테스트 과정에서 임시 생성된 `.csv` 정제 파일이나 컬럼 인벤토리 엑셀 파일이 커밋 대상에 포함되지 않는지 확인합니다.
   - ignored 파일 전체를 일괄 삭제하는 명령은 `.venv`, `.env` 같은 로컬 환경 파일까지 제거할 수 있으므로 유지보수 가이드에서는 사용하지 않습니다.

---

## 📌 3. 버전 네이밍 원칙
본 도구는 유의적 버전(Semantic Versioning) 규칙을 기반으로 소스코드를 관리합니다.
- **메이저 버전 (vX.0.0)**: 하위 호환성이 깨지는 대규모 아키텍처적 개편 시
- **마이너 버전 (v1.X.0)**: 기존 엔진 호환성을 유지하며 신규 data_group 추가 또는 Report View 집계 기능 고도화 시
- **패치 버전 (v1.0.X)**: 기존 설정을 유지한 채 버그 핫픽스 및 예외 처리 구문 보완 시
- **배포 방식 관리**: 핫픽스 및 기능 패치 버전은 소스코드 배포를 기본으로 하며, 독립 실행 Setup 관련 변경이 있을 때만 `scripts/build_standalone.py`로 `FinanceDataMart_Setup.exe`를 재빌드하고 GitHub Release asset을 갱신합니다.

---

## 🛠️ 4. GitHub Actions CI 실패 시 조치 가이드
원격 저장소에 푸시(Push)하거나 PR을 전송한 뒤, GitHub Actions 자동 검증(`Finance DataMart CI`) 빌드가 실패(빨간 불)한 경우 아래 절차에 따라 진단 및 조치를 수행하십시오.

1. **GitHub CI 로그 확인**:
   - GitHub Actions 탭에서 실패한 워크플로우 단계를 확인하여 `Release Hygiene Check` 또는 `Run Local Quality Gate` 중 어느 구간에서 실패가 발생했는지 식별합니다.
2. **로컬 품질 게이트를 통한 재현 및 확인 (권장)**:
   - 원격 저장소에 수정 코드를 다시 푸시하기 전, 로컬 개발 환경에서 품질 검사 스크립트를 실행하여 모든 검증이 통과하는지 한 번에 점검하십시오:
     ```bash
     python scripts/run_quality_gate.py
     ```
   - 만약 특정 단계가 실패할 경우, 개별 스크립트들을 수동 기동하여 디버깅할 수 있습니다:
     ```bash
     # 1) 배포 위생 검사 단독 테스트
     python scripts/check_release_hygiene.py

     # 2) 전체 코드 컴파일 정상 여부 검사
     python -m compileall app scripts

     # 3) 무결성 자가 진단 가동 (7대 항목 PASS 확인)
     python scripts/pre_release_check.py

     # 3) GUI 모듈 임포트 가능 여부 검사
     python -c "from app.ui_app import DataMartUI; print('UI import ok')"
     ```
3. **배포 위생 체크 (Release Hygiene Check 실패 시)**:
   - 만약 GitHub Actions 빌드 중 `Release Hygiene Check` 단계에서 실패한 경우, 이는 `.gitignore` 대상 폴더(예: `sample_workspace/`, `tool/`, `build/`, `dist/` 등)나 캐시 파일이 실수로 Git에 의해 추적(tracked)되고 있는 상태입니다.
   - **조치 요령**: 로컬 터미널에서 다음 명령어를 실행하여 문제를 해결하십시오:
     ```bash
     # 1) 로컬 위생 검사 스크립트 실행으로 위반 목록 확인
     python scripts/check_release_hygiene.py

     # 2) 실수로 추적된 대상을 Git 관리 대상에서만 수동 제거 (실제 파일은 삭제되지 않음)
     git rm -r --cached sample_workspace/
     git rm -r --cached tool/
     # (기타 위반으로 나열된 파일들에 대해 동일하게 git rm --cached 실행)

     # 3) 정리 후 커밋 작성 및 푸시
     git commit -m "Fix release hygiene by untracking forbidden files"
     git push
     ```

---

## 🔍 5. GitHub Actions 원격 실행 결과 수동 확인 절차
원격 GitHub Actions CI 결과를 최종 검인할 때는 다음 수동 검증 순서에 따라 처리하십시오.

1. **원격 푸시(Push) 또는 PR 생성**:
   - 로컬에서 `python scripts/run_quality_gate.py`로 사전 품질 게이트를 완료한 후, 코드를 GitHub 원격 저장소에 푸시하거나 Pull Request를 생성합니다.
2. **GitHub Actions 탭 모니터링**:
   - GitHub 리포지토리 웹 페이지 상단의 **Actions** 탭으로 이동합니다.
   - 최근 푸시된 커밋 메시지 또는 PR 제목으로 진행 중인 `Finance DataMart CI` 워크플로우 실행을 확인합니다.
3. **세부 단계 통과 여부 교차 검증**:
   - 워크플로우 실행을 클릭하여 세부 단계를 진입합니다.
   - **Release Hygiene Check** 단계가 성공(Green Check)했는지 확인하여 `.gitignore` 대상 파일들이 원격에 노출되지 않았는지 검증합니다.
   - **Run Local Quality Gate** 단계가 성공했는지 확인하여 소스 컴파일, 샘플 데이터 정제 연산, 무결성 자가 진단(7대 항목 PASS)이 가상 Windows 환경에서도 완벽히 가동하는지 확인합니다.
4. **최종 릴리즈 가용성 확정**:
   - 원격 Actions 빌드가 모두 초록색(PASS)으로 완료되면, 비로소 Phase 24 완료를 선언하고 배포용 RC3 릴리즈를 공식 마감(Releases 탭에 standalone Setup 업로드)할 수 있습니다. 만약 원격 빌드가 통과하지 않았다면 Phase 24는 대기(In Progress) 상태로 계속 묶이게 됩니다.
