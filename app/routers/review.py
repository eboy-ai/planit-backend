from fastapi import APIRouter, Depends, Query
from app.db.database import get_db
from app.db.schema.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.services import ReviewService
from app.routers.user import Auth_Dependency
from app.services.review import get_current_user_id

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/reviews',tags=['Review'])

# 작성한 여행계획에서 id를 가져올건지 (request body)
#Create
@router.post('/', response_model=ReviewRead)
async def create_review(review_data:ReviewCreate,
                        trip_id:int,
                        current_user:Auth_Dependency,   #로그인한사람만 작성가능
                        db:AsyncSession=Depends(get_db)):
    # 현재 로그인한 유저의 User.id
    user_id = current_user.id
    return await ReviewService.create(db,review_data,user_id,trip_id)

#Read
#리뷰리스트
@router.get('/', response_model=list[ReviewRead])
async def review_list(trip_id:int,
                       db:AsyncSession=Depends(get_db),
                       serach:str|None=Query(None,min_length=1),
                       limit:int = Query(10,ge=1,le=30),
                       offset:int = Query(0,ge=0)):
    return await ReviewService.get_all_review( db=db,
                                               trip_id=trip_id,
                                               search=serach,
                                               limit=limit,
                                               offset=offset)
   
#상세보기
@router.get('/{review_id}', response_model=ReviewRead)
async def read_review(review_id:int,db:AsyncSession=Depends(get_db)):
    result = await ReviewService.get_review(db,review_id)
    return result

#Update
@router.put('/{review_id}', response_model=ReviewRead)
async def update_review(review_id:int, 
                        review:ReviewUpdate,
                        user_id:int = Depends(get_current_user_id),
                        db:AsyncSession=Depends(get_db)
                        ):
    return await ReviewService.update_review_by_id(db,review,review_id,user_id)    

#delete
@router.delete('/{review_id}')
async def delete_review_by_id(review_id:int,user_id:int =Depends(get_current_user_id),db:AsyncSession=Depends(get_db)):
    db_review = await ReviewService.delete_review_by_id(db,user_id,review_id)

    if db_review:
        return {'msg':'리뷰삭제왼료'}
# # 외부api 구조 확인용
# from fastapi import APIRouter, HTTPException
# import httpx

# router = APIRouter(prefix="/test-weather", tags=["Test"])
# API_KEY = "acfe504c47bcfd91a492915a1cf41c28"

# @router.get("/")
# async def get_weather_by_city(city: str):
#     """
#     도시 이름으로 현재 날씨 구조(JSON) 확인용 임시 API
#     예: /test-weather?city=Seoul
#     """
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": city,
#         "appid": API_KEY,
#         "units": "metric",
#         "lang": "kr"
#     }

#     async with httpx.AsyncClient() as client:
#         res = await client.get(url, params=params)
#         if res.status_code != 200:
#             raise HTTPException(status_code=res.status_code, detail=res.text)
#         return res.json()  # 그대로 Response Body로 반환
                                                           
                                                           