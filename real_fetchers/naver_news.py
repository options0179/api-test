"""Naver 뉴스 검색 실API fetcher — 보류.

2026-09-07 개정된 'NAVER API 서비스 이용약관(검색 API 특약)'이 검색 API를
"네이버 검색결과를 그대로 노출하는 용도"로만 허용하고, 받은 데이터를 가공/재처리
하거나 AI 파이프라인에 넣는 걸 금지하는 것으로 보인다. 이 프로젝트가 하려는
"화제도 스코어로 가공"이 여기 걸릴 수 있어서, 사용자가 developers.naver.com에서
약관 원문을 직접 확인하기 전까지는 구현하지 않는다.

run_real_test.py는 이 모듈을 import하지 않는다. 확인 끝나면 fetch(keyword)가
fetchers/naver_news.py의 mock과 같은 TrendSignal을 반환하도록 구현할 것.
"""
