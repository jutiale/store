from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
import models, schemas
from fastapi.responses import FileResponse
import os
from fastapi import UploadFile
from fastapi import HTTPException
from auth import pwd_context

def get_category_name_by_id(id, db):
    cateogory = db.query(models.Category).filter(models.Category.id == id).first()
    return cateogory.name

def get_brand_name_by_id(id, db):
    brand = db.query(models.Brand).filter(models.Brand.id == id).first()
    return brand.name


def get_good(db: Session, good_id: int):
    good = db.query(models.Goods).filter(models.Goods.id == good_id).first()
    if not good:
        raise HTTPException(status_code=400, detail="The good doesn't exist")
    category = schemas.Category(id=good.category_id, name=get_category_name_by_id(good.category_id, db))
    brand = schemas.Brand(id=good.brand_id, name=get_brand_name_by_id(good.brand_id, db))
    return schemas.GoodRead(id=good.id, name=good.name, description=good.description, category=category,
                            brand=brand, price=good.price)

def get_goods(db: Session, skip: int = 0, limit: int = 100):
    goods = db.query(models.Goods).offset(skip).limit(limit).all()
    total = db.query(models.Goods).count()
    on_page = len(goods)
    goods_res = []
    for good in goods:
        category = schemas.Category(id=good.category_id, name=get_category_name_by_id(good.category_id, db))
        brand = schemas.Brand(id=good.brand_id, name=get_brand_name_by_id(good.brand_id, db))
        goods_res.append(schemas.GoodRead(id=good.id, name=good.name, description=good.description, category=category,
                            brand=brand, price=good.price))
    return schemas.GoodsList(goods=goods_res, total=total, on_page=on_page)


def create_good(db: Session, good: schemas.GoodCreate):
    db_good = models.Goods(name=good.name, description=good.description, 
                           category_id=good.category_id, brand_id=good.brand_id, price=good.price)
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good

def delete_good(db: Session, db_good: schemas.Good):
    db.delete(db_good)
    db.commit()
    return {"ok": True}

def update_good(db: Session, good: schemas.GoodUpdate, db_good: schemas.Good):
    good_data = good.model_dump(exclude_unset=True)
    for key, value in good_data.items():
        setattr(db_good, key, value)
    db.add(db_good)
    db.commit()
    db.refresh(db_good)
    return db_good

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    categories_res = []
    for c in categories:
        categories_res.append(schemas.Category(name=c.name, id=c.id))
    total = db.query(models.Category).count()
    on_page = len(categories)
    return schemas.CategoriesList(categories=categories_res, total=total, on_page=on_page)


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, db_category):
    try:
        db.delete(db_category)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Cannot delete the category")
    return {"ok": True}

def update_category(db: Session, category: schemas.CategoryUpdate, db_category: schemas.Category):
    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_brand(db: Session, brand_id: int):
    return db.query(models.Brand).filter(models.Brand.id == brand_id).first()

def get_brands(db: Session, skip: int = 0, limit: int = 100):
    brands = db.query(models.Brand).offset(skip).limit(limit).all()
    brands_res = []
    for brand in brands:
        brands_res.append(schemas.Brand(name=brand.name, id=brand.id))
    total = db.query(models.Brand).count()
    on_page = len(brands)
    return schemas.BrandsList(brands=brands_res, total=total, on_page=on_page)


def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(name=brand.name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def delete_brand(db: Session, db_brand: schemas.Brand):
    try:
        db.delete(db_brand)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Cannot delete the brand")
    return {"ok": True}

def update_brand(db: Session, brand: schemas.BrandUpdate, db_brand: schemas.Brand):
    brand_data = brand.model_dump(exclude_unset=True)
    for key, value in brand_data.items():
        setattr(db_brand, key, value)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


def upload_image(file: UploadFile):
    file_location = f"images/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return file_location

def create_upload_image(db: Session, good_id: int, path: str):
    db_image = models.Image(path=path, good_id=good_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()

def delete_image(db: Session, db_image: schemas.Image):
    db.delete(db_image)
    db.commit()
    os.unlink(db_image.path)
    return {"ok": True}

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    users_res = []
    for user in users:
        users_res.append(schemas.UserRead(email=user.email, name=user.name, role=user.role, id=user.id))
    total = db.query(models.User).count()
    on_page = len(users)
    return schemas.UsersList(users=users_res, total=total, on_page=on_page)

def create_user_admin(db: Session, user: schemas.UserCreateAdmin):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_admin(db: Session, user: schemas.UserCreateAdmin, user_id):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def delete_user(db: Session, db_user: schemas.User):
    db.delete(db_user)
    db.commit()
    return {"ok": True}

def update_user(db: Session, user_info: schemas.UserUpdate, db_user: schemas.User):
    user_data = user_info.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_my_profile(db: Session, db_user: schemas.User):
    return schemas.UserRead(email=db_user.email, name=db_user.name, id=db_user.id, role=db_user.role)

def add_good_to_cart(db, good_id, user, count=1):
    db_cart = models.Cart(user_id=user.id, good_id=good_id, count=count)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def read_cart(db, user, skip, limit):
    cart_goods = db.query(models.Cart).filter(models.Cart.user_id == user.id).offset(skip).limit(limit).all()
    goods = []
    total_price = 0
    for cart_good in cart_goods:
        good = db.query(models.Goods).filter(models.Goods.id == cart_good.good_id).first()
        category = schemas.Category(id=good.category_id, name=get_category_name_by_id(good.category_id, db))
        brand = schemas.Brand(id=good.brand_id, name=get_brand_name_by_id(good.brand_id, db))
        good_read = schemas.GoodInCartRead(id=good.id, id_in_cart=cart_good.id, name=good.name, count=cart_good.count, category=category, 
                                           brand=brand, price=good.price)
        goods.append(good_read)
        total_price += good.price * cart_good.count
    result = schemas.CartInfo(total_price=total_price, goods=goods)
    return result

def delete_cart(db, user):
    db.query(models.Cart).filter(models.Cart.user_id == user.id).delete()
    db.commit()
    return {"ok": True}

def delete_good_in_cart(db, user, good_in_cart_id):
    db.query(models.Cart).filter(and_(models.Cart.user_id == user.id, models.Cart.id == good_in_cart_id)).delete()
    db.commit()
    return {"ok": True}

def change_count_goood_in_cart(db, user, good_in_cart_id, count):
    db_good = db.query(models.Cart).filter(and_(models.Cart.id == good_in_cart_id, models.Cart.user_id == user.id)).first()
    db_good.count = count
    db.commit()
    db.refresh(db_good)
    return db_good

def create_order(db, user):
    order = read_cart(db, user, 0, 100)
    if not order.goods:
        raise HTTPException(status_code=404, detail="The cart is empty")
    delete_cart(db, user)
    return order

