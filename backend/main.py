from fastapi import Cookie, FastAPI, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect, WebSocketException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, engine
from typing import List, Union
from fastapi import FastAPI, File, UploadFile, Security
import auth
from auth import get_current_user
import models
from typing_extensions import Annotated
from auth import oauth2_scheme
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
connected_managers = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: Annotated[Union[str, None], Query()]):
    await websocket.accept()
    if not token:
        await websocket.close()
    print(token)
    user = auth.get_user_by_token(token=token, db=SessionLocal())
    try:
        if user.role == 2:
            connected_managers.append({"websocket": websocket, "user_name": user.name})
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        connected_managers.remove({"websocket": websocket, "user_name": user.name})


async def send_message_to_manager(user_name, price):
    message = {
        "user_name": user_name,
        "total_price": price
    }
    print(message)
    for user_name in connected_managers:
        socket = user_name["websocket"]
        await socket.send_json(message)
        
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/users/me", tags=['users'])
def get_user_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user

@app.post("/register", tags=['users'])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/token", tags=['users'])
def authenticate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> schemas.Token:
    user = schemas.UserAuth(email=form_data.username, password=form_data.password) 
    return auth.authenticate_user(user, db)

@app.get("/users/", response_model=schemas.UsersList, tags=['users'])  # Просмотр списка пользователей
def read_users(current_user: Annotated[schemas.User, Security(get_current_user, scopes=["UsersRead"])],
            skip: int = 0, limit: int = 100, 
            db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.post("/users/", response_model=schemas.User, tags=['users'])  
def create_user(user: schemas.UserCreateAdmin, current_user: Annotated[schemas.User, Security(get_current_user, scopes=["UsersCreate"])],
            db: Session = Depends(get_db)):
    return crud.create_user_admin(db, user)

@app.patch("/users/{user_id}", response_model=schemas.User, tags=['users'])  
def update_user(user_id: int, user: schemas.UserUpdateAdmin, current_user: Annotated[schemas.User, Security(get_current_user, scopes=["UsersCreate"])],
            db: Session = Depends(get_db)):
    return crud.update_user_admin(db, user, user_id)

@app.get("/myprofile/", response_model=schemas.UserRead, tags=['my_profile'])  # Просмотр 
def get_my_profile(current_user: Annotated[schemas.User, Depends(get_current_user)], 
                db: Session = Depends(get_db)):
    db_user = crud.get_user(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="This user doesn't exist")
    return crud.get_my_profile(db, db_user)

@app.patch("/myprofile/", response_model=schemas.UserRead, tags=['my_profile'])  # Изменение 
def update_user(current_user: Annotated[schemas.User, Depends(get_current_user)], 
                user_info: schemas.UserUpdate,
                db: Session = Depends(get_db)):
    db_user = crud.get_user(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="This user doesn't exist")
    return crud.update_user(db, user_info, db_user)

@app.delete("/myprofile/", tags=['my_profile'])  # Удаление
def delete_user(current_user: Annotated[schemas.User, Depends(get_current_user)], 
                db: Session = Depends(get_db)):
    db_user = crud.get_user(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="This user doesn't exist")
    return crud.delete_user(db, db_user)

# @app.patch("/users/{user_id}", response_model=schemas.UserRead, tags=['users'])  # Изменение 
# def update_user(current_user: Annotated[schemas.User, Security(get_current_user, scopes=["UsersUpdate"])], 
#                 user_info: schemas.UserUpdate,
#                 user_id: int,
#                 db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="This user doesn't exist")
#     return crud.update_user(db, user_info, db_user)

@app.delete("/users/{user_id}", tags=['users'])  # Удаление
def delete_user(current_user: Annotated[schemas.User, Security(get_current_user, scopes=["UsersDelete"])], 
                user_id: int,
                db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="This user doesn't exist")
    return crud.delete_user(db, db_user)

@app.get("/")
def read_root():
    return {"Hello": "World"}
    

@app.get("/goods/", response_model=schemas.GoodsList, tags=['goods'])  # Просмотр списка товаров
async def read_goods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_goods(db, skip=skip, limit=limit)

@app.get("/goods/{good_id}", response_model=schemas.GoodRead, tags=['goods'])  # Поиск по id 
def read_good(good_id: int, db: Session = Depends(get_db)):
    good = crud.get_good(db, good_id)
    return good
 
@app.post("/goods/", response_model=schemas.Good, tags=['goods'])  # Создание 
def create_good(good: schemas.GoodCreate, 
                current_user: Annotated[schemas.User, Security(get_current_user, scopes=["GoodsCreate"])], 
                db: Session = Depends(get_db)):
    return crud.create_good(db, good)

@app.delete("/goods/{good_id}", tags=['goods'])  # Удаление 
def delete_good(good_id: int, 
                current_user: Annotated[schemas.User, Security(get_current_user, scopes=["GoodsDelete"])], 
                db: Session = Depends(get_db)):
    db_good = db.query(models.Goods).filter(models.Goods.id == good_id).first()
    if not db_good:
        raise HTTPException(status_code=400, detail="The good doesn't exist")
    return crud.delete_good(db, db_good)

@app.patch("/goods/{good_id}", response_model=schemas.Good, tags=['goods'])  # Изменение
def update_good(good_id: int, good: schemas.GoodUpdate, 
                current_user: Annotated[schemas.User, Security(get_current_user, scopes=["GoodsUpdate"])], 
                db: Session = Depends(get_db)):
    db_good = db.query(models.Goods).filter(models.Goods.id == good_id).first()
    if not db_good:
        raise HTTPException(status_code=400, detail="The good doesn't exist")
    return crud.update_good(db, good, db_good)

@app.get("/categories/", response_model=schemas.CategoriesList, tags=['categories'])  # Просмотр списка категорий
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/{category_id}", response_model=schemas.Category, tags=['categories'])  # Поиск по id 
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    return category
 
@app.post("/categories/", response_model=schemas.Category, tags=['categories'])  # Создание 
def create_category(category: schemas.CategoryCreate, 
                    current_user: Annotated[schemas.User, Security(get_current_user, scopes=["CategoriesCreate"])], 
                    db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@app.delete("/categories/{category_id}", tags=['categories'])  # Удаление 
def delete_category(category_id: int, 
                    current_user: Annotated[schemas.User, Security(get_current_user, scopes=["CategoriesDelete"])], 
                    db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="This category doesn't exist")
    return crud.delete_category(db, db_category)

@app.patch("/categories/{category_id}", response_model=schemas.Category, tags=['categories'])
def update_category(category_id: int, category: schemas.CategoryUpdate,
                    current_user: Annotated[schemas.User, Security(get_current_user, scopes=["CategoriesUpdate"])], 
                    db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="This category doesn't exist")
    return crud.update_category(db, category, db_category)

@app.get("/brands/", response_model=schemas.BrandsList, tags=['brands'])  # Просмотр списка брендов
def read_brands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    brands = crud.get_brands(db, skip=skip, limit=limit)
    return brands

@app.get("/brands/{brand_id}", response_model=schemas.Brand, tags=['brands'])  # Поиск по id 
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = crud.get_brand(db, brand_id)
    return brand
 
@app.post("/brands/", response_model=schemas.Brand, tags=['brands'])  # Создание 
def create_brand(brand: schemas.BrandCreate, 
                 current_user: Annotated[schemas.User, Security(get_current_user, scopes=["BrandsCreate"])], 
                 db: Session = Depends(get_db)):
    return crud.create_brand(db, brand)

@app.delete("/brands/{brand_id}", tags=['brands'])  # Удаление 
def delete_brand(brand_id: int, 
                 current_user: Annotated[schemas.User, Security(get_current_user, scopes=["BrandsDelete"])], 
                 db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="This brand doesn't exist")
    return crud.delete_brand(db, db_brand)

@app.patch("/brands/{brand_id}", response_model=schemas.Brand, tags=['brands'])
def update_brand(brand_id: int, brand: schemas.BrandUpdate, 
                 current_user: Annotated[schemas.User, Security(get_current_user, scopes=["BrandsUpdate"])], 
                 db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="This brand doesn't exist")
    return crud.update_brand(db, brand, db_brand)


@app.post("/goods/{good_id}/images", response_model=schemas.Image, tags=['goods'])
def upload_image(good_id: int, file: UploadFile, 
                 current_user: Annotated[schemas.User, Security(get_current_user, scopes=["GoodsUpdate"])], 
                 db: Session = Depends(get_db)):
   file_location = crud.upload_image(file)
   return crud.create_upload_image(db, good_id, file_location)

@app.delete("/goods/{good_id}/images/{image_id}", tags=['goods'])
def delete_image(image_id: int, 
                 current_user: Annotated[schemas.User, Security(get_current_user, scopes=["GoodsUpdate"])], 
                 db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="This image doesn't exist")
    return crud.delete_image(db, db_image)

@app.get("/goods/{good_id}/images", response_model=List[schemas.Image], tags=['goods'])  # Просмотр списка 
def read_images(good_id: int, db: Session = Depends(get_db)):
    good = db.query(models.Goods).filter(models.Goods.id == good_id).first()
    if not good:
        raise HTTPException(status_code=400, detail="The good doesn't exist")
    return good.images

@app.post("/goods/{good_id}/add_to_cart", tags=['goods'])
def add_good_to_cart(good_id: int, current_user: Annotated[schemas.User, Depends(get_current_user)], count: int = 1, 
                     db: Session = Depends(get_db)):
    return crud.add_good_to_cart(db, good_id, current_user, count)


@app.get("/myprofile/cart/", response_model=schemas.CartInfo, tags=['cart'])  
def read_cart(current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db), 
              skip: int = 0, limit: int = 20):
    return crud.read_cart(db, current_user, skip, limit)

@app.delete("/myprofile/cart/", tags=['cart']) 
def delete_cart(current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return crud.delete_cart(db, current_user)

@app.delete("/myprofile/cart/{good_in_cart_id}", tags=['cart'])  
def delete_goood_in_cart(good_in_cart_id: int, current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return crud.delete_good_in_cart(db, current_user, good_in_cart_id)

@app.patch("/myprofile/cart/{good_in_cart_id}", tags=['cart'])  
def change_count_goood_in_cart(good_in_cart_id: int, count: int, current_user: Annotated[schemas.User, Depends(get_current_user)], 
                               db: Session = Depends(get_db)):
    return crud.change_count_goood_in_cart(db, current_user, good_in_cart_id, count)

@app.post("/myprofile/cart/buy", tags=['cart'])  
async def create_order(current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    order = crud.create_order(db, current_user)
    await send_message_to_manager(current_user.name, order.total_price)
    return order

