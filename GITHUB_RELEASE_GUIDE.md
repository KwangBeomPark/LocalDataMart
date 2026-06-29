# GitHub 공개 저장소 업로드 및 최초 릴리즈 가이드 (GITHUB_RELEASE_GUIDE.md)

본 문서는 Finance DataMart Tool을 퍼블릭 GitHub 저장소에 안전하고 깨끗하게 수동으로 초도 커밋 및 배포(Release)하기 위해 **사용자가 직접 이행해야 하는 최종 운영 지침서**입니다.

---

## 🚫 1. 배포 사양 및 제약 사항
1. **Source-only 배포**: 본 릴리즈는 소스코드 공개 형태이며, 컴파일된 단일 실행 파일(`.exe`)이나 자동 인스톨러는 제공하지 않습니다.
2. **CI/CD 및 Actions 배포 배제**: 원격 빌드나 자동 테스트 통합(GitHub Actions)은 내장되어 있지 않으며, 모든 검증은 로컬 터미널에서 수동으로 이행됩니다.
3. **다른 PC 설치 테스트 목적**: 본 배포본은 다양한 환경의 다른 PC에서 소스코드를 복사/클론하여 의존 패키지 설치부터 데이터마트 기동 및 무결성 진단까지 전 과정을 수동으로 검증할 수 있도록 돕는 것을 목표로 합니다.

---

## 📋 2. 업로드 전 필수 조치 사항 (사용자 직접 확인)

### [확인 1] 오픈소스 라이선스 파일(`LICENSE`) 확인
현재 저장소에는 사용자가 선택한 MIT License 전문이 `LICENSE` 파일로 포함되어 있습니다. 공개 업로드 전 루트의 `LICENSE` 파일이 누락되지 않았는지 확인해야 합니다.

### [확인 2] 로컬 무결성 자가 진단 실행
퍼블릭 업로드 전, 코드가 정상 컴파일되며 불필요한 사내 절대 경로와 상세 디버그 콜스택이 사용자용 로그에 노출되지 않는지 최종 자가 진단을 수행합니다.
```bash
python scripts/pre_release_check.py
```
- **출력 결과**: 7가지 진단 항목이 모두 **[PASS]**를 획득해야 릴리즈가 가능합니다.

### [확인 3] 저장소 위생 상태 및 캐시 정리
정제 연산으로 재생성된 로컬 CSV 파일들과 logs 파일들이 깃 커밋 리스트에 노출되지 않도록 최종 격리를 점검합니다.
```bash
# 1. 깃 상태 조회를 통해 임시 xlsx/csv가 올라오지 않는지 확인
git status --short --ignored
```

ignored 파일 전체를 일괄 삭제하는 명령은 `.venv`, `.env` 같은 로컬 환경 파일까지 제거할 수 있으므로 공개 직전 수동 점검 가이드에서는 사용하지 않습니다.

---

## 🚀 3. 수동 GitHub 연동 및 최초 커밋 절차

### 1단계: 원격 GitHub 리포지토리 개설
- 본인의 GitHub 계정에 접속하여 신규 퍼블릭 저장소(Public Repository)를 생성합니다. (※ README, .gitignore 생성 체크 박스는 모두 해제한 클린 상태로 생성)

### 2단계: 로컬 저장소 초기화 및 원격 브랜치 연결
로컬 프로젝트 루트 폴더에서 터미널을 열고 아래 명령어를 순차적으로 실행하여 최초 원격 저장소 매핑을 수행합니다.
```bash
# 1. 로컬 git 초기화
git init

# 2. 원격 저장소 추가 (URL에 본인의 GitHub 주소 대입)
git remote add origin https://github.com/[YOUR_GITHUB_ID]/LocalDataMart.git

# 3. 기본 브랜치를 main으로 설정
git branch -M main
```

### 3단계: 초도 커밋 생성 및 최초 푸시
```bash
# 1. 모든 소스 및 문서 파일 추가 (.gitignore 격리 외 대상)
git add .

# 2. 최초 릴리즈 후보 버전 커밋 메시지 작성
git commit -m "Initial commit of v1.0.0-RC1 (Source-only Release Candidate)"

# 3. 원격 저장소 최초 푸시
git push -u origin main
```

### 4단계: Release Candidate (RC) 태그 설정 및 업로드
```bash
# 1. 로컬 릴리즈 태그 설정
git tag -a v1.0.0-RC1 -m "Release Candidate 1"

# 2. 원격 저장소에 태그 푸시
git push origin --tags
```
이후 GitHub 저장소 페이지의 `Releases` 탭으로 이동하여 `Draft a new release` 버튼을 누르고 `v1.0.0-RC1` 태그를 지정한 후, `RELEASE_NOTES.md` 본문 내용을 설명에 첨부하여 배포를 완료하십시오.

### 5단계: 다른 PC 설치 테스트 연동 및 피드백 접수
- 업로드가 완료되면 다른 검증 PC(또는 환경)를 준비하여 [배포 버전 설치 테스트 가이드 (DISTRIBUTION_TEST_GUIDE.md)](DISTRIBUTION_TEST_GUIDE.md) 지침에 따라 가상환경 구축 및 파이프라인 구동이 원활하게 통과되는지 확인하고, 피드백을 전달하십시오.
