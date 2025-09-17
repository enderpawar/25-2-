def normalize_data(n_cases, n_people, scale):
    norm_cases = []
    # n_cases와 n_people 리스트를 순회하며 계산
    for idx, n in enumerate(n_cases):
        # (해당 지역 확진자 수 / 해당 지역 인구수) * 기준값(scale)
        normalized_value = (n / n_people[idx]) * scale
        norm_cases.append(normalized_value)
    return norm_cases
ㅌ
# 데이터 정의
regions  = ['Seoul', 'Gyeongi', 'Busan', 'Gyeongnam', 'Incheon', 'Gyeongbuk', 'Daegu', 'Chungnam', 'Jeonnam', 'Jeonbuk', 'Chungbuk', 'Gangwon', 'Daejeon', 'Gwangju', 'Ulsan', 'Jeju', 'Sejong']
n_people = [9550227,  13530519, 3359527,     3322373,   2938429,     2630254, 2393626,    2118183,   1838353,   1792476,    1597179,   1536270,  1454679,   1441970, 1124459, 675883,  365309] # 2021-08
n_covid  = [    644,       529,      38,          29,       148,          28,      41,         62,        23,        27,         27,        33,       16,        40,      20,       5,       4] # 2021-09-21

# 전체 인구수, 전체 신규 확진자 수 계산
sum_people = sum(n_people)
sum_covid  = sum(n_covid)

# 인구 100만 당  신규 확진자 수 계산
norm_covid = normalize_data(n_covid, n_people, 1000000)

# 지역별 인구수 출력
print('### Korean Population by Region')
print('* Total population:', sum_people)
print()
print('| Region | Population | Ratio (%) |')
print('| ------ | ---------- | --------- |')
for idx, pop in enumerate(n_people):
    # 전체 인구수 대비 / 해당 지역의 인구 비율 계산
    ratio = (pop / sum_people) * 100
    print('| %s | %d | %.1f |' % (regions[idx], pop, ratio))
print()

# 지역별 COVID-19 신규 확진자 수 출력
print('### Korean COVID-19 New Cases by Region')
print('* Total new cases:', sum_covid)
print()
print('| Region | New Cases | Normalized Cases (per 1M) |')
print('| ------ | --------- | --------------------------- |')
for idx, region in enumerate(regions):
    print('| %s | %d | %.1f |' % (region, n_covid[idx], norm_covid[idx]))
print()
