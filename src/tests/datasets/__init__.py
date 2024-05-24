import pytest
import src.models as models

from sqlalchemy.orm import Session
from src.tests import engine

from src.database import Base
from src.utils.webtokens import hash_password


class Dataset:
    def __init__(self):
        print("new dataset")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.session: Session = Session(bind=engine)

    def create_user(self, mail: str, username: str, password: str):
        user = models.Users(
            mail=mail, username=username, password=hash_password(password)
        )
        user.__setattr__("password_nonhashed", password)
        self.session.add(user)
        return user


@pytest.fixture
def dataset():
    ds = Dataset()
    ds.user_1 = ds.create_user(
        mail="user1@pytest.io", username="user1", password="00agh!&à"
    )

    ds.session.commit()
    return ds
