# SNS-API
소셜 네트워킹 서비스(sns) API

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [개발 기간](#개발-기간)
3. [프로젝트 기술 스택](#프로젝트-기술-스택)
4. [요구사항 분석](#요구사항-분석)
5. [ERD](#erd)
6. [API 명세](#api-명세)
7. [프로젝트 구조](#프로젝트-구조)
8. [프로젝트 시작 방법](#프로젝트-시작-방법)


<br>

## 프로젝트 개요


Django Rest Framework 를 이용한 REST API 서버로

- 유저 회원가입, 로그인(토큰 인증 방식) 기능
- 게시글 생성, 수정, 삭제, 조회 기능
- 좋아요

위 기능을 제공합니다.

<br>

## 개발 기간
- 2022/09/29~2022/10/03 (3일)


<br>

## 프로젝트 기술 스택

### Backend
<section>
<img src="https://img.shields.io/badge/Django-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?logo=Django&logoColor=white"/>
</section>

### DB
<section>
<img src="https://img.shields.io/badge/MySQL-4479A1?logo=MySQL&logoColor=white"/>
</section>

### Tools
<section>
<img src="https://img.shields.io/badge/GitHub-181717?logo=GitHub&logoColor=white"/>
<img src="https://img.shields.io/badge/Discord-5865F2?logo=Discord&logoColor=white">
<img src="https://img.shields.io/badge/Postman-FF6C37?logo=Postman&logoColor=white">
</section>

<br>

## 과제 요구사항 분석
✅ 게시글 기능 : 로그인한 유저만 접근 가능합니다.


### 1. 유저 관련

- 모델링 : django의 `AbstractBaseUser`를 상속 받아 이메일을 id로 하는 User 모델 구현
- 
#### 1-1) 유저 회원가입
  
#### 1-2) 유저 로그인
- `simplejwt`를 이용하여 토큰 인증 방식 로그인 구현


### 2. 게시글 관련
#### 2-1) 게시글 생성
- 게시글 생성시 
  1) 제목(title), 내용(content), 태그(tags) 필요
  2) 태그는 '#태그' 형식이며 여러 개인 경우 '#태그1,#태그2' 와 같이 ','로 구분

<br>


#### 2-2) 게시글 수정
- 게시글 수정시
  1) 제목(title), 내용(content), 태그(tags) 필요


#### 2-3) 게시글 조회

- 게시글 전체 조회시
  1) 기본 정렬: 최신순(생성일자 기준)
  2) 정렬은 조회수(`views`), 좋아요 수(`likes`), 생성 일자(`created_at`) 기준으로 가능하며 오름차순, 내림차순 가능
  `url/?ordering=-views` => 내림차순인 경우 필드명 앞에 '-'
  3) 검색이 가능하며 제목을 기준으로 검색 가능
  `url/?search=검색어`
  4) 태그 필터링이 가능하며 여러 개인 경우 ','로 구분하고 해당 태그를 모두 포함한 게시글만 필터링
  `url/?tags=태그1,태그2`
  5) 페이지 사이즈 지정 가능하며 페이지에 표현할 글의 최대 개수는 30개 기본은 10개
  `url/?page_size=20`
  
- 게시글 상세 조회시
  1) 날짜, 유저에 상관 없이 조회시 조회수 1 증가


#### 2-4) 게시글 삭제

- `is_deleted` 필드를 이용하여 soft delete 방식으로 구현
- 삭제 게시글 복구 가능

#### 2-5) 좋아요 기능
- 유저는 한 게시글에 한번 좋아요를 할 수 있으며 좋아요가 되어있는 경우 다시 요청시 좋아요 취소


### 3. 테스트
- 테스트 코드 구현 예정
- `rest_framework`의 `APITestCase` 이용

<br>

### 기능 목록

| 버전  | 기능  | 세부 기능 | 설명                            | 상태 |
|-----|-----|-------|-------------------------------|----|
| v1  | 유저  | 회원가입  | 회원가입                          | ✅  |
| -   | -   | 로그인   | jwt를 이용한 로그인                  | ✅  |
| -   | 게시글 | 생성    | 게시글 생성                        | ✅  |
| -   | -   | 조회    | 게시글 조회                        | ✅  |
| -   | -   | 수정    | 게시글 수정                        | ✅  | 
| -   | -   | 삭제    | 게시글 삭제(soft-delete)           | ✅  |
| -   | -   | 조회    | 조회시 필터링, 페이지네이션, 정렬, 검색 기능    | ✅  |
| -   | -   | 좋아요   | 게시글 좋아요 기능                    | ✅  |
| -   | 테스트 | 테스트   | 기능, 전체 테스트                    |    |

🔥 추가 기능 구현시 업데이트 예정

<br>

## ERD

- User model
  - User 모델은 Django의 `AbstractBaseUser`를 overriding 
- Post model
  - USER ↔ POST (1:N)
  - POST ↔ HASHTAG (N:M)
  - POST ↔ USER (N:M) (좋아요 기능)
- HashTag model


<br>


## API 명세

[POSTMAN API DOCS](https://documenter.getpostman.com/view/19274775/2s83tJFqL7)

## 프로젝트 구조
```bash         
├── apps              
│   ├── account       
│   │   ├── admin.py  
│   │   ├── apps.py   
│   │   ├── forms.py  
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── post
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── paginations.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── urls.py
├── config
│   ├── asgi.py
│   ├── settings
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   │   └── test.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

```

<br>

## 프로젝트 시작 방법
1. 로컬에서 실행할 경우
```bash
# 프로젝트 clone(로컬로 내려받기)
git clone -b develop --single-branch ${github 주소}
cd ${디렉터리 명}

# 가상환경 설정
python -m venv ${가상환경명}
source ${가상환경명}/bin/activate
# window (2 ways) 
# 1> ${가상환경명}/Scripts/activate
# 2> activate

# 라이브러리 설치
pip install -r requirements.txt
# 실행
python manage.py runserver
```

<br>