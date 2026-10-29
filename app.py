import streamlit as st
import pandas as pd

st.set_page_config(page_title="온라인 사업 추천기", page_icon="💡", layout="wide")

# ------------------------------------------------------------------
# 데이터: 사업을 추가/수정하려면 이 리스트만 고치면 됩니다.
# 수익은 '시작 후 6개월~1년 이후 현실적인 범위(만원/월)'의 대략적인 추정치입니다.
# ------------------------------------------------------------------
BUSINESSES = [
    {
        "name": "블로그 · 애드센스/체험단",
        "emoji": "✍️",
        "summary": "정보성 글을 꾸준히 올려 광고 수익과 체험단·제휴 수익을 얻는 사업",
        "difficulty": 2,
        "cost": 0,
        "months": "3~6개월",
        "income_low": 0,
        "income_high": 100,
        "skills": ["글쓰기", "검색 키워드 분석", "꾸준함"],
        "tools": ["네이버 블로그", "티스토리", "구글 서치콘솔", "키워드 도구"],
        "steps": [
            "관심 분야 1개 정하기 (IT, 공부법, 리뷰 등)",
            "블로그 플랫폼 선택 (애드센스는 티스토리/워드프레스)",
            "검색 키워드를 조사해서 주 3회 이상 글 작성",
            "방문자가 늘면 애드센스 신청 또는 체험단 지원",
            "인기 글을 분석해 비슷한 주제로 확장",
        ],
        "pros": ["초기 비용 거의 없음", "한번 쓴 글이 계속 수익을 만듦"],
        "cons": ["수익까지 오래 걸림", "초반 몇 달은 수익이 거의 없음"],
        "minor": "애드센스는 만 18세 미만 가입 제한 및 법정대리인 명의 필요가 있을 수 있어요. 정책을 꼭 확인하세요.",
    },
    {
        "name": "유튜브 · 숏폼 채널",
        "emoji": "🎬",
        "summary": "영상 콘텐츠로 조회수 광고, 협찬, 제휴 수익을 만드는 사업",
        "difficulty": 3,
        "cost": 5,
        "months": "6~12개월",
        "income_low": 0,
        "income_high": 200,
        "skills": ["영상 편집", "기획력", "꾸준함"],
        "tools": ["CapCut", "Vrew", "DaVinci Resolve", "YouTube Studio"],
        "steps": [
            "채널 주제와 타깃 시청자 정하기",
            "스마트폰과 무료 편집 앱으로 영상 제작 환경 만들기",
            "주 2~3회 업로드, 첫 3초에 시선을 끄는 구성 연습",
            "조회수·시청 지속 시간 분석해서 반응 좋은 주제 반복",
            "수익화 조건(구독자·시청시간) 달성 후 파트너 프로그램 신청",
        ],
        "pros": ["성공하면 수익 상한이 높음", "협찬·상품 판매로 확장 가능"],
        "cons": ["수익화 조건까지 장벽이 있음", "영상 제작 시간이 많이 듦"],
        "minor": "미성년자는 수익 수령 시 법정대리인 동의·계좌 확인이 필요할 수 있어요.",
    },
    {
        "name": "스마트스토어 · 위탁판매",
        "emoji": "🛒",
        "summary": "재고 없이 상품을 등록하고 주문이 들어오면 도매처가 배송하는 방식",
        "difficulty": 3,
        "cost": 10,
        "months": "2~4개월",
        "income_low": 0,
        "income_high": 300,
        "skills": ["상품 소싱", "상세페이지 제작", "고객 응대(CS)"],
        "tools": ["네이버 스마트스토어", "도매꾹", "도매매", "미리캔버스"],
        "steps": [
            "사업자등록 및 통신판매업 신고 (연령·대리인 조건 확인)",
            "스마트스토어 개설",
            "도매 사이트에서 경쟁이 적은 상품 소싱",
            "상품명 키워드 최적화 + 상세페이지 제작",
            "주문·배송·교환 환불 응대 반복하며 상품 확장",
        ],
        "pros": ["재고 부담이 적음", "시작 속도가 빠름"],
        "cons": ["경쟁이 치열함", "마진이 낮고 CS 스트레스가 있음"],
        "minor": "사업자등록은 만 19세 미만이면 법정대리인 동의 등 추가 절차가 필요해요. 관할 세무서에 확인하세요.",
    },
    {
        "name": "쿠팡파트너스 · 제휴마케팅",
        "emoji": "🔗",
        "summary": "상품 링크를 공유하고 구매가 발생하면 수수료를 받는 방식",
        "difficulty": 2,
        "cost": 0,
        "months": "2~5개월",
        "income_low": 0,
        "income_high": 100,
        "skills": ["콘텐츠 제작", "상품 비교 분석", "SNS/블로그 운영"],
        "tools": ["쿠팡파트너스", "블로그", "인스타그램", "유튜브"],
        "steps": [
            "쿠팡파트너스 가입 및 승인 조건 확인",
            "리뷰·비교 콘텐츠를 올릴 채널(블로그/SNS) 준비",
            "'가성비 OO 추천' 같은 구매 의도가 높은 주제로 콘텐츠 제작",
            "게시물에 파트너스 링크와 필수 고지 문구 삽입",
            "클릭·구매 데이터를 보고 잘 팔리는 카테고리 집중",
        ],
        "pros": ["재고·배송 부담이 없음", "무자본 시작 가능"],
        "cons": ["트래픽이 없으면 수익도 없음", "최종 구매 시 취소되면 수수료도 취소됨"],
        "minor": "수수료 고지 문구 의무가 있으며, 가입 연령과 정산 조건은 약관을 확인하세요.",
    },
    {
        "name": "전자책 · 온라인 강의",
        "emoji": "📚",
        "summary": "내가 가진 지식과 노하우를 콘텐츠로 만들어 판매하는 사업",
        "difficulty": 3,
        "cost": 3,
        "months": "2~4개월",
        "income_low": 0,
        "income_high": 150,
        "skills": ["전문 지식", "콘텐츠 구성력", "마케팅"],
        "tools": ["크몽", "탈잉", "클래스101", "노션", "Canva"],
        "steps": [
            "남들이 돈 내고 배울 만한 주제 찾기 (공부법, 코딩, 디자인 등)",
            "목차를 먼저 설계하고 샘플 챕터 제작",
            "노션 또는 PDF로 전자책 완성",
            "크몽·스토어 등에 등록하고 상세 설명 작성",
            "후기와 피드백으로 내용을 개선해 업데이트",
        ],
        "pros": ["한번 만들면 반복 판매 가능", "마진이 높음"],
        "cons": ["신뢰와 실적이 없으면 팔기 어려움", "초기 마케팅이 필요함"],
        "minor": "플랫폼별로 판매자 가입 연령 제한이 있을 수 있어요.",
    },
    {
        "name": "프리랜서 · 개발/디자인 외주",
        "emoji": "💻",
        "summary": "코딩, 디자인, 영상 편집 등 기술을 의뢰인에게 직접 판매",
        "difficulty": 4,
        "cost": 0,
        "months": "1~3개월",
        "income_low": 20,
        "income_high": 300,
        "skills": ["프로그래밍/디자인 실력", "커뮤니케이션", "일정 관리"],
        "tools": ["크몽", "숨고", "GitHub", "Notion"],
        "steps": [
            "자신 있는 기술 1~2개 정하기 (예: Python 자동화, 크롤링, 데이터 분석)",
            "포트폴리오를 GitHub와 노션에 정리",
            "크몽·숨고에 서비스 등록 (저렴한 가격으로 후기부터 확보)",
            "의뢰 상담 → 견적 → 납품 → 수정 과정 반복",
            "후기가 쌓이면 가격 인상 및 전문 분야 집중",
        ],
        "pros": ["빠르게 수익 가능", "실력과 포트폴리오가 곧 커리어가 됨"],
        "cons": ["시간을 팔아야 해서 확장이 어려움", "납기와 수정 요청 스트레스"],
        "minor": "미성년자는 계약·정산에 법정대리인 동의가 필요할 수 있어요.",
    },
    {
        "name": "AI 활용 콘텐츠 · 자동화 서비스",
        "emoji": "🤖",
        "summary": "AI 도구로 콘텐츠를 제작하거나 업무 자동화를 대행하는 사업",
        "difficulty": 3,
        "cost": 3,
        "months": "1~4개월",
        "income_low": 0,
        "income_high": 200,
        "skills": ["프롬프트 작성", "자동화 도구 활용", "기획력"],
        "tools": ["Claude", "ChatGPT", "Zapier/Make", "Canva", "Python"],
        "steps": [
            "AI로 해결 가능한 문제 찾기 (블로그 글 초안, 상세페이지, 데이터 정리 등)",
            "반복 업무를 자동화하는 간단한 프로토타입 제작",
            "크몽·SNS에 샘플 결과물과 함께 서비스 소개",
            "소규모 사업자 대상으로 첫 의뢰 확보",
            "결과물 품질 검수 프로세스를 만들어 신뢰 쌓기",
        ],
        "pros": ["진입장벽이 낮고 성장 중인 시장", "AI·데이터 진로와 연결됨"],
        "cons": ["경쟁자가 빠르게 늘고 있음", "AI 결과물 검수·저작권 이슈 주의"],
        "minor": "AI 생성물의 저작권·이용약관을 확인하고, 결과물은 반드시 직접 검수하세요.",
    },
]

DIFFICULTY_LABEL = {1: "매우 쉬움", 2: "쉬움", 3: "보통", 4: "어려움", 5: "매우 어려움"}


def stars(n: int) -> str:
    return "⭐" * n + "☆" * (5 - n)


def to_df(items):
    return pd.DataFrame(
        {
            "사업": [f'{b["emoji"]} {b["name"]}' for b in items],
            "난이도": [b["difficulty"] for b in items],
            "초기비용(만원)": [b["cost"] for b in items],
            "수익까지": [b["months"] for b in items],
            "월 최소(만원)": [b["income_low"] for b in items],
            "월 최대(만원)": [b["income_high"] for b in items],
        }
    )


# ------------------------------------------------------------------
# 사이드바: 조건 필터
# ------------------------------------------------------------------
st.sidebar.header("🔍 내 조건 고르기")
max_cost = st.sidebar.slider("감당 가능한 초기 비용 (만원)", 0, 50, 10, step=1)
max_diff = st.sidebar.slider("감당 가능한 난이도", 1, 5, 4)
sort_by = st.sidebar.radio("정렬 기준", ["난이도 낮은 순", "예상 최대 수익 높은 순", "초기 비용 낮은 순"])

filtered = [b for b in BUSINESSES if b["cost"] <= max_cost and b["difficulty"] <= max_diff]

if sort_by == "난이도 낮은 순":
    filtered.sort(key=lambda b: b["difficulty"])
elif sort_by == "예상 최대 수익 높은 순":
    filtered.sort(key=lambda b: b["income_high"], reverse=True)
else:
    filtered.sort(key=lambda b: b["cost"])

# ------------------------------------------------------------------
# 메인 화면
# ------------------------------------------------------------------
st.title("💡 온라인 사업 추천기")
st.caption("조건에 맞는 온라인 사업을 추천하고, 시작 방법과 예상 수익을 알려드려요.")

if not filtered:
    st.warning("조건에 맞는 사업이 없어요. 왼쪽에서 비용이나 난이도 조건을 완화해 보세요.")
    st.stop()

st.subheader(f"추천 결과: {len(filtered)}개")
df = to_df(filtered)
st.dataframe(df, use_container_width=True, hide_index=True)

chart_df = df.set_index("사업")[["월 최대(만원)"]]
st.bar_chart(chart_df)

st.divider()

# ------------------------------------------------------------------
# 사업 상세
# ------------------------------------------------------------------
names = [f'{b["emoji"]} {b["name"]}' for b in filtered]
choice = st.selectbox("📌 자세히 알아볼 사업을 골라보세요", names)
biz = filtered[names.index(choice)]

st.header(f'{biz["emoji"]} {biz["name"]}')
st.write(biz["summary"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("난이도", f'{biz["difficulty"]}/5', DIFFICULTY_LABEL[biz["difficulty"]], delta_color="off")
c2.metric("초기 비용", f'{biz["cost"]}만원 이하')
c3.metric("수익까지", biz["months"])
c4.metric("예상 월수익", f'{biz["income_low"]}~{biz["income_high"]}만원')

tab1, tab2, tab3, tab4 = st.tabs(["🚀 시작 방법", "💰 수익 정보", "⚖️ 장단점", "⚠️ 주의사항"])

with tab1:
    st.subheader("시작 순서")
    for i, step in enumerate(biz["steps"], start=1):
        st.markdown(f"**{i}단계.** {step}")
    st.subheader("필요한 역량")
    st.write(" · ".join(biz["skills"]))
    st.subheader("추천 도구/플랫폼")
    st.write(" · ".join(biz["tools"]))

with tab2:
    st.subheader("예상 수익 범위")
    st.write(f'시작 후 {biz["months"]} 지나면 월 **{biz["income_low"]}~{biz["income_high"]}만원** 정도를 목표로 볼 수 있어요.')
    st.info("실제 수익은 노력, 시간, 운, 시장 상황에 따라 크게 달라요. 위 수치는 참고용 추정치입니다.")
    hours = st.slider("주당 투자 가능 시간", 1, 30, 7)
    price_factor = min(hours / 10, 1.5)
    est_low = int(biz["income_low"] * price_factor)
    est_high = int(biz["income_high"] * price_factor)
    st.metric("내 투자 시간 기준 예상 월수익(대략)", f"{est_low}~{est_high}만원")

with tab3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("👍 장점")
        for p in biz["pros"]:
            st.success(p)
    with col_b:
        st.subheader("👎 단점")
        for c in biz["cons"]:
            st.error(c)

with tab4:
    st.warning(biz["minor"])
    st.markdown(
        "- 수익이 발생하면 세금(종합소득세 등) 신고 의무가 생길 수 있어요.\n"
        "- '무조건 수익 보장' 같은 광고는 사기일 가능성이 높아요.\n"
        "- 미성년자는 계약, 정산, 사업자등록에 법정대리인 동의가 필요할 수 있어요."
    )

st.divider()
st.caption("※ 본 앱의 수익·비용 수치는 참고용 추정치이며, 실제 결과를 보장하지 않습니다.")
