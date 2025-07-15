from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pandas as pd

# 예제 데이터 (관광지명, 주소, 업무명, 위도, 경도)
data = [
    {"place": "경복궁", "address": "서울 종로구 사직로 161", "job": "입장 안내", "lat": 37.579617, "lon": 126.977041},
    {"place": "남산타워", "address": "서울 용산구 남산공원길 105", "job": "기념품 판매", "lat": 37.551169, "lon": 126.988227},
    {"place": "부산 해운대", "address": "부산 해운대구 우동", "job": "해변 청소", "lat": 35.158698, "lon": 129.160384},
]

df = pd.DataFrame(data)


# 사용자 입력 처리
def find_nearby_jobs(user_input):
    geolocator = Nominatim(user_agent="tourism-job-finder")
    location = geolocator.geocode(user_input)

    if location is None:
        return "입력한 장소를 찾을 수 없습니다."

    user_coord = (location.latitude, location.longitude)

    # 거리 계산
    df['distance_km'] = df.apply(
        lambda row: geodesic(user_coord, (row['lat'], row['lon'])).kilometers, axis=1
    )

    # 거리순 정렬
    sorted_df = df.sort_values(by='distance_km')

    # 결과 출력
    results = []
    for _, row in sorted_df.iterrows():
        results.append(f"{row['place']} - {row['job']} ({row['distance_km']:.2f} km)")

    return results


# 사용 예시
if __name__ == "__main__":
    user_input = input("관광지명 또는 주소를 입력하세요: ")
    results = find_nearby_jobs(user_input)

    print("\n가까운 업무 목록:")
    if isinstance(results, list):
        for r in results:
            print(" -", r)
    else:
        print(results)
