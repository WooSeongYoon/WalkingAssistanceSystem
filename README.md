# WalkingAssistanceSystem
시각장애인을 위한 "보행 보조 시스템"   
![image](https://github.com/user-attachments/assets/63f36dcb-033f-451d-95aa-a3b020f79597)

## 개요
2024년 기준 대한민국에는 여러 가지 시각장애인 보조가 이루어지고 있지만, 여전히 보도 환경에서 킥보드, 손상된 점자블록 등으로 인해 안전한 보행에 어려움을 겪고 있는 현실입니다. 국민권익위원회의 자료에 따르면 1,257건(44.2%)의 점자블록 파손･훼손의 민원이 들어 왔습니다. 또한 킥보드, 자전거 등 위험 물체로 인해 다치는 사례가 꾸준히 발생하고 있는 것을 기사와 보고서 등으로 확인하였습니다.   
이를 통해 관리가 되지 않은 점자블록과 위험 물체로 인하여 교통약자들이 몇 년 동안 어려움을 겪고 있다. 이를 해결하고자 해당 프로그램을 개발하게 되었습니다.

## 설계 및 구현
1. 시제품 구성도 및 기능
![image](https://github.com/user-attachments/assets/24bacd0c-8189-4e64-8735-2ea03c2fa515)   
![image](https://github.com/user-attachments/assets/bcafb25c-322a-4df8-94c8-8aa9a75d55bb)   
보행 보조 임베디드 시스템은 라즈베리파이5를 기반으로 2D 라이다, GPS 모듈, 웹캠을 통합하여 시각장애인의 안전한 보행을 지원하는 시스템입니다.   
![image](https://github.com/user-attachments/assets/2ebb2bdd-0efa-42cc-9e0a-706fc2ba0a5d)   

2. 2D 라이다 센서   
![image](https://github.com/user-attachments/assets/f8ac56ab-b473-4604-a634-4719003baeac)   
본 시스템에 사용한 그림3의 TFmini Plus 라이다는 TOF(Time of Flight, 비행 시간) 원리를 기반으로 작동하며 구체적으로는 정해진 시간마다 변조된 근적외선을 방출하고 반사된 빛의 왕복 위상 차이를 파악하여 비행시간을 측정합니다.   
장애물과의 거리 측정을 통해 1m 이내에 있는 객체를 탐지하기 위해 사용하였습니다. 시스템이 작동하는 그 순간의 거리 측정한 값을 나타내는 방식을 사용하였습니다. 이러한 방식으로 라즈베리파이 5로 특정 거리에 있는 객체를 인식할 수 있습니다.

3. Yolov11
![image](https://github.com/user-attachments/assets/0a22d4a0-b563-48b3-96ef-d744923732ce)   

4. GPS 모듈
 라즈베리 파이가 카메라에서, 점자 블록 손상 위치, 파손된 볼라드 위치 등을 식별하게 되면, GPS 모듈을 기반으로 현재 위치를 클라우드 데이터베이스에 전송하고 지도 웹페이지에 표시하게끔 합니다.   
“gps.gps(host="localhost", port="2947")” 해당 코드를 사용하여 GPS 값인 경도, 위도를 반환할 수 있습니다. 이렇게 출력된 경도, 위도의 값으로 네이버 API를 활용하여 도로명 주소를 출력합니다.   
출력할 때는 건물과 도로의 도로명 주소가 다르기 때문에 조건문을 사용하여 특정 위치 그림9와 같이 전부 출력할 수 있습니다.
![image](https://github.com/user-attachments/assets/8a76725e-87b6-4f44-975d-010bff56df95)   

5. MongoDB 클라우드 데이터베이스
![image](https://github.com/user-attachments/assets/058fcf24-a190-495a-9d10-399c3ed3c393)   
MongoDB 클라우드 데이터베이스는 인터넷 가상환경에서 실행이 가능한 비정형 데이터베이스로, 라즈베리파이5에서 로컬 데이터베이스를 처리하기에는 과부화가 우려되어 선택하게 되었습니다.   
해당DB는 상기의 표와 같이 학습한 YOLOv11s 모델이 인식한 파손된 객체데이터와, GPS 모듈의 현재 위도 & 경도 값 및 인식한 사진의 BSON 데이터를 저장하고 해당하는 데이터를 지도 웹페이지에서 로딩 할 수있도록 구성하였습니다.

6. 웹 페이지
![image](https://github.com/user-attachments/assets/70bffb51-f562-4fc8-baa8-b4dee4d9a663)   
MongoDB에서 저장한 데이터를 웹페이지를 통해 표시하고, flask를 통해 웹을 호스팅하여 언제 어디서나 접근할 수 있도록 설정하고, 불러온 위도, 경도값을 네이버 cloud platform의 지도에서 표시할 수 있도록 처리하였습니다.

## 기대효과
![image](https://github.com/user-attachments/assets/9648c29c-5836-4e1f-837a-b53f0882eb5e)   
MongoDB에서 저장한 데이터를 웹페이지를 통해 표시하고, flask를 통해 웹을 호스팅하여 언제 어디서나 접근이 가능하도록 설정하고, 불러온 위도, 경도값을 네이버 cloud platform의 지도에서 표시할 수 있도록 처리 하였습니다.

## 성과
 - 2024.04.17. | [대구대학교 창업지원단] 창업동아리 선정
 - 2024.04.29. | [대구대학교 Linc3.0] 30만원 지원금 선정
 - 2024.05.27. | [대구대학교 공학교육혁신센터] 180만원 지원금 선정
 - 2024.06.14. | [벤처스타트업 아카데미사업단] 캡스톤디자인 장려상
 - 2024.09.13. | [대구대학교 창업지원단] 린스타트업 200만원 지원금 선정
 - 2024.10.01. | [대구대학교 Linc3.0] 30만원 지원금 선정
 - 2024.11.21. | [대구대학교 정보통신대학] 정보통신대전 대상(총장상)
 - 2024.08.01. | [대구대학교 교육혁신원] Learning SIG+ 우수상(총장상)
 - 2024.11.24. | [대구대학교 정보통신연구소] 졸업 논문 작성
 - 2024.12.12. | [대구대학교 Linc3.0] 캡스톤디자인 최우수상
