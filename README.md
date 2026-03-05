# 🐢 ROS Noetic Study

> Ubuntu 20.04 + VMware 환경에서 ROS Noetic을 처음부터 설정하고 실습한 학습 기록입니다.

---

## 🛠️ 개발 환경

| 항목 | 버전 |
|------|------|
| OS | Ubuntu 20.04 LTS |
| 가상머신 | VMware Workstation |
| ROS | Noetic Ninjemys |
| Python | Python 3 |
| 에디터 | VS Code |

---

## 📦 설치 목록

- ✅ ROS Noetic Desktop Full
- ✅ Git + GitHub SSH 등록
- ✅ VS Code + ROS / C++ / Python / GitLens Extension
- ✅ Catkin 워크스페이스 구성
- ✅ Terminator (터미널 분할 도구)

---

## 📁 패키지 구조
```
catkin_ws/
├── src/
│   ├── my_tutorial/
│   │   ├── scripts/
│   │   │   ├── publisher.py
│   │   │   └── subscriber.py
│   │   └── launch/
│   │       ├── my_tutorial.launch
│   │       ├── multi_turtle.launch
│   │       ├── color_turtle.launch
│   │       └── full_turtle.launch
│   └── beginner_tutorials/
│       ├── msg/
│       │   └── Num.msg
│       ├── srv/
│       │   └── AddTwoInts.srv
│       └── scripts/
│           ├── talker.py
│           ├── listener.py
│           ├── add_two_ints_server.py
│           └── add_two_ints_client.py
```

---

## 📚 학습 내용

### 1️⃣ Topic 통신 — Publisher & Subscriber
```
Publisher ──────────────→ Subscriber
         hello world 계속 전송
```

- **특징**: 1:N 통신, 단방향, 응답 없음
- **활용**: 센서 데이터, 카메라 영상, 위치 정보 전송
```bash
roslaunch my_tutorial my_tutorial.launch
```

---

### 2️⃣ Service 통신 — Server & Client
```
Client ──요청(3+5)──→ Server
Client ←──응답(8)──── Server
```

- **특징**: 1:1 통신, 양방향, 응답 필수
- **활용**: 명령 실행, 계산 요청, 상태 조회
```bash
roslaunch beginner_tutorials service.launch
```

---

### 3️⃣ roslaunch 실습

#### 거북이 2마리 독립 제어

![turtlesim 멀티 실행](images/turtlesim.PNG)
```bash
roslaunch my_tutorial multi_turtle.launch
```

- `turtle1` → 키보드(teleop)로 제어
- `turtle2` → rostopic pub으로 독립 제어

---

#### rqt_graph — 노드 관계 시각화

![rqt_graph 노드 시각화](images/rqt_graph.PNG)
```bash
roslaunch my_tutorial full_turtle.launch
```

---

### 4️⃣ 커스텀 msg & srv
```bash
rosmsg show beginner_tutorials/Num
# int64 num

rossrv show beginner_tutorials/AddTwoInts
# int64 a
# int64 b
# ---
# int64 sum
```

---

## 📌 Topic vs Service 비교

| | Topic | Service |
|--|-------|---------|
| 방향 | 단방향 | 양방향 |
| 연결 | 1:N | 1:1 |
| 응답 | ❌ | ✅ |
| 흐름 | 지속적 | 1회성 |
| 활용 | 센서, 영상 | 명령, 계산 |

---

## 🔑 핵심 명령어 정리
```bash
cd ~/catkin_ws && catkin_make   # 빌드
rosrun [패키지] [노드]           # 노드 실행
roslaunch [패키지] [launch파일]  # launch 실행
rostopic list                   # 토픽 목록
rostopic echo /[토픽명]          # 토픽 내용
rosnode list                    # 노드 목록
rqt_graph                       # 노드 시각화
rosrun rqt_console rqt_console  # 로그 모니터링
```
---

## 📸 Day 2 실습 결과

### 카운터 Publisher / Subscriber
![카운터 발행 수신](images/구조13.PNG)

### rqt_graph — 노드 연결 시각화
![rqt_graph](images/구조12.PNG)

### 랜덤 온도 센서 + 경고 시스템
![온도 센서](images/구조14.PNG)

### 거북이 원 그리기
![거북이 원](images/구조15.PNG)

### 거북이 벽 근처 경고
![거북이 벽 경고](images/구조16.PNG)
---

## 👤 Author

- **GitHub**: [@parkmin-je](https://github.com/parkmin-je)
- **Email**: alswp6@naver.com
---

## Day 3 — ROS 서비스 프로그래밍

### 실습 1 & 3: 문자열 길이 서비스 + 파라미터 계산기

![calc-server](images/day3-calc-server.PNG)

- `StringLength.srv` 정의 및 빌드
- `string_length_server.py` / `string_length_client.py` 작성
- `calc_server.py`: `/operator` 파라미터로 add/sub/mul 실시간 전환

### 실습 2: turtlesim 펜 색상 변경

![turtlesim-pen](images/day3-turtlesim-pen.PNG)

- `/turtle1/set_pen` 서비스 호출로 펜 색상 변경
- `change_pen_client.py` 작성 → 초록색 선 확인


---

## Day 3 — rosbag 데이터 기록 & 재생

### rosbag record — 거북이 경로 기록

![rosbag record 중 거북이 경로](screenshots/rosbag_record.png)

### rosbag play — 재생 결과

![rosbag play 재생 결과](screenshots/rosbag_play.png)

- `rosbag record -a` 로 전체 토픽 기록
- `rosbag play` 로 거북이 경로 재현
- `pose_listener.py` 로 rosbag 재생 중 위치 데이터 수신 확인
- 선택적 기록 비교: all_topics(106.6KB) vs cmd_only(7.8KB)

