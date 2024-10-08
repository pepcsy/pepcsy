def read_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue  # 헤더 건너뛰기
            scores = list(map(int, line.strip().split(',')))  # 점수를 정수로 변환
            data.append(scores)  # 데이터를 리스트에 추가
    return data

def calc_weighted_average(data_2d, weight):
    average = []
    for row in data_2d:
        weighted_avg = sum(score * w for score, w in zip(row, weight))
        average.append(weighted_avg)
    return average

def analyze_data(data_1d):
    n = len(data_1d)
    mean = sum(data_1d) / n if n > 0 else 0
    var = sum((x - mean) ** 2 for x in data_1d) / n if n > 0 else 0
    sorted_data = sorted(data_1d)
    mid = n // 2
    median = (sorted_data[mid] + sorted_data[mid - 1]) / 2 if n % 2 == 0 else sorted_data[mid]
    
    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2:  # 'data'가 유효한지 확인
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ------- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')  # 소수점 셋째 자리까지 표시
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average
            }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')  # 소수점 셋째 자리까지 표시
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')
