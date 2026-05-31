from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import engine, SessionLocal
from app.models import Base, Product

app = FastAPI(
    title="Online Store API",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API works"}
# ----------------------
# Pydantic schemas
# ----------------------

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True


# ----------------------
# ROOT
# ----------------------

@app.get("/")
def root():
    return {"message": "API works"}


# ----------------------
# CREATE
# ----------------------

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate):
    db = SessionLocal()
    try:
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product

    finally:
        db.close()


# ----------------------
# READ ALL
# ----------------------

@app.get("/products", response_model=list[ProductResponse])
def get_products(
    min_price: float | None = None,
    max_price: float | None = None,
    limit: int = 10,
    offset: int = 0
):
    db = SessionLocal()

    try:
        query = db.query(Product)

        # ----------------------
        # FILTER: min price
        # ----------------------
        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        # ----------------------
        # FILTER: max price
        # ----------------------
        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        # ----------------------
        # PAGINATION
        # ----------------------
        products = query.offset(offset).limit(limit).all()

        return products

    finally:
        db.close()

# ----------------------
# READ ONE
# ----------------------

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product
    finally:
        db.close()


# ----------------------
# UPDATE (PUT)
# ----------------------

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated_product: ProductCreate):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product.name = updated_product.name
        product.description = updated_product.description
        product.price = updated_product.price
        product.quantity = updated_product.quantity

        db.commit()
        db.refresh(product)

        return product
    finally:
        db.close()


# ----------------------
# UPDATE (PATCH)
# ----------------------

@app.patch("/products/{product_id}", response_model=ProductResponse)
def patch_product(product_id: int, updated_product: ProductUpdate):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if updated_product.name is not None:
            product.name = updated_product.name

        if updated_product.description is not None:
            product.description = updated_product.description

        if updated_product.price is not None:
            product.price = updated_product.price

        if updated_product.quantity is not None:
            product.quantity = updated_product.quantity

        db.commit()
        db.refresh(product)

        return product
    finally:
        db.close()


# ----------------------
# DELETE
# ----------------------

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete(product)
        db.commit()

        return {"message": "Product deleted"}
    finally:
        db.close()