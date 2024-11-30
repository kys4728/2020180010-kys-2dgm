
# 프로젝트 제목 : 아머드 샷
 
게임의 간단한 소개 (카피의 경우 원작에 대한 언급)

![image](https://github.com/user-attachments/assets/16c15421-9e85-498b-ad43-c30325fe29ad)

## 게임 컨셉
  2D 슈팅게임으로 우주를 배경으로 하여 전방에서 접근하는 적을 섬멸하고 일정한 적 처치시 보스전에 돌입하여 처치하는 게임,
  고전 게임인 캡콤의 194x 시리즈, 드래곤 플라이트 등의 시스템을 일부분을 사용
  
## 핵심 메카닉 제시

- **이동**  : 키보드 상하좌우 키로 화면 내를 자유롭게 이동

- **공격** : z키로 공격하며 x 키를 입력 시 강한 공격이 발사됨

- **업그레이드** : 적 소멸 시 아이템을 떨구고 아이템을 먹으면 강화가 됨

- **보스** : 일정 적 처치시 보스가 등장 보스 처치 시 게임 종료

- **체력** : 목숨은 3개 있으며 공격 피격시 플레이어 체력 감소, 0이 되면 목숨이 한 개 소진됨

## 스크린샷 혹은 그림판으로 끄적인 이미지 포함

![image](https://github.com/user-attachments/assets/8899378e-c61d-42cb-800f-8c47deacc6fd)

- 예상 게임 실행 흐름 (간단히 스케치한 그림 사용, 게임이 어떤 식으로 진행되는지 직관적으로 알 수 있도록 구성)

<img width="725" alt="image" src="https://github.com/user-attachments/assets/965b93bc-9d1a-49e9-a6a2-723a0dc00a3c">

<img width="958" alt="image" src="https://github.com/user-attachments/assets/d81e4727-ed2e-422e-9f25-f27f292f92b3">

## 예상 게임 흐름 설명 
1. 게임 시작 시 시작화면 생성
2. 게임 시작 클릭 시 스테이지로 전환 되며 적들이 등장
3. 적 처치 후 업그레이드로 강화하며 게임 진행
4. 보스 등장 후 처치시 게임 종료
5. 게임 종료 화면 생성


## 개발 내용
### Scene 의 종류 및 구성, 전환 규칙

- **로딩 화면** : 게임 시작 회면 전 츨력

- **시작 화면** :
  - 시작 화면에는 게임 이름, 게임 시작 버튼, 종료 버튼이 있음
  - 시작 버튼 클릭 시 플레이 화면으로 전환됨
  - 종료 버튼 클릭 시 프로그램이 종료

- **플레이 화면** :
  - 게임 시작 버튼을 클릭 후 나오며 플레이어는 상하좌우 키로 이동하며 z,x 로 투사체를 발사가능해짐, 화면의 상단부(전체화면의 절반)에서 적이 생성되어 플레이어를 향해 투사체 공격을 하며 화면 내 적을 처치해야 다음 적이 출현하며 일정 적 처치 시 보스가 등장하며 보스는 게임 최상단에 전용 체력바를 가지고 등장

~~- **게임 종료 화면** : 보스 처치 시 게임 종료 화면이 뜨며 이때 아무키를 눌러 시작 화면으로 돌아가게 함~~ 
 
 (${\textsf{\color{red}2차발표 수정 사항: 비슷한 기능을 가진 게임 오버 화면과 통합}}$)

- **게임 오버 화면** : 플레이어의 목숨이 0이 되면 게임 오버 화면이 뜨며 재도전 버튼과 시작 화면으로 돌아가는 버튼이 생성되어 게임을 재개하거나 타이틀로 돌아갈 수 있음

- **일시 정지 화면** : 플레이 화면에서 esc 버튼을 누르면 게임이 일시정지되며 재개버튼과 시작화면으로 가는 버튼으로 재개하거나 타이틀로 돌아갈 수 있음

### 각 Scene 에 등장하는 GameObject 의 종류 및 구성, 상호작용

- 모든 class 에 대한 언급
- 각 클래스의 역할을 나열
- 생김새를 간단한 문장으로 표현
- 화면에 보이지 않는 Controller 객체들에 대한 언급
- 함수 단위의 설명 (1차발표때는 아직 알 수 없을 것이므로, 2차발표때 추가)

  - **플레이어** : 전투기 형상, 상하좌우 이동하며 z로 일반 공격, x로 횟수 제한의 강한 공격의 투사체로 적을 공격, 적 투사체에 공격 받거나 적 캐릭터에 부딫히면 체력이 감소
        
  - **업그레이드 아이템** : 무기 모양, 적 처치 시 업그레이드 아이템이 등장하며 일반 공격을 강화/ 강한 공격의 남은 횟수를 채워줌, 플레이어가 사망시 업그레이드 무기가 흩어지며 플레이어는 게임 초기 상태로 돌아감 

  - **적** : 작은 비행체 모양, 투사체를 발사하는 적이 있으며 투사체를 발사하는 적은 플레이어를 향해 공격함

  (${\textsf{\color{red}2차발표 수정 사항 : 플레이어와 충돌하는 공격하는 적 유형 '잔해'는 비행체가 관련 기능을 가지고 있기에 필요없다 판단하여 삭제했습니다.}}$)

  - **보스** : 거대한 비행체 형태, 일정 적 처치 시 보스가 나오며 보스는 일반 적보다 빠른 공격과 거대한 투사체로 공격하며 별도의 체력바를 가짐, 일정 체력 이하가 되면 공격 속도가 빨라지는 특징을 가짐

  - **배경** : 어두운 우주를 배경으로 남색의 배경을 그리며 보스를 처치하면 게임 종료화면으로 전환됨

  - **UI** : 플레이어의 체력과 목숨, 강한 공격 무기의 횟수, 업그레이드 상태가 화면 하단부의 표시가 됨

  - **입력 감지 controller** : 플레이어의 입력에 따른 캐릭터 움직임과 공격 제어

  - **화면 controller** : 화면 전환을 감지하는 역할, 플레이어의 체력 /업그레이드 상황 또는 보스 체력의 상황을 화면에 표시해줌

  - **충돌 감지 controller** : 화면 내 적, 플레이어, 투사체 들의 충돌을 감지하여 플레이어와 충돌 시 체력이 감소하게 끔 함

### 사용한/사용할 개발 기법들에 대한 간단한 소개 (각 개발 요소들을 정량적으로 제시할 것)

- 파이썬 : 
  pico2d 로 60fps로 최대 30개의 오브젝트 렌더링
  플레이어, 적, 보스, 아이템 투사체 등의 클래스를 구현하고 화면에 50개의 오브젝트를 처리하게 함
  프레임 단위의 캐릭터와 적의 애니메이션을 구현
  Collision Checker를 통해 적 및 아이템 충돌 감지
  
- 포토샵 : 게임 내 배경 및 플레이어, 적 등 이미지 파일 수정 시 사용

### 게임 프레임워크   
프레임워크에서 지원되는 기능들 중 어떤 것을 사용할 것인지
아직 배우지 않았거나 다루지 않을 항목이 있는지

 - Scene 관리 함수를 통해 전환 및 관리를 한다

 - 루프를 통해 업데이트, 렌더링, 이벤트 처리를 한다

 - 키보드의 입력을 받아 게임의 동작을 제어한다

 - 이미지 로드 함수로 메모리에 로드하여 성능을 최적화한다

 - 스프라이트 클래스로 화면에 이미지를 렌더링 한다

 - 애니메이션 스프라이트로 프레임 단위의 이미지 애니메이션 구현

 - 충돌 감지 함수를 사용하여 객체간의 충돌 확인

## 일정 (1차 발표 전까지 수정 가능)

 10/28 이전에 준비할 사항들을 나열해 본다
 10/28 부터 7주(6.5주)간의 개발 계획을 수립한다
 다른 수업이나 과제, 시험 등을 고려하여 현실적인 계획을 짠다
 수시로 변경되는 것을 수정하며 수정 사유를 함께 기입한다.
 일정 대비 진행 상황을 발표 이후 매주 업데이트한다.

 - 10/28 이전 : 게임 컨셉 강화 및 다루기 힘든 부분 제거, 게임 내 사용할 스프라이트 조사 (res 파일에 추가), 필요시 사운드 파일 수집

 - 1주차(10/29 ~ 11/3)
 스프라이트 추가, 씬 구성(메인, 플레이 등), 플레이어의 이동과 공격 메카니즘 구현

 - 2주차(11/4 ~ 11/10)
 적 캐릭터와 충돌 감지 구현 / 패턴 구현

 - 3주차(11/11 ~ 11/17)
 업그레이드 아이템 구현 및 플레이어와 상호작용 구현

 - 4주차(11/17 ~ 11/24)
 버그 수정/추가 사항 기재 및 2차 발표 준비

 - 5주차(11/26 ~ 12/1)
 보스 추가 / 패턴 추가

 - 6주차(12/2 ~ 12/8)
UI 및 사운드 추가

 - 7주차(12/8 ~ 12/12)
최종 버그 및 최적화, 3차발표 준비

## 구현하면서 어려운 부분, 수업에서 추가로 다루었으면 하는 부분에 대한 언급 (최종 발표때까지 수정 가능)
수업 진행 방식에 대한 제안 (최종 발표때까지 수정 가능)

1차 발표 영상 YouTube link: https://youtu.be/gQt7B6bFdbg

1차 발표 전까지의 활동 정리

1. res 파일에 게임 내 사용할 리소스 스프라이트를 추가 하였습니다.
2. res 파일에 맞추어 게임 내 들어갈 객체의 설명을 변경하였습니다.
3. 제작 시 불필요한 부분을 제거하였습니다. (로딩창 출력은 게임 시작시에만 출력되도록 변경했습니다)

### 진행 상황 보고

 - **1주차**
1. 게임 환경에 맞게 1주차에 사용할 수정된 스프라이트를 res에 추가하였습니다.
2. 플레이어 객체의 상하좌우 이동과 발사를 구현하였습니다. 
3. 투사체는 키(z또는 x)를 누르고 있는 동안에는 계속 발사 됩니다.
4. 강한 공격인 x의 경우 현재 3회 발사 시 3초의 충전시간을 가집니다.(모두 소진해야 충전됩니다.)

 - **2주차**
1. 적캐릭터를 추가 하였으며 적은 플레이어를 향해 3발의 공격을 발사합니다.
2. 플레이어의 투사체가 적의 투사체를 파괴하지 않고 적 객체만 공격하게끔 하였습니다.
3. 패턴은 대각선 방향에서 임시로 등장하게끔 하였습니다.

 - **3주차**
1. 로딩 씬, 타이틀 씬이 추가 되었습니다.
2. 아이템이 추가 되었습니다 현재 이미지는 수정 전입니다.
3. 아이템은 적이 죽으면 랜덤하게 나오며 플레이어의 체력 또는 데미지를 증가시킵니다.
4. 적 투사체가 플레이어에 충돌하면 플레이어 체력이 감소하며 0이되면 종료됩니다.
5. 백그라운드 확장자 명을 수정하여 통일성 있게 만들었습니다.

 - **4주차 및 2차 발표 요약**
1. https://www.youtube.com/watch?v=Iqbj7lOMYyo (2차발표 영상 링크)
2. 2차 발표 피드백을 반영하여 read.me의 형식을 수정하였습니다.
3. 삭제 요소를 반영하여 리드미에 추가 했습니다.
4. 이전까지의 커밋 수
   
<img width="749" alt="image" src="https://github.com/user-attachments/assets/6355585a-b144-456f-b995-512fb3766581">

6. 주차 별 구현 내용

<img width="938" alt="image" src="https://github.com/user-attachments/assets/b6b820c5-04c9-4f1a-a808-6864b7f25c27">

