import sqlalchemy as sa
import enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer, primary_key=True)
    user_name = sa.Column(sa.String, nullable=False)


class ListEnum(enum.Enum):
    default = "default"
    artist = "artist"
    user = "user"


class Lists(Base):
    __tablename__ = "lists"
    list_id = sa.Column(sa.Integer, primary_key=True)
    list_name = sa.Column(sa.String, nullable=False)
    list_type = sa.Column(sa.Enum(ListEnum), server_default="user")
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.user_id"), nullable=False)


class Songs(Base):
    __tablename__ = "songs"
    song_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)


class Binds(Base):
    __tablename__ = "binds"
    list_id = sa.Column(
        sa.Integer, sa.ForeignKey("lists.list_id"), nullable=False, primary_key=True
    )
    song_id = sa.Column(
        sa.Integer, sa.ForeignKey("songs.song_id"), nullable=False, primary_key=True
    )
