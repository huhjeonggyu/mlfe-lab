# SKKU MLFE Lab 홈페이지

기존 Google Sites의 공개 내용을 옮긴 GitHub Pages용 연구실 홈페이지입니다. 별도 서버와 데이터베이스 없이 운영할 수 있습니다.

## 처음 공개하기

현재 자료는 GitHub 업로드용 완성 파일입니다. 아직 저장소를 생성하거나 공개하지 않았습니다.

1. 새 GitHub 공개 저장소를 준비합니다. 제안 이름: mlfe-lab.
2. 압축을 풀고 이 폴더의 파일들을 저장소에 올립니다. 완성된 웹페이지는 docs 폴더에 있습니다.
3. 게시할 저장소를 확정한 후 Settings → Pages → Build and deployment → Source에서 Deploy from a branch를 선택합니다.
4. 업로드한 브랜치(예: main)와 /docs를 선택하고 Save합니다.
5. 완료되면 Pages 화면에 나타나는 주소로 접속합니다.

huhjeonggyu/mlfe-lab 저장소를 쓸 경우 예상 주소는 https://huhjeonggyu.github.io/mlfe-lab/ 입니다. 현재 존재하는 공개 주소라는 뜻은 아닙니다.

자동으로 생성·게시하는 GitHub Actions 설정은 포함하지 않았습니다. 게시할 저장소·브랜치·공개 범위를 확정한 뒤 추가할 수 있습니다.

## 평소 수정 방법

이 작업에서 다음처럼 요청하시면 됩니다.

- “이 학생을 추가해줘. 이름, 과정, 사진, 연구 주제는 이거야.”
- “이 사람은 졸업생으로 옮기고 2027년 2월 졸업, 진로는 이렇게 적어줘.”
- “학회 소식을 추가하고 참여한 사람은 누구누구로 연결해줘.”
- “이 논문을 게재 논문으로 옮겨줘.”

내용 수정 → 미리보기 확인 → GitHub 반영 순서로 운영합니다.

## 내용이 저장되는 곳

| 내용 | 관리 파일 |
|---|---|
| 홈 소개 | content/site.json |
| 구성원·졸업생 | content/people/이름.json |
| 연구실 소식 | content/news/소식.json |
| 논문·투고 원고 | content/publications.json |
| 연구, 연구 노트, 이력, 강의·발표, 과제 | content/pages/*.json |
| 진학·연락 안내 | content/contact.json |
| 사진·연구 이미지 | assets/images/ |

구성원의 group을 Alumni로 바꾸고 graduated, placement를 넣으면 졸업생 목록으로 이동합니다. 이름이 바뀌어도 id는 유지하세요.

소식과 논문의 members에는 관련 구성원의 id를 넣습니다. 해당 사람의 상세 페이지에도 자동 표시됩니다. 기존 People의 개인 연구·발표 목록은 원문 상태를 보존한 별도 활동 기록입니다. 논문 제목이나 상태를 바꿀 때 같은 내용의 활동 기록도 함께 확인합니다.

sections는 제목, 문단, 목록, 이미지 순서입니다. html에 링크·줄바꿈·첨자를 넣을 수 있습니다.

## 다시 만들기와 미리보기

Python 3.10 이상만 있으면 되고 추가 설치는 필요 없습니다.

    python scripts/build.py
    python scripts/validate.py
    python -m http.server 4173 --bind 127.0.0.1 --directory docs

브라우저에서 http://127.0.0.1:4173/ 를 엽니다.

docs는 생성 결과입니다. 직접 수정하지 말고 content 또는 assets를 수정한 뒤 다시 만드세요. GitHub에 갱신된 docs도 함께 반영합니다. 상대 경로를 사용해 저장소 하위 주소에서도 작동합니다.

## 이전 범위

- 기존 공개 페이지 10개와 구성원·소식 상세를 포함해 30개 화면
- 현재 구성원 14명, 졸업생 8명, 소식 4건
- 논문·투고 원고 45건, 기존 원본과 첨부 사진을 포함한 이미지 36개 보관
- 수식 연구 노트 7장, 강의 도표, 특허 출원 내역 포함
- 2026-09-17에 직접 읽은 공개 HTML을 기준으로 이전
- 저자 순서·별표·투고 상태·강의 예정일·지원금·특허 출원 상태 보존
- 외부 자료 열람 권한은 원래 서비스의 설정을 따름
- 원문 일부의 -> h 표기와 반복된 워크숍 링크는 의미를 추정해 바꾸지 않음

[GitHub Pages 공식 게시 설정 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)


## 2026-09-18 수정

하단 배너는 영문 연구실 이름과 설명만 표시합니다. AQFC 사진 4장을 추가했으며 단체사진을 대표로 사용합니다. Projects의 로고와 Publications의 Refereeing service를 제거했습니다.
Submitted 논문은 세부 연구 분야 구분 없이 하나의 목록으로 표시합니다.

홈의 Our research 소개 문단만 한·영 병기를 유지하고 나머지 화면은 영어를 기본으로 합니다. 영문 표기가 확인되지 않은 졸업생 인명과 원본 사진 속 글자는 그대로 보존합니다.


## Google Analytics

`content/site.json`의 `google_analytics_measurement_id`로 GA4 측정 ID를 관리합니다. 현재 ID는 `G-ZN51HGJ61H`입니다. 값을 비우면 추적 코드를 생성하지 않습니다.

빌드 시 모든 페이지에 Google 태그가 한 번씩 삽입됩니다. `huhjeonggyu.github.io`에서만 로드하며 로컬 미리보기에서는 전송하지 않습니다. GA4의 기본 page_view를 사용하므로 별도의 page_view 이벤트를 중복 전송하지 않습니다.

도메인이 바뀌면 `scripts/build.py`의 Analytics 호스트 조건도 변경해야 합니다. 설치 후 Google Analytics의 실시간 보고서에서 수집 여부를 확인할 수 있습니다.


## Research overview

Research는 경로 미분을 이용한 국소 제어 복원, OL-BPTT/PMP와 CL-BPTT/HJB, 정책 갱신 연산자, 문제별 확장과 한계를 중심으로 구성합니다. 본문과 도식은 `content/pages/research.json`, 전용 스타일은 `assets/research.css`에서 관리합니다.

Research의 두 수식은 MathJax 4.0.0으로 표시하며 해당 페이지에서만 불러옵니다. 원본 수식 이미지는 변경하지 않았고, 이전 BPTT 기술 노트는 Research 하단의 Earlier technical material에서 접근할 수 있습니다.
