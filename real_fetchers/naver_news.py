"""Naver 뉴스 검색 실API fetcher — 이 프로젝트에서는 사용하지 않기로 결정함.

## 조사 결과 (2026-09-12 확인)

2026-09-07 시행된 'NAVER API 서비스 이용약관(검색 API 특약)' 개정으로, 검색 API
(뉴스/블로그/이미지/카페/지식iN/책/백과사전/쇼핑/전문자료 등 developers.naver.com의
"검색" 카테고리 전체)로 받은 데이터는:
  - AI에 입력하거나 학습/개선/평가/노출에 활용 금지
  - 제3자 제공·판매 금지
  - 복사·저장·캐싱 금지
  - 광고 수익화 금지
  - "네이버 검색결과를 그대로, 가공 없이 노출"하는 용도로만 허용

이 프로젝트가 하려는 일(응답을 로컬 JSON으로 저장하고, 화제도 스코어로 가공해서
집계하는 것) 자체가 "저장·캐싱 금지"와 "가공 없이 노출" 조항에 정면으로 걸린다.
뉴스 검색 API를 이 파이프라인에서 완전히 제외하기로 함.

참고로 데이터랩("데이터랩 통합검색 트렌드")은 developers.naver.com에서 "검색"과
분리된 별도 최상위 카테고리라, 이번에 개정된 "검색 API 특약" 적용 대상이 아닌
것으로 보임 — real_fetchers/datalab.py는 그대로 사용.

출처:
- https://www.dataeconomy.co.kr/news/articleView.html?idxno=42307
- https://www.tokenpost.kr/news/ai/403521
- https://naver.github.io/naver-openapi-guide/apilist.html (카테고리 분류 확인용)

run_real_test.py는 이 모듈을 import하지 않는다. fetch()는 구현하지 않는다.
"""
