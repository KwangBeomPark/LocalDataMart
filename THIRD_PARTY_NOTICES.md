# 제3자 소프트웨어 고지서 (THIRD_PARTY_NOTICES.md)

이 문서는 Finance DataMart Tool의 source-only release candidate 기준 외부 의존성을 정리합니다.

## 현재 외부 의존성

`requirements.txt` 기준 설치 대상은 다음 두 패키지입니다.

| package | purpose |
|---|---|
| pandas | CSV/Excel 데이터 처리, 컬럼 매핑, 집계, reconciliation 계산 |
| openpyxl | `.xlsx` 파일 읽기 및 `column_inventory.xlsx` 생성 |

## 라이선스 확인 상태

이 문서는 의존성 목록을 기록하기 위한 고지서입니다. 공개 릴리즈 전에는 각 패키지의 실제 설치 버전과 공식 라이선스 정보를 다시 확인해야 합니다.

프로젝트 자체의 공식 라이선스는 MIT License이며, 전문은 루트의 `LICENSE` 파일을 참조합니다.

## 주의 사항

- 이 문서는 특정 패키지 버전을 고정하지 않습니다.
- 이 문서는 라이선스 법률 검토를 대체하지 않습니다.
- 새 의존성이 `requirements.txt`에 추가되면 이 문서도 함께 갱신해야 합니다.
