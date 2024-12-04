from pydantic import BaseModel
from typing import Union, List
from sqlalchemy.orm import Session


class GoodBase(BaseModel):
    name: str
    description: Union[str, None] = None    
    category_id: int
    brand_id: int
    price: float



    

    
class GoodCreate(GoodBase):
    pass

class GoodUpdate(GoodBase):
    pass

class Good(GoodBase):
    id: int
    class Config:
        orm_mode = True



class CategoryBase(BaseModel):
    # id : int
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True
        
class CategoriesList(BaseModel):
    categories: List[Category]
    total: int
    on_page: int


class BrandBase(BaseModel):
    name: str

class BrandRead(BrandBase):
    pass

class BrandCreate(BrandBase):
    pass 

class BrandUpdate(BrandBase):
    pass

class Brand(BrandBase):
    id: int
    class Config:
        orm_mode = True
        
class BrandsList(BaseModel):
    brands: List[Brand]
    total: int
    on_page: int

class ImageBase(BaseModel):
    path: str
    good_id: int

class ImageCreate(ImageBase):
    pass

class ImageRead(ImageBase):
    pass

class Image(ImageBase):
    id: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    name: str
    password: str

class UserRead(UserBase):
    id: int
    name: str
    role: int

class UserUpdate(UserBase):
    name: str
    password: str

class User(UserBase):
    id: int
    name: str
    hashed_password: str
    role: int

    class Config:
        orm_mode = True
        
class UserCreateAdmin(BaseModel):
    name: str
    email: str
    role: int
    password: str

class UserUpdateAdmin(BaseModel):
    name: str
    email: str
    role: int

class UserAuth(UserBase):
    password: str
    
class UsersList(BaseModel):
    users: List[UserRead]
    total: int
    on_page: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    scopes: List[str] = []

class GoodInCartRead(BaseModel):
    id: int
    id_in_cart: int
    name: str
    count: int
    category: Category
    brand: Brand
    price: float

class CartInfo(BaseModel):
    total_price: float
    goods: List[GoodInCartRead]

class GoodRead(BaseModel):
    id: int
    name: str
    description: Union[str, None] = None    
    category: Category
    brand: Brand
    price: float
    

class GoodsList(BaseModel):
    goods: List[GoodRead]
    total: int
    on_page: int