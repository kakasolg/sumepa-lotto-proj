
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime

# Base model for SQLAlchemy
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# User Model
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False) # In a real app, this should be hashed
    is_identity_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    wallet_balance: Mapped[float] = mapped_column(Float, default=0.0)
    
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")
    favorite_numbers: Mapped[list["FavoriteNumber"]] = relationship(back_populates="user")

# Game Model
class Game(db.Model):
    __tablename__ = 'game'
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    jackpot: Mapped[str] = mapped_column(String(50))
    ticket_price: Mapped[float] = mapped_column(Float, nullable=False)
    draw_days: Mapped[str] = mapped_column(String(100)) # e.g., "Monday, Wednesday, Saturday"
    next_draw: Mapped[str] = mapped_column(String(100))
    main_numbers_count: Mapped[int] = mapped_column(Integer)
    main_numbers_range_low: Mapped[int] = mapped_column(Integer)
    main_numbers_range_high: Mapped[int] = mapped_column(Integer)
    special_ball_range_low: Mapped[int] = mapped_column(Integer, nullable=True)
    special_ball_range_high: Mapped[int] = mapped_column(Integer, nullable=True)
    special_ball_name: Mapped[str] = mapped_column(String(50), nullable=True) # e.g., "Powerball", "Mega Ball"

# Ticket Model
class Ticket(db.Model):
    __tablename__ = 'ticket'
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    game_id: Mapped[str] = mapped_column(ForeignKey('game.id'), nullable=False)
    numbers: Mapped[str] = mapped_column(String(100), nullable=False)
    special_ball: Mapped[str] = mapped_column(String(10), nullable=True)
    draw_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='active') # active, checked, archived
    purchase_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    winnings: Mapped[float] = mapped_column(Float, default=0.0)
    
    user: Mapped["User"] = relationship(back_populates="tickets")
    game: Mapped["Game"] = relationship()

# Favorite Numbers Model
class FavoriteNumber(db.Model):
    __tablename__ = 'favorite_number'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    game_id: Mapped[str] = mapped_column(ForeignKey('game.id'), nullable=False)
    nickname: Mapped[str] = mapped_column(String(50))
    numbers: Mapped[str] = mapped_column(String(100), nullable=False)
    special_ball: Mapped[str] = mapped_column(String(10), nullable=True)
    
    user: Mapped["User"] = relationship(back_populates="favorite_numbers")
    game: Mapped["Game"] = relationship()
