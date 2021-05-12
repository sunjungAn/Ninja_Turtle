## 분류 모델
Ninja_turtle에서 거북목 판단을 위한 모델

### 기본 요구사항(ver 1.0) 
+ 초기 모델은 논문에서 사용한 SVM(Support Vector Machine)을 사용
+ GridSearchCV 를 통한 최적 파라미터 찾기
+ 5-Fold 교차 검증
+ Pipeline 구성


### 기본 요구사항(ver 2.0)
+ 시각화를 통한 파라미터 별 성능 비교
+ 여러 알고리즘의 성능 시각화




## Turtle_Model(Ver 2.2)
### - 직접 가공한 4만개의 데이터를 GridSearchCV한 결과 'C = 1, gamma = 100'일 때 가장 높은 정확도를 보여주었다.
### - 아래는 각 파라미터 별 정확도를 시각화 한 것이다.
![SVM 그리드서치 결과](https://user-images.githubusercontent.com/71021694/117926685-1829dc80-b334-11eb-93c2-caa74d795e1a.png)



### Log
+ Ver 1.0 (GridSearchCV를 통한 SVM 파라미터 최적화) - 배은기
+ Ver 1.1 (fit -> trasform 구조를 위한 StandardScaling 및 GridSearchCV을 Pipeline으로 구성) - 배은기
+ Ver 2.1 (matplotlib.pyplot을 이용한 GridSearchCV 출력값 시각화) - 배은기
+ Ver 2.2 직접 모은 약 4만개의 데이터로 GridSearchCV를 한 결과 중 best_estimator를 pkl로 저장 및 시각 - 배은기
