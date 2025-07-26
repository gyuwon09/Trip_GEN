from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from funcs import *
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

jobs = []

@app.get("/", response_class=HTMLResponse)
async def main():
    print("관광지 검색 화면")
    return html_page(
        0,'관광지 검색', '가고싶은 관광 지역을 검색하세요',"관광지 추천",
        '강원도 평창군','충청북도 단양','충청남도 당진','경기도 용인시',
        '모나 용평 리조트', '이끼터널','삽교호 놀이동산','에버랜드',
    )

@app.post("/travel", response_class=HTMLResponse)
async def travel():
    print("관광지 검색 화면")
    return html_page(
        0,'관광지 검색', '가고싶은 관광 지역을 검색하세요','관광지 추천',
        '부산','강원도','서울','제주도',
        '해운대 해수욕장', '용평 모나 리조트','남산타워','제주도'
    )

@app.get("/search_travel", response_class=HTMLResponse)
async def search_travel(request: Request,query: str = ""):
    return templates.TemplateResponse("loading.html", {
        "request": request,
        "redirect_url": f"/schedule_travel/{query}",
        "delay": 0
    })

@app.get("/schedule_travel/{query}",response_class=HTMLResponse)
async def schedule_travel(query):
    return schedule(query)


@app.post("/job", response_class=HTMLResponse)
async def job():
    print("직업 검색 화면")
    return html_page(
        1,'직업 검색', '원하는 일자리나 직군을 검색하세요','가까운 일자리',
        '에버랜드','모나 리조트','강원랜드','홍대 나이트클럽',
        '주차 안내원', '인형탈 알바','탭댄서','바텐더'
    )

@app.get("/job_add", response_class=HTMLResponse)
async def job_add():
    return add_job()

@app.get("/submit_job/{place}/{location}/{job_name}",response_class=HTMLResponse)
async def submit_job(place, location, job_name):

    lat, lon = get_lat_lon(place,location)

    if lat is None or lon is None:
        return add_job_fail()
    else:
        jobs.append({
            "place":place,
            "address":location,
            "job":job_name,
            "lat":lat,
            "lon":lon,
        })
        print(jobs)

        return add_job_success()

@app.get("/search_job")
async def search_travel(request: Request,query: str = ""):
    return templates.TemplateResponse("job_list.html", {"request": request, "results": find_nearby_jobs(jobs,query)})
