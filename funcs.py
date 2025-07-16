import requests
import openai
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pandas as pd

imgs = {
    "해운대 해수욕장":"https://i.namu.wiki/i/hkDOgJHC40yiIFKQDRz7YjHpzWrL9vCTT7mve4TF6Lj-GpGsBpvT8WlXbwOT_To1Ndl1zKrVLQ-SiwaGNFOgQA.webp",
    "용평 모나 리조트":"https://i.namu.wiki/i/3oOpb1tw8p7dNRjdCmu0_LlkJbESn0jIcInMO-uX7VfkqXZDskgFN7YFD8MuvlRVJVGj-tswmkzUdAZVBtHUVA.webp",
    "남산타워":"https://i.namu.wiki/i/DK-BcaE6wDCM-N9UJbeQTn0SD9eWgsX9YKWK827rqjbrzDz0-CxW-JFOCiAsUL3CBZ4zE0UDR-p4sLaYPiUjww.webp",
    "제주도":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Jeju_Island.jpg/250px-Jeju_Island.jpg",
    "주차 안내원":"https://newsimg.sedaily.com/2016/11/03/1L3TT6196V_1.jpg",
    "인형탈 알바":"https://1.bp.blogspot.com/-GJxs0OHKNro/XRq3yEbc5tI/AAAAAAAACeE/tPS7Lj2gmUMeOLSc6wYJ9-CM2N8tXKjVQCLcBGAs/s1600/9.gif",
    "탭댄서":"https://dimg.donga.com/wps/NEWS/IMAGE/2021/07/12/107921227.1.jpg",
    "바텐더":"https://www.drinkmagazine.asia/wp-content/uploads/2001/10/web-ounce.jpg"
}

def html_page(
        active_nav_index,title,subtitle,comment,
        location_a, location_b, location_c, location_d,
        place_a, place_b, place_c, place_d
):
    search_adress = "/search_travel"
    if active_nav_index == 0:
        active_a = 'class="active"'
        active_b = ''
        search_adress = "/search_travel"
    else:
        active_a = ''
        active_b = 'class="active"'
        search_adress = "/search_job"

    image_url_a = get_image_urls(place_a)[0]
    image_url_b = get_image_urls(place_b)[0]
    image_url_c = get_image_urls(place_c)[0]
    image_url_d = get_image_urls(place_d)[0]


    return """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>관광지 검색</title>
  <style>
    html, body {
      touch-action: manipulation;
    }
    body {
      background-color: #ffffff;
      color: #000;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      margin: 0;
      font-family: sans-serif;
      padding-bottom: 60px;
    }
    header {
      text-align: center;
      padding: 1.5rem 0 0 0; /* 하단 패딩 제거 */
    }
    header h1 {
      font-size: 1.875rem;
      font-weight: bold;
      margin-bottom: 5px;

    }
    header p {
      color: #9ca3af;
      margin-top: 0px;
      margin-bottom: 20px;
    }
    .search-box {
      display: flex;
      align-items: center;
      background-color: #ffffff;
      border-radius: 9999px;
      padding: 0.5rem 1rem;
      margin: 0.5rem auto 0 auto;
      max-width: 500px;
      width: 90%;
      box-sizing: border-box;
      outline: 2px solid black;
    }

    .search-box svg {
      width: 1.25rem;
      height: 1.25rem;
      color: #9ca3af;
      margin-right: 0.5rem;
    }
    .search-box input {
      background-color: #ffffff;
      color: #000000;
      border: none;
      outline: none;
      width: 100%;
      font-size: 1rem;
    }
    .recommend-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1rem;
      margin-top: 0;
    }
    section h2 {
      color: black;
      font-size: 1.8rem;
      font-weight: 600;
      margin-bottom: 5px;
    }
    .tour-list {
      padding: 0 1rem;
      margin-top: 0.5rem;
    }
    .tour-item {
      position: relative;
      width: 100%;
      height: 8rem;
      border-radius: 0.75rem;
      overflow: hidden;
      margin-bottom: 1rem;
      background-size: 100% auto;
      background-repeat: no-repeat;
      background-position: center center;
    }
    .tour-item:last-child {
      margin-bottom: 0;
    }
    .tour-item img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center center;
      display: block;
    }
    .tour-item-overlay {
      position: absolute;
      inset: 0;
      background-color: rgba(0, 0, 0, 0.4);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      padding: 1rem;
    }
    .tour-item-overlay h3 {
      font-size: 1.5rem;
      font-weight: bold;
      color: white;
    }
    .tour-item-overlay p {
      font-size: 0.875rem;
      color: #d1d5db;
      margin-top: 0.25rem;
    }
    nav {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      background-color: #111827;
      display: flex;
      justify-content: space-around;
      align-items: center;
      padding: 0.3rem 0;
    }
    nav button {
      background: none;
      border: none;
      display: flex;
      flex-direction: column;
      align-items: center;
      color: #9ca3af;
      cursor: pointer;
      padding: 1rem 2rem;
      border-radius: 0.75rem;
    }
    nav button.active {
      color: #fff;
    }
    nav svg {
      width: 1.5rem;
      height: 1.5rem;
      margin-bottom: 0.25rem;
    }
    nav span {
      font-size: 0.75rem;
    }
    nav button:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }
  </style>
</head>
<body>
  <header>
    <h1 class="title_text">"""+title+"""</h1>
    <p>"""+subtitle+"""</p>
    <form action="""+search_adress+""" method="get">
      <div class="search-box">
        <svg viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M12.9 14.32a8 8 0 111.414-1.414l4.387 4.387a" clip-rule="evenodd"/>
        </svg>
        <input type="text" name="query" placeholder="검색하려면 여기를 누르세요" />
      </div>
    </form>
  </header>
  <section class="recommend-header">
    <h2>"""+comment+"""</h2>
  </section>

  <section class="tour-list">
    <button class="tour-item" style="background-image: url('"""+image_url_a+"""');">
      <div class="tour-item-overlay">
        <h3>"""+location_a+"""</h3>
        <p>"""+place_a+"""</p>
      </div>
    </button>
    <button class="tour-item" style="background-image: url('"""+image_url_b+"""');">
      <div class="tour-item-overlay">
        <h3>"""+location_b+"""</h3>
        <p>"""+place_b+"""</p>
      </div>
    </button>
    <button class="tour-item" style="background-image: url('"""+image_url_c+"""');">
      <div class="tour-item-overlay">
        <h3>"""+location_c+"""</h3>
        <p>"""+place_c+"""</p>
      </div>
    </button>
    <button class="tour-item" style="background-image: url('"""+image_url_d+"""');">
      <div class="tour-item-overlay">
        <h3>"""+location_d+"""</h3>
        <p>"""+place_d+"""</p>
      </div>
    </button>
  </section>

  <nav>
    <form action="/travel" method="post">
      <button """+active_a+""">
        <svg fill="currentColor" viewBox="0 0 20 20">
          <path d="M5.05 4.05a7 7 0 019.9 0l.94.94a7 7 0 010 9.9l-.94.94a7 7 0 01-9.9 0l-.94-.94a7 7 0 010-9.9l.94-.94zM10 8a2 2 0 100 4 2 2 0 000-4z"/>
        </svg>
        <span>관광지 검색</span>
      </button>
    </form>
    <form action="/job" method="post">
      <button """+active_b+""">
        <svg fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 2a8 8 0 00-5.293 13.707l-1.414 1.414a1 1 0 001.414 1.414l1.414-1.414A8 8 0 1010 2zm1 11H9v-2h2v2zm0-4H9V5h2v4z" clip-rule="evenodd"/>
        </svg>
        <span>직업 검색</span>
      </button>
    </form>
  </nav>
</body>
</html>
"""

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
model = "gpt-4"

def gpt_request(query):
    try:
        messages = [{
            "role": "system",
            "content": """
             너는 특정 지역에 대한 관광 쏠림 현상과 관광지의 환경 오염 문제 및 사회 문제를 해결하기 위한 대책으로 개발된 지속 가능한 관광 일정 자동 생성
            어플의 시스템 일부야. 너는 입력된 값을 보고 사용자가 어떤 위치, 어떤 관광지를 찾는지 판단한 뒤 여행 일정을 작성해야해. 여행 일정은 json형태로
            다음과 같은 서식을 갖추고 있어.

            {
              "location": "여행지 주소",
              "location_name": "여행지 이름",
              "schedule_day1": ["일정1","일정2","일정3"],
              "schedule_day1_info": {
                "day_start": ["일정 시작 시간","조식 여부"],
                "일정1": ["일정 시간","입장료 및 음식점이라면 인당 예상 식비 등"],
                "일정2": ["일정 시간","입장료 및 음식점이라면 인당 예상 식비 등"],
                "일정3": ["일정 시간","입장료 및 음식점이라면 인당 예상 식비 등"],
                "day_end": ["일정 종료 시간","석식 여부"]
              },
              "schedule_day2": ["일정1","일정2","일정3"],
              "schedule_day2_info": {
                "day_start": ["일정 시작 시간","조식 여부"],
                "일정1": ["일정 시간","입장료 및 음식점이라면 인당 예상 식비 등"],
                "일정2": ["일정 시간","입장료 및 음식점이라면 인당 예상 식비 등"],
                "일정3": ["일정 시간","입장료 및 음식점이라면 인당 예상 식비 등"],
                "day_end": ["일정 종료 시간","석식 여부"]
              },
              "hotel" : "호텔 이름",
              "hotel_location" : "호텔 주소",
              "traffic_cost": "교통수단 사용시 예상 청구 요금",
              "fuel_cost": "차량 사용시 기름값 예상 금액"
              "goal":"이 여행지가 지속가능한 관광지로 선택된 이유"
            }

            너는 반드시 위의 서식에 맞춘 답만 말해야하며, 이 외에의 말을 할 경우 프로그램에 오류가 발생함을 항시 유의해야해.
            호텔 이름은 다른 호텔과 구별할 수 있는 짧은 호텔 이름으로, 호텔 주소는 최대한 자세하게 기입하며,
            찾을 수 없는 정보는 '알 수 없음'으로 표기하도록 해.
            석식 여부 및 조식 여부는 있다면 boolean값으로 True, 아니라면 boolean값으로 False를 기입하고, 
            여행지 주소는 국내로 하며 국가이름은 기입 금지, ~도 ~시 또는 ~군 또는 ~읍까지 기입해.
            여행지 주소 예시) 경기도 용인시
            그리고 여행지 이름은 이 여행일정의 대표 일정을 기입해.
            입장료 및 음식점이라면 인당 예상 식비 등을 입력할 때는 가격 정보만 입력하며, 무료라면 '무료'를 기입하고, 유료라면 ','표시를 포함한 정수값으로 기입해.

            [ 주의사항 ]
            1.절대 json외의 어떤 텍스트도 출력하지마
            2.일정 생성에 실패하지마. 만일 못하겠다면 다시 한번 생각해봐.
            3.절대 서식에서 단 한개의 사항도 누락하지마.
            4.모든 생각은 논리적으로 진행해
            5.숙소는 호텔 또는 모텔만 가능해. 이외의 어떤 곳도 숙소로 선정하지마.
            """
        }, {
            "role": "user",
            "content": query
        }]
        response = openai.chat.completions.create(model=model, messages=messages)
        answer = response.choices[0].message.content
        return answer
    except:
        print("Error[gpt_request]")
        return False

GOOGLE_API = "AIzaSyA8urcQxk_yVkDnoOws1NU6m-9FTbptgBA"
CX = "2116b8901748b4bff"
def get_image_urls(place_name):
    if not place_name in imgs:
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": place_name,
            "key": GOOGLE_API,
            "cx": CX,
            "searchType": "image",
            "num": 1
        }

        response = requests.get(search_url, params=params)
        results = response.json()

        image_urls = []
        if "items" in results:
            for item in results["items"]:
                image_urls.append(item["link"])

        imgs[place_name] = image_urls[0]

        return image_urls
    else:
        print(imgs[place_name])
        return [imgs[place_name]]

def add_job():
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>관광지 아르바이트 등록</title>
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      font-family: Arial, sans-serif;
      background-color: #e6f2ff;
      margin: 0;
      padding: 20px;
    }

    h1 {
      text-align: center;
      color: #333;
      font-size: 1.8em;
    }

    form {
      max-width: 500px;
      margin: 0 auto;
      padding: 20px;
      background-color: #ffffff;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
    }

    input[type="text"] {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 1em;
    }

    button {
      margin-top: 20px;
      width: 100%;
      padding: 12px;
      background-color: #007acc;
      color: white;
      border: none;
      border-radius: 5px;
      font-size: 1em;
    }

    button:hover {
      background-color: #005f99;
    }
  </style>
</head>
<body>

  <h1>관광지 아르바이트 등록</h1>

  <form id="job-form">
    <label for="place">관광지 명칭 *</label>
    <input type="text" id="place" name="place" required>

    <label for="address">주소 *</label>
    <input type="text" id="address" name="address" required>

    <label for="job">업무 이름 *</label>
    <input type="text" id="job" name="job" required>

    <button type="submit">등록하기</button>
  </form>

  <script>
    document.getElementById("job-form").addEventListener("submit", function(event) {
      event.preventDefault(); // 기본 제출 막기

      const place = encodeURIComponent(document.getElementById("place").value.trim());
      const address = encodeURIComponent(document.getElementById("address").value.trim());
      const job = encodeURIComponent(document.getElementById("job").value.trim());

      // 입력값이 비어있는지 확인
      if (!place || !address || !job) {
        alert("모든 항목을 입력해주세요.");
        return;
      }

      const redirectUrl = `/submit_job/${place}/${address}/${job}`;
      window.location.href = redirectUrl; // URL로 이동
    });
  </script>

</body>
</html>
"""

def loading_page():
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>로딩 중</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html, body {
      height: 100%;
      background: linear-gradient(135deg, #f0f4f8, #ffffff);
      font-family: 'Poppins', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .loader-wrapper {
      background: rgba(255, 255, 255, 0.25);
      box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border-radius: 20px;
      padding: 40px 30px;
      text-align: center;
      width: 90%;
      max-width: 280px;
      min-width: 160px;
    }

    .dots {
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 20px;
    }

    .dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background-color: black;
      animation: bounce 1.4s infinite ease-in-out;
    }

    .dot:nth-child(2) {
      animation-delay: 0.2s;
    }

    .dot:nth-child(3) {
      animation-delay: 0.4s;
    }

    @keyframes bounce {
      0%, 80%, 100% {
        transform: translateY(0);
        opacity: 0.6;
      }
      40% {
        transform: translateY(-12px);
        opacity: 1;
      }
    }

    .loading-text {
      font-size: 16px;
      font-weight: 500;
      color: #333;
      letter-spacing: 0.5px;
      white-space: nowrap;
    }
  </style>
</head>
<body>
  <div class="loader-wrapper">
    <div class="dots">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
    <div class="loading-text">일정 생성중..</div>
  </div>
</body>
</html>

    """

def schedule(query):

    print("스케줄 불러오는중")
    schedule_json = gpt_request(query)

    if not schedule_json == "False" or not schedule_json == False:
        print("스케줄 로드됨")
    else:
        return False

    return """
    <!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>여행 일정</title>
  <style>
    :root {
      --primary-color: black;
      --background-color: #ffffff;
    }

    body {
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      padding: 0;
      background-color: var(--background-color);
      color: #333;
    }

    #back-button {
      position: fixed;
      top: 16px;
      left: 16px;
      padding: 10px 16px;
      font-size: 14px;
      background-color: var(--primary-color);
      color: white;
      border: none;
      border-radius: 8px;
      z-index: 100;
    }

    .loading-screen {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      font-weight: bold;
      z-index: 1000;
    }

    .timeline-container {
      max-width: 100%;
      padding: 70px 16px 16px;
    }

    .day-section {
      margin-bottom: 32px;
    }

    .day-title {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 12px;
      color: var(--primary-color);
    }

    .timeline {
      border-left: 2px solid var(--primary-color); /* 막대기 형태 유지 */
      padding-left: 16px;
      position: relative;
    }

    .timeline-item {
      margin-bottom: 24px;
      padding-left: 4px;
      position: relative;
    }

    /* 둥근 원 제거 */
    .timeline-item::before {
      display: none;
    }

    .timeline-time {
      display: block;
      font-weight: bold;
      font-size: 15px;
      color: #222;
      margin-bottom: 4px;
    }

    .timeline-desc {
      display: block;
      font-size: 14px;
      margin-left: 0;
      line-height: 1.5;
      word-break: keep-all;
    }


    .info-box {
      margin: 20px 0;
      padding: 16px;
      background-color: #f2f8ff;
      border: 1px solid #d0e6ff;
      border-radius: 12px;
    }

    .info-box h3 {
      margin-top: 0;
      color: var(--primary-color);
      font-size: 18px;
    }

    .info-box p {
      margin: 8px 0;
      font-size: 15px;
      line-height: 1.4;
    }

    @media (min-width: 600px) {
      .timeline-container {
        max-width: 500px;
        margin: auto;
      }
    }
  </style>
</head>
<body>
  <a href="/">
    <button id="back-button">← 뒤로가기</button>
  </a>
  <div class="timeline-container" id="timeline"></div>
  <div class="timeline-container">
    <div class="info-box" id="info-box"></div>
  </div>

  <script>
    const data = """+schedule_json+""";

    function createDayTimeline(day, schedule, info) {
      let html = `<div class="day-section"><div class="day-title">${day}</div><div class="timeline">`;
      html += `<div class="timeline-item"><div class="timeline-time">시작 (${info.day_start[0]})</div><div class="timeline-desc">조식 여부: ${info.day_start[1]}</div></div>`;
      for (let item of schedule) {
        const [time, cost] = info[item];
        html += `<div class="timeline-item"><div class="timeline-time">${time}</div><div class="timeline-desc">${item} (${cost})</div></div>`;
      }
      html += `<div class="timeline-item"><div class="timeline-time">종료 (${info.day_end[0]})</div><div class="timeline-desc">석식 여부: ${info.day_end[1]}</div></div>`;
      html += `</div></div>`;
      return html;
    }

    window.onload = () => {
      const container = document.getElementById('timeline');
      const day1 = createDayTimeline("Day 1", data.schedule_day1, data.schedule_day1_info);
      const day2 = createDayTimeline("Day 2", data.schedule_day2, data.schedule_day2_info);
      container.innerHTML = `<h2 style="text-align:center; color: var(--primary-color); margin-bottom: 24px;">${data.location_name} 일정</h2>${day1}${day2}`;

      const infoBox = document.getElementById('info-box');
      infoBox.innerHTML = `
        <h3>여행 정보 요약</h3>
        <p><strong>숙소:</strong> ${data.hotel} (${data.hotel_location})</p>
        <p><strong>교통비:</strong> ${data.traffic_cost}</p>
        <p><strong>유류비:</strong> ${data.fuel_cost}</p>
        <p><strong>지속가능성 이유:</strong><br>${data.goal}</p>
      `;

      document.getElementById('loading').style.display = 'none';
    };
  </script>
</body>
</html>

    """

def add_job_success():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>등록 완료</title>
      <style>
        * {
          box-sizing: border-box;
        }
        body {
          font-family: Arial, sans-serif;
          background-color: #f0f8ff;
          margin: 0;
          padding: 20px;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
        }

        .container {
          background-color: white;
          padding: 30px;
          border-radius: 12px;
          box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
          text-align: center;
          max-width: 400px;
          width: 100%;
        }

        h1 {
          font-size: 1.8em;
          color: #007acc;
        }

        p {
          margin-top: 10px;
          color: #333;
        }

        .buttons {
          margin-top: 30px;
          display: flex;
          justify-content: space-between;
          gap: 10px;
        }

        .buttons a {
          flex: 1;
          text-align: center;
          padding: 12px;
          text-decoration: none;
          color: white;
          background-color: #007acc;
          border-radius: 8px;
          font-weight: bold;
          transition: background-color 0.2s;
        }

        .buttons a:hover {
          background-color: #005f99;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>업무 정보 등록 완료</h1>
        <p>새로운 관광지 아르바이트 정보가 성공적으로 등록되었습니다!</p>

        <div class="buttons">
          <a href="/">홈으로</a>
          <a href="/job_add">더 추가하기</a>
        </div>
      </div>
    </body>
    </html>
    """

def add_job_fail():
    return """
    <!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>등록 실패</title>
  <style>
    * {
      box-sizing: border-box;
    }
    body {
      font-family: Arial, sans-serif;
      background-color: #fff5f5;
      margin: 0;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    .container {
      background-color: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      text-align: center;
      max-width: 400px;
      width: 100%;
    }

    h1 {
      font-size: 1.8em;
      color: #d9534f;
    }

    p {
      margin-top: 10px;
      color: #555;
    }

    .buttons {
      margin-top: 30px;
      display: flex;
      justify-content: space-between;
      gap: 10px;
    }

    .buttons a {
      flex: 1;
      text-align: center;
      padding: 12px;
      text-decoration: none;
      color: white;
      background-color: #d9534f;
      border-radius: 8px;
      font-weight: bold;
      transition: background-color 0.2s;
    }

    .buttons a:hover {
      background-color: #c9302c;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>등록 실패</h1>
    <p>위도와 경도를 불러오는데 실패했습니다. 주소를 재확인하고 문제가 해결되지 않는다면 주소 상세하게 입력하지 마십시오.</p>

    <div class="buttons">
      <a href="/">홈으로</a>
      <a href="/job_add">다시 시도하기</a>
    </div>
  </div>
</body>
</html>

    """

def get_lat_lon(address):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def find_nearby_jobs(data, user_input):
    df = pd.DataFrame(data)

    if 'lat' not in df.columns or 'lon' not in df.columns:
        return "입력된 데이터에 'lat' 또는 'lon' 정보가 없습니다."

    # 사용자 주소 -> 좌표 변환
    geolocator = Nominatim(user_agent="tourism-job-finder")
    location = geolocator.geocode(user_input)

    if location is None:
        return "입력한 주소를 찾을 수 없습니다."

    user_coord = (location.latitude, location.longitude)

    try:
        # 거리 계산
        df['distance_km'] = df.apply(
            lambda row: geodesic(user_coord, (row['lat'], row['lon'])).kilometers, axis=1
        )
    except Exception as e:
        return f"거리 계산 중 오류 발생: {e}"

    # 거리순 정렬
    sorted_df = df.sort_values(by='distance_km')

    # 결과 출력
    results = []
    for _, row in sorted_df.iterrows():
        results.append(f"{row['place']} - {row['job']} ({row['distance_km']:.2f} km)")
    return results
