# 공개 후 초기 확인 체크리스트 (POST_RELEASE_CHECKLIST.md)

본 문서는 프로젝트를 외부 GitHub 저장소에 퍼블릭 업로드(Push)한 직후, 운영 담당자가 리포지토리의 위생 및 초기 배포 무결성을 최종 검수하기 위한 **공개 후 사후 검진 체크리스트**입니다.

---

## 📋 공개 후 즉시 확인 항목

### 1. 원격 저장소 파일 위생 검사
- [ ] GitHub 웹 인터페이스에서 업로드된 파일 구조를 브라우징하여 `RELEASE_MANIFEST.md`에 명시된 43종의 공식 자산 외에 불필요한 임시 파일이 없는지 확인합니다.
- [ ] GitHub Actions 빌드 이력에서 `Release Hygiene Check` 단계가 통과(Green)하여 업로드 차단 폴더/파일이 유입되지 않았음을 교차 확인합니다.
- [ ] GitHub Release에 `FinanceDataMart_Setup.exe`가 asset으로 첨부되어 있는지 확인합니다. 이 파일은 저장소 커밋 대상이 아니라 Release 첨부 대상입니다.
- [ ] 특히 `.venv/` 파이썬 가상환경 폴더, `__pycache__/` 바이트코드 캐시, 로컬 개발 시 생성되었던 `column_inventory.xlsx`, `validation_log.csv` 등의 임시 산출물이 노출되지 않았는지 이중 스캔합니다.

### 2. 라이선스 정상 적용 검안
- [ ] 공개 저장소 루트의 `LICENSE` 파일이 GitHub 상에서 MIT License로 정상 표기 및 렌더링되는지 확인합니다.

### 3. 기밀 데이터 노출 차단 확인
- [ ] `sample_workspace/` 폴더가 GitHub 원격 저장소에 업로드되지 않았는지 확인합니다. 샘플 Raw Excel과 `config.xlsx`는 다른 PC에서 `scripts/create_sample_data.py`로 재생성해야 합니다.

### 4. 격리 클론 가동성 검증 (배포 검사)
- [ ] GitHub Actions 탭에서 `Finance DataMart CI` 워크플로우가 성공(PASS)했는지 확인합니다.
- [ ] 별도의 테스트용 폴더 혹은 다른 PC 환경에서 공개된 원격 저장소를 클론(`git clone`)하거나 다운로드합니다.
- [ ] 파이썬 가상환경 구축 후 의존성을 설치하고, **로컬 품질 게이트 스크립트**를 실행하여 원클릭으로 모든 검증이 PASS하는지 교차 확인합니다:
  ```powershell
  # 1. 가상환경 생성 및 활성화
  python -m venv .venv
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  .\.venv\Scripts\Activate.ps1
  
  # 2. 의존 패키지 설치
  pip install -r requirements.txt
  
  # 3. 로컬 품질 게이트 일괄 실행
  python scripts/run_quality_gate.py
  ```
- [ ] 최종적으로 콘솔에 `Quality gate PASS`가 정상 출력되고 프로세스가 종료 코드 `0`으로 완료되는지 확인합니다.

### 5. 이슈 관리 보안 규정 리마인드
- [ ] 향후 외부 사용자로부터 유입되는 이슈(Issue)나 풀 리퀘스트(PR) 관리 시, 임직원들이 사내 실데이터 및 디버그 스택 트레이스 전체를 유출하지 않도록 `MAINTENANCE.md` 규정을 준수하여 초기 대응이 수립되었는지 검토합니다.
