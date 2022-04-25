import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

######다영
sj = pd.read_csv("philips_dy.csv")

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

dy = pd.read_csv("fitbit_dy.csv")

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

#걷기 na 평균으로 대체
HR_list_wk_2 = pd.DataFrame({'value' : HR_list_wk})
HR_list_wk_2= HR_list_wk_2.dropna()


hr_mean = HR_list_wk_2['value'].mean() 


HR_list_wk = pd.DataFrame({'value' : HR_list_wk})
HR_list_wk= HR_list_wk.fillna(0)



HR_list_wk['value'][1]
for i in range(len(HR_list_wk)):
    if HR_list_wk['value'][i] == 0:
        HR_list_wk['value'][i] = hr_mean



plt.plot(HR_list_wk['value'], '-r', label='philips') 
plt.plot(dy_wk['value'], '-b', label='fitbit')
plt.legend()    

######diff 분석


#fitbit 앉기 데이터
dy_sit = dy_real

a_sit = HR_list - dy_sit['value']

a_wk = HR_list_wk['value'] - dy_wk['value']




plt.plot(a_sit)
plt.axhline(0, 60, 0, color='lightgray', linestyle='--', linewidth=2)

plt.plot(a_wk)
plt.axhline(0, 60, 0, color='lightgray', linestyle='--', linewidth=2)



from itertools import accumulate
b_sit = list(accumulate(HR_list[1:]))
b_wk = list(accumulate(dy_sit['value'][1:]))


plt.plot(b_sit)
plt.plot(b_wk)


#계절성
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

plot_acf(pd.DataFrame(HR_list[1:]))
plot_pacf(pd.DataFrame(HR_list[1:]))
plt.show()


plot_acf(pd.DataFrame(HR_list_wk[1:]))

from scipy import signal

signal.correlate(HR_list[1:], dy_sit['value'], 'full')



#감소 -> 추세 / 물결 -> 계절성
#AR : 자기상관 : 시계열의 시차 값(lagged values) 사이의 선형 관계를 측정
#MA : 무빙에버리지

#######성주
sj = pd.read_csv("philips_sj.csv")

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

dy = pd.read_csv("fitbit_sj.csv")

index_start = dy[dy["time"] == "17:45:01"].index[0]
index_end = dy[dy["time"] == "17:55:56"].index[0]

dy = dy[index_start  : index_end ]

len(dy)

dy = dy.reset_index(drop = True)

list_time = []
for i in range(len(dy)):
    list_time.append(str(dy['time'][i][:-3])) 
    
    
dy['time_cut'] = list_time
    

#예제데이터 생성
sample_data = pd.date_range('2022-04-12 17:45:01', periods=132, freq='5S')

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



#걷기 na 평균으로 대체
HR_list_wk_2 = pd.DataFrame({'value' : HR_list_wk})
HR_list_wk_2= HR_list_wk_2.dropna()


hr_mean = HR_list_wk_2['value'].mean() 


HR_list_wk = pd.DataFrame({'value' : HR_list_wk})
HR_list_wk= HR_list_wk.fillna(0)



HR_list_wk['value'][1]
for i in range(len(HR_list_wk)):
    if HR_list_wk['value'][i] == 0:
        HR_list_wk['value'][i] = hr_mean



plt.plot(HR_list_wk['value'], '-r', label='philips') 
plt.plot(dy_wk['value'], '-b', label='fitbit')
plt.legend()    




#######효진
sj = pd.read_csv("philips_hj_sit.csv")

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
sj_wk = pd.read_csv("philips_hj_wk.csv")

sj_walk = sj_wk[-150000:]
sj_walk = sj_walk["ECG_HR"]

sj_walk = sj_walk.reset_index(drop = True)


#na값 0으로 대체
sj_walk = sj_walk.fillna(0)
sj_walk.isnull().sum()


#5초(2500개 데이터)단위로 평균
sj_wk = pd.read_csv("philips_hj_wk.csv")


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



##fitbit 데이터 앉기용
import pandas as pd

dy = pd.read_csv("fitbit_hj.csv")

index_start = dy[dy["time"] == "14:07:57"].index[0]
index_end = dy[dy["time"] == "14:12:47"].index[0]

dy = dy[index_start  : index_end ]

len(dy)

dy = dy.reset_index(drop = True)

list_time = []
for i in range(len(dy)):
    list_time.append(str(dy['time'][i][:-3])) 
    
    
dy['time_cut'] = list_time
    

#예제데이터 생성
sample_data = pd.date_range('2022-04-6 14:07:57', periods=132, freq='5S')

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



##fitbit 데이터 걷기용
import pandas as pd

dy = pd.read_csv("fitbit_hj.csv")

index_start = dy[dy["time"] == "14:17:02"].index[0]
index_end = dy[dy["time"] == "14:23:02"].index[0]

dy = dy[index_start  : index_end ]

len(dy)

dy = dy.reset_index(drop = True)

list_time = []
for i in range(len(dy)):
    list_time.append(str(dy['time'][i][:-3])) 
    
    
dy['time_cut'] = list_time
    

#예제데이터 생성
sample_data = pd.date_range('2022-04-6 14:17:02', periods=132, freq='5S')

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
dy_wk = dy_real[:60]
dy_wk = dy_wk.reset_index(drop=True)


len(HR_list)        
len(dy_sit)
    
#시각화
plt.plot(HR_list, '-r', label='philips') 
plt.plot(dy_sit['value'], '-b', label='fitbit')
plt.legend()    



#걷기 na 평균으로 대체
HR_list_wk_2 = pd.DataFrame({'value' : HR_list_wk})
HR_list_wk_2= HR_list_wk_2.dropna()


hr_mean = HR_list_wk_2['value'].mean() 


HR_list_wk = pd.DataFrame({'value' : HR_list_wk})
HR_list_wk= HR_list_wk.fillna(0)



HR_list_wk['value'][1]
for i in range(len(HR_list_wk)):
    if HR_list_wk['value'][i] == 0:
        HR_list_wk['value'][i] = hr_mean



plt.plot(HR_list_wk['value'], '-r', label='philips') 
plt.plot(dy_wk['value'], '-b', label='fitbit')
plt.legend()    