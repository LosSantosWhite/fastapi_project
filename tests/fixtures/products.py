import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import Mock


from app.db.postgresql.crud import Table
from tests.factory import Factory


class DataFactory(Factory):
    def __init__(
        self,
        async_session: AsyncSession,
        model: Table,
        data: dict,
    ):
        data = data.get("init_data", {}).get(model.__tablename__ + "s", [])

        super().__init__(async_session, model, data)


@pytest_asyncio.fixture
async def _datas(
    _async_session: AsyncSession,
    _test_data: dict,
):
    async def _method(model: Table):
        factory = DataFactory(
            async_session=_async_session, model=model, data=_test_data
        )
        return await factory.populate_data(many=True)

    return _method


@pytest_asyncio.fixture
async def _data(
    _async_session: AsyncSession,
    _test_data: dict,
):
    async def _method(model: Table):
        factory = DataFactory(
            async_session=_async_session, model=model, data=_test_data
        )
        return await factory.populate_data(many=False)

    return _method


@pytest.fixture
def _mocked_download_function(monkeypatch):
    mock = Mock()
    monkeypatch.setattr("app.modules.products.utils.download.download_file", mock)
    return mock
