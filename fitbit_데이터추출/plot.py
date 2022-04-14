import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sj = pd.read_csv("dy2.csv")

#심박수 데이터 확인
sj["ECG_HR"]

#150,000개 == 5분 (1초에 500개 데이터 쌓임 ) (앉아 있기 데이터)
sj_sit = sj[:150000]
sj_sit = sj_sit["ECG_HR"]

#na값 0으로 대체
sj_sit = sj_sit.fillna(0)
sj_sit.isnull().sum()


#5초(2500개 데이터)단위로 평균
HR_list = []
list_500 = []
for i in range(len(sj_sit)):
    if sj_sit[i] !=0:
        list_500.append(sj_sit[i])
    if i % 2500 == 0:        
        HR_list.append(np.mean(list_500))
        list_500 = []        


#길이확인 (5초=60개 : 5분)
len(HR_list)

#그래프
plt.plot(HR_list)


##걷기 데이터
#150,000개 == 5분 (1초에 500개 데이터 쌓임 ) (앉아 있기 데이터)
sj_walk = sj[-150000:]
sj_walk = sj_walk["ECG_HR"]

sj_walk = sj_walk.reset_index(drop = True)


#na값 0으로 대체
sj_walk = sj_walk.fillna(0)
sj_walk.isnull().sum()


#5초(2500개 데이터)단위로 평균
HR_list_wk = []
list_500 = []
for i in range(len(sj_walk)):
    if sj_walk[i] !=0:
        list_500.append(sj_walk[i])
    if i % 2500 == 0:        
        HR_list_wk.append(np.mean(list_500))
        list_500 = []        


#길이확인 (5초=60개 : 5분)
len(HR_list_wk)

#그래프
plt.plot(HR_list_wk)


##fitbit 데이터
import pandas as pd

dy = pd.read_csv("all_intradata_dy.csv")

index_start = dy[dy["time"] == "17:30:01"].index[0]
index_end = dy[dy["time"] == "17:40:56"].index[0]

dy = dy[index_start  : index_end ]

len(dy)

dy = dy.reset_index(drop = True)

list_time = []
for i in range(len(dy)):
    list_time.append(str(dy['time'][i][:-3])) 
    
    
dy['time_cut'] = list_time
    

#예제데이터 생성
sample_data = pd.date_range('2022-04-12 17:30:01', periods=132, freq='5S')

len(sample_data)
dy['time'][0] = str(sample_data[0])[11:]


sample_data_list = []
for i in range(len(sample_data)):
    sample_data_list.append(str(sample_data[i])[11:])
    
    
dy_real = pd.DataFrame({'time' : sample_data_list})


dy_real["value"] = 0


#데이터 채워넣기
for i in range(len(dy_real)):
    for j in range(len(dy)):
        if dy_real["time"][i] == dy["time"][j]:
            dy_real['value'][i] = dy["value"][j]
        
for i in range(len(dy_real)):
    if dy_real['value'][i] == 0:
        dy_real['value'][i] = dy_real['value'][i-1] 


#fitbit 앉기 데이터
dy_sit = dy_real[:60]
#fitbit 걷기 데이터
dy_wk = dy_real[-60:]
dy_wk = dy_wk.reset_index(drop=True)


len(HR_list)        
len(dy_sit)
    
#시각화
plt.plot(HR_list, '-r', label='philips') 
plt.plot(dy_sit['value'], '-b', label='fitbit')
plt.legend()    

plt.plot(HR_list_wk, '-r', label='philips') 
plt.plot(dy_wk['value'], '-b', label='fitbit')
plt.legend()    
