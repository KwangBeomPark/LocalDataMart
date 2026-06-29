# 릴리즈 매니페스트: 공식 배포 파일 목록 (RELEASE_MANIFEST.md)

본 문서는 Finance DataMart Tool의 퍼블릭 소스 공식 배포판에 최종 포함되는 소스코드 및 문서 자산의 전체 목록(Manifest)입니다. 배포 업로드 시 아래 명시된 항목들만 정합하게 업로드되어야 하며, `sample_workspace/` 전체와 런타임 중 재생성되는 캐시, 임시 CSV, 로그, 엑셀 결과물은 제외됩니다.

---

## 📂 1. 배포 대상 파일 목록 (총 38종)

### 1) 프로젝트 핵심 설정 및 메인 가이드 (7개)
- `README.md`: 프로젝트 개요, 퀵스타트 및 핵심 제약 조건 명세서
- `requirements.txt`: 외부 종속성 라이브러리(`pandas`, `openpyxl`) 명세
- `.gitignore`: 저장소 위생을 위한 캐시 및 런타임 결과물 제외 설정 파일
- `LICENSE`: 프로젝트 공식 MIT License 전문
- `myAGENT.MD`: AI Pairs pair programming 전용 지침 문서
- `AI_CODE_MAP.MD`: 프로젝트 소스코드 디렉토리 지도 및 컴포넌트 해설서
- `PROJECT_ROADMAP.MD`: 데이터마트 기능 고도화 로드맵

### 2) 배포 가이드 및 사용자 지침 문서 (12개)
- `USER_GUIDE.md`: CLI/GUI 실행 순서 및 Config 시트 매핑 상세 기술문서
- `KNOWN_LIMITATIONS.md`: 인메모리 OOM 한계 및 연동 플랫폼 미지원 고지서
- `PUBLIC_RELEASE_CHECKLIST.md`: 보안 검열 및 수동 릴리즈 자가 체크리스트
- `RELEASE_NOTES.md`: v1.0.0-RC1 배포 사양 및 후속 Changelog 작성 지침서
- `THIRD_PARTY_NOTICES.md`: Pandas/OpenPyXL 라이선스 및 PSF 저작권 고지서
- `GITHUB_RELEASE_GUIDE.md`: 사용자의 원격지 수동 저장소 연동 및 릴리즈 태깅 매뉴얼
- `MAINTENANCE.md`: 이슈 제보 시의 사내 보안 준수 및 패치 전 자가 진단 가이드라인
- `RELEASE_MANIFEST.md`: 본 배포 대상 목록 파일
- `OFFICIAL_RELEASE_HANDOFF.md`: 공식 공개 업로드 전 최종 수동 점검 및 배포 절차 요약서
- `POST_RELEASE_CHECKLIST.md`: 공개 후 원격 저장소 파일 위생 및 가동성 확인 체크리스트
- `LICENSE_DECISION_GUIDE.md`: 사용자의 오픈소스 라이선스 검토 및 결정용 안내서
- `DISTRIBUTION_TEST_GUIDE.md`: 타 PC에서의 소스코드 다운로드 및 가동성 검증용 다른 PC 설치 테스트 가이드

### 3) 정제 및 요약 엔진 모듈 (`app/` 폴더 - 11개)
- `app/__init__.py`: 패키지 초기화 파일
- `app/main.py`: 데이터마트 전체 파이프라인 제어 진입점
- `app/config_loader.py`: `config.xlsx` 설정 파싱 및 사전 유효성 검증
- `app/file_scanner.py`: 지정 경로 내 대상 Excel 파일 스캔 및 처리 순서 보장
- `app/excel_reader.py`: 원본 Excel 데이터를 읽기 모드로 안전 파싱
- `app/transformer.py`: Config 기반 keep 열 매핑 정제 데이터 생성
- `app/report_generator.py`: Report_View 설정에 근거한 sum/count 요약 리포트 집계
- `app/validator.py`: 원본 엑셀 행/금액 합계 정보 대조 Reconciliation 정합성 검증
- `app/logger_setup.py`: 사용자용 무오류 정밀 로그 시스템 설정
- `app/ui_app.py`: tkinter 기반 비동기 데스크톱 GUI 제어반 모듈
- `app/column_inventory.py`: Raw 엑셀 컬럼 인벤토리 분석 집계 추출 모듈

### 4) 운영 및 검증용 스크립트 (`scripts/` 폴더 - 6개)
- `scripts/create_sample_data.py`: 가상 데이터 및 설정 템플릿 복구 유틸리티
- `scripts/create_column_inventory.py`: 신규 파일의 스키마 분석용 인벤토리 추출기
- `scripts/pre_release_check.py`: 배포 전 자가 무결성 7대 진단 검증기 (★ PASS 획득 필수)
- `scripts/run_desktop_app.py`: 데스크톱 GUI 원클릭 가동용 래퍼 스크립트
- `scripts/installer.py`: AppData 설치 및 가상환경, 바로가기를 자동 생성해주는 자가 설치 스크립트
- `scripts/build_installer.py`: 자가 설치 스크립트를 PyInstaller로 단일 exe로 빌드해주는 배포 스크립트
