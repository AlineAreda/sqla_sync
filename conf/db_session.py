import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker

from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.future.engine import Engine

from models.model_base import ModelBase

__engine: Optional[Engine] = None

def create_engine(sqlite: bool = False) -> Engine:
  """_summary_
  Args:
      sqlite (bool, optional): _description_. Defaults to False.
  Returns:
      Engine: Função para criar a conexão com banco de dados
  """
  global __engine
  
  if __engine:
    return
  
  if sqlite:
    arquivo_db = 'db/picoles.sqlite'
    folder = Path(arquivo_db).parent
    folder.mkdir(parents=True, exist_ok=True)
    
    conn_str = f'sqlite:///{arquivo_db}'
    __engine = sa.create_engine(url=conn_str, echo=False, connect_args={"check_same_thread": False})
  else:
    conn_str = "postgresql://user:password@localhost:5432/picoles"
    __engine = sa.create_engine(url=conn_str, echo=False)
    
  return __engine

def create_session() -> Session:
  """_summary_
  Returns:
      Session: Função para criar a sessão de conexão com banco de dados
  """
  global __engine
  
  if not __engine:
    create_engine()  #create_engine(sqlite=True) para uso do sqlite
    
  __session = sessionmaker(__engine, expire_on_commit=False, class_=Session)
    
  session: Session = __session()
    
  return session

def create_tables() -> None:
  global __engine
  
  if not __engine:
    create_engine(sqlite=True) #create_engine(sqlite=True) para uso do sqlite
    
  import models.all_models
  ModelBase.metadata.drop_all(__engine)
  ModelBase.metadata.create_all(__engine)