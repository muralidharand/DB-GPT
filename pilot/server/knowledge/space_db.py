from datetime import datetime

from sqlalchemy import Column, Integer, Text, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pilot.configs.config import Config
from pilot.server.knowledge.request.request import KnowledgeSpaceRequest
from pilot.connections.rdbms.base_dao import BaseDao

CFG = Config()
Base = declarative_base()


class KnowledgeSpaceEntity(Base):
    __tablename__ = "knowledge_space"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    vector_type = Column(String(100))
    desc = Column(String(100))
    owner = Column(String(100))
    context = Column(Text)
    gmt_created = Column(DateTime)
    gmt_modified = Column(DateTime)

    def __repr__(self):
        return f"KnowledgeSpaceEntity(id={self.id}, name='{self.name}', vector_type='{self.vector_type}', desc='{self.desc}', owner='{self.owner}' context='{self.context}', gmt_created='{self.gmt_created}', gmt_modified='{self.gmt_modified}')"


class KnowledgeSpaceDao(BaseDao):
    def __init__(self):
        super().__init__(
            database="knowledge_management", orm_base=Base, create_not_exist_table=True
        )

    def create_knowledge_space(self, space: KnowledgeSpaceRequest):
        session = self.Session()
        knowledge_space = KnowledgeSpaceEntity(
            name=space.name,
            vector_type=CFG.VECTOR_STORE_TYPE,
            desc=space.desc,
            owner=space.owner,
            gmt_created=datetime.now(),
            gmt_modified=datetime.now(),
        )
        session.add(knowledge_space)
        session.commit()
        session.close()

    def get_knowledge_space(self, query: KnowledgeSpaceEntity):
        session = self.Session()
        knowledge_spaces = session.query(KnowledgeSpaceEntity)
        if query.id is not None:
            knowledge_spaces = knowledge_spaces.filter(
                KnowledgeSpaceEntity.id == query.id
            )
        if query.name is not None:
            knowledge_spaces = knowledge_spaces.filter(
                KnowledgeSpaceEntity.name == query.name
            )
        if query.vector_type is not None:
            knowledge_spaces = knowledge_spaces.filter(
                KnowledgeSpaceEntity.vector_type == query.vector_type
            )
        if query.desc is not None:
            knowledge_spaces = knowledge_spaces.filter(
                KnowledgeSpaceEntity.desc == query.desc
            )
        if query.owner is not None:
            knowledge_spaces = knowledge_spaces.filter(
                KnowledgeSpaceEntity.owner == query.owner
            )
        if query.gmt_created is not None:
            knowledge_spaces = knowledge_spaces.filter(
                KnowledgeSpaceEntity.gmt_created == query.gmt_created
            )
        if query.gmt_modified is not None:
            knowledge_spaces = knowledge_spaces.filter(
                KnowledgeSpaceEntity.gmt_modified == query.gmt_modified
            )

        knowledge_spaces = knowledge_spaces.order_by(
            KnowledgeSpaceEntity.gmt_created.desc()
        )
        result = knowledge_spaces.all()
        session.close()
        return result

    def update_knowledge_space(self, space: KnowledgeSpaceEntity):
        session = self.Session()
        session.merge(space)
        session.commit()
        session.close()
        return True

    def delete_knowledge_space(self, space: KnowledgeSpaceEntity):
        session = self.Session()
        if space:
            session.delete(space)
            session.commit()
        session.close()
