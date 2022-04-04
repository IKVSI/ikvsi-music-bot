import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = sa.Column(sa.Integer, primary_key=True)


class Lists(Base):
    __tablename__ = "lists"
    list_id = sa.Column(sa.Integer, primary_key=True)
    list_name = sa.Column(sa.String, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.user_id"), nullable=False)


class Songs(Base):
    __tablename__ = "songs"
    song_id = sa.Column(sa.Integer, primary_key=True)
    song_name = sa.Column(sa.String, nullable=False)
    artist = sa.Column(sa.String, nullable=False)


class Binds(Base):
    __tablename__ = "binds"
    bind_id = sa.Column(sa.Integer, primary_key=True)
    list_id = sa.Column(sa.Integer, sa.ForeignKey("lists.list_id"), nullable=False)
    song_id = sa.Column(sa.Integer, sa.ForeignKey("songs.song_id"), nullable=False)
