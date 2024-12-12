import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import matplotlib.font_manager as fm
from matplotlib.ticker import FixedFormatter, FixedLocator

if __name__ == "__main__":
    # 한국어 폰트 설정
    font_path = 'malgunsl.ttf'  # 폰트 파일 경로
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)

    # CSV 파일 읽기
    park_data = pd.read_csv('NLPRK_STA.csv', encoding='cp949')

    data_points = park_data.iloc[:, [1, 2]].values
    num_data_points = data_points.shape[0]  # 데이터 개수
    num_features = data_points.shape[1]  # 데이터 차원 (2차원: 육지면적, 탐방객수)

    k = 3  # 클러스터 개수
    interation = 100  # 반복 횟수

    cluster_centers = np.array([]).reshape(num_features, 0)
    for i in range(k):
        random_index = rd.randint(0, num_data_points - 1)
        cluster_centers = np.c_[cluster_centers, data_points[random_index]]

    # 클러스터링 수행
    clustering_result = {}
    for iteration in range(interation):
        # 유클리드 거리 계산
        distances_to_centers = np.array([]).reshape(num_data_points, 0)
        for cluster_index in range(k):
            distance = np.sum((data_points - cluster_centers[:, cluster_index]) ** 2, axis=1)
            distances_to_centers = np.c_[distances_to_centers, distance]

        # 각 데이터 포인트를 가장 가까운 클러스터에 할당
        cluster_assignments = np.argmin(distances_to_centers, axis=1) + 1

        cluster_data = {}
        for cluster_index in range(k):
            cluster_data[cluster_index + 1] = np.array([]).reshape(2, 0)
        for point_index in range(num_data_points):
            cluster_data[cluster_assignments[point_index]] = np.c_[
                cluster_data[cluster_assignments[point_index]], data_points[point_index]
            ]
        for cluster_index in range(k):
            cluster_data[cluster_index + 1] = cluster_data[cluster_index + 1].T

        for cluster_index in range(k):
            cluster_centers[:, cluster_index] = np.mean(cluster_data[cluster_index + 1], axis=0)

        clustering_result = cluster_data

    # 클러스터링 결과 시각화
    cluster_colors = ['green', 'blue', 'red']
    cluster_labels = ['Cluster 1', 'Cluster 2', 'Cluster 3']

    for cluster_index in range(k):
        if len(clustering_result[cluster_index + 1]) > 0:  # 클러스터가 비어있지 않은 경우만 시각화
            plt.scatter(
                clustering_result[cluster_index + 1][:, 0],
                clustering_result[cluster_index + 1][:, 1],
                c=cluster_colors[cluster_index],
                label=cluster_labels[cluster_index]
            )
    plt.scatter(
        cluster_centers[0, :],
        cluster_centers[1, :],
        s=300,
        c='yellow',
        label='Centroids'
    )  # 클러스터 중심 표시

    y_ticks = np.arange(0, np.max(data_points[:, 1]) + 1000000, 1000000)  # 1,000,000 단위로 눈금 설정
    plt.gca().yaxis.set_major_locator(FixedLocator(y_ticks))
    plt.gca().yaxis.set_major_formatter(FixedFormatter([str(int(val)) for val in y_ticks]))

    plt.xlabel('육지면적 (㎢)')  # x축은 육지면적
    plt.ylabel('탐방객수 (명)')  # y축은 탐방객수
    plt.grid(True)
    plt.legend()
    plt.show()