from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "postgresql+psycopg2://user:password@localhost/dbname"

app = FastAPI()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Channel(Base):
    __tablename__ = "channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=20), index=True, nullable=False)
    channel_chat_id = Column(String(length=14), nullable=False)


Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# Pydantic reponse models


class ChannelBase(BaseModel):
    name: str
    channel_chat_id: str


# Endpoint to create a new channel
@app.post("/channels/", response_model=ChannelBase)
async def create_channel(channel: ChannelBase, db: Session = Depends(get_db)):
    db_channel = Channel(name=channel.name, channel_chat_id=channel.channel_chat_id)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel


# Endpoint to get a list of all channels
@app.get("/channels/", response_model=list[ChannelBase])
async def get_channels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    channels = db.query(Channel).offset(skip).limit(limit).all()
    return channels


# SQL Alchemy Admin panel
admin = Admin(app, engine)


class ChannelAdmin(ModelView, model=Channel):
    column_list = '__all__'
    name = "Каналы телеграм"
    name_plural = "Каналы телеграм"


admin.add_view(ChannelAdmin)
