# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from src.config.db_config import get_db
# from services.example_service import ReviewService

# reviews_router = APIRouter()

# @reviews_router.get("/{review_id}")
# async def get_review(review_id:int, db: Session = Depends(get_db)):
#     if review_id <= 0:
#         raise HTTPException(status_code=400, detail="Invalid review_id, must be greater than 0")
#     try:
#         review = await ReviewService.get_review_by_id(db=db, review_id=review_id)
#         if not review:
#             raise HTTPException(status_code=404, detail="Review not found")
#         return review
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    

# @reviews_router.get("/product/{product_id}")
# async def get_review_by_product(product_id: int, db: Session = Depends(get_db)):
#     if product_id <= 0:
#         raise HTTPException(status_code=400, detail="Invalid product_id, must be greater than 0")
#     try:
#         reviews = await ReviewService.get_review_by_product_id(db=db, product_id=product_id)
#         if not reviews:
#             raise HTTPException(status_code=404, detail="Product does not have review yet")
#         return reviews
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
