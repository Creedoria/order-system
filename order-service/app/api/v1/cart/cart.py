from fastapi import APIRouter, Depends, HTTPException
from app.model.cart_model import CartItemResponse
from app.core.auth import get_current_user_id
from sqlalchemy.orm import Session
from app.model.entities import Cart, CartItem, Item
from datetime import datetime
from app.core.database import get_db

router = APIRouter()

def get_or_create_active_cart(user_id: int, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id, Cart.status == "active").first()
    if not cart:
        cart = Cart(user_id=user_id, status="active", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.post("/add-to-cart", response_model=CartItemResponse)
def add_to_cart(item_id: int, quantity: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if quantity <= 0:
        raise HTTPException(400, "Quantity must be positive")

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")

    cart = get_or_create_active_cart(user_id, db)

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.item_id == item_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            item_id=item_id,
            quantity=quantity,
            unit_price=item.price,   # snapshot the price
        )
        db.add(cart_item)

    cart.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/cart")
def get_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart = get_or_create_active_cart(user_id, db)
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    total = sum(ci.unit_price * ci.quantity for ci in items)
    return {"cart_id": cart.id, "status": cart.status, "items": items, "total": total}

@router.put("/cart/items/{item_id}")
def update_cart_item(item_id: int, quantity: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart = get_or_create_active_cart(user_id, db)
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.item_id == item_id
    ).first()
    if not cart_item:
        raise HTTPException(404, "Item not in cart")

    if quantity <= 0:   
        db.delete(cart_item)
    else:
        cart_item.quantity = quantity

    cart.updated_at = datetime.utcnow()
    db.commit()
    return {"detail": "Cart updated"}

@router.delete("/cart/items/{item_id}")
def remove_from_cart(item_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart = get_or_create_active_cart(user_id, db)
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.item_id == item_id
    ).first()
    if not cart_item:
        raise HTTPException(404, "Item not in cart")

    db.delete(cart_item)
    cart.updated_at = datetime.utcnow()
    db.commit()
    return {"detail": "Item removed from cart"}

@router.delete("/delete_cart")
def clear_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart = get_or_create_active_cart(user_id, db)
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    cart.updated_at = datetime.utcnow()
    db.commit()
    return {"detail": "Cart cleared"}

@router.post("/checkout")
def checkout_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart = get_or_create_active_cart(user_id, db)
    if not cart:
        raise HTTPException(404, "No active cart found")

    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not items:
        raise HTTPException(400, "Cart is empty")

    total_amount = sum(ci.unit_price * ci.quantity for ci in items)

    # Here you would typically create an order and process payment
    # For simplicity, we'll just mark the cart as checked out
    cart.status = "checked_out"
    cart.updated_at = datetime.utcnow()
    db.commit()

    return {"detail": "Checkout successful", "total_amount": total_amount}

@router.get("/view-all-items-cart")
def view_all_items_in_cart(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    cart = get_or_create_active_cart(user_id, db)
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    return {"cart_id": cart.id, "status": cart.status, "items": items}