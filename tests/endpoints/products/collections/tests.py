from unittest.mock import Mock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.collections.crud.models import Collection
from app.modules.products.brands.crud.models import Brand
from tests.utils.assertions import assert_dict_response


class TestCollection:
    base_url = "/collection"
    json_key = "collections"
    model = Collection

    @pytest.mark.asyncio
    @patch("app.modules.products.base.service.download_file")
    async def test_create(
        self,
        _mocked_func: Mock,
        _data: dict,
        _test_data: dict,
        _async_client_as_staff: AsyncClient,
        _async_session: AsyncSession,
        _test_image_entity,
    ):
        payload = _test_data["cases"]["create"]["payload"]
        brand = await _data(model=Brand)

        _mocked_func.return_value = payload["file"]

        response = await _async_client_as_staff.post(
            self.base_url,
            params={"name": payload["name"], "brand_uuid": brand.uuid},
            files={"file": _test_image_entity},
        )
        assert response.status_code == 201

        got = response.json()
        want = _test_data["cases"]["create"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = (
            select(Collection)
            .options(selectinload(Collection.brand))
            .where(Collection.uuid == got["uuid"])
        )

        result = await _async_session.execute(stmt)
        collection = result.scalar_one()

        assert collection
        assert collection.name == want["name"]

    @pytest.mark.asyncio
    async def test_get(
        self,
        _datas: dict,
        _test_data: dict,
        _async_client_as_staff: AsyncClient,
        _async_session: AsyncSession,
    ):
        brands = await _datas(model=Brand)
        collections = await _datas(model=Collection)

        response = await _async_client_as_staff.get(
            f"{self.base_url}/{collections[0].uuid}"
        )
        assert response.status_code == 200

        got = response.json()
        want = _test_data["cases"]["get"]["want"]

        assert_dict_response(got=got, want=want)

    @pytest.mark.asyncio
    async def test_delete(
        self,
        _async_client_as_staff: AsyncClient,
        _async_session: AsyncSession,
        _data: dict,
        _test_data: dict,
    ):
        model = await _data(model=Brand)
        collection = await _data(model=Collection)

        response = await _async_client_as_staff.delete(
            f"{self.base_url}/{collection.uuid}"
        )
        assert response.status_code == 200

        got = response.json()
        want = _test_data["cases"]["delete"]["want"]

        assert_dict_response(got=got, want=want)

    @pytest.mark.asyncio
    async def test_update(
        self,
        _async_client_as_staff: AsyncClient,
        _async_session: AsyncSession,
        _data: dict,
        _test_data: dict,
        _test_image_entity,
    ):
        brand = await _data(model=Brand)
        collection = await _data(model=Collection)

        payload = _test_data["cases"]["patch"]["payload"]
        payload["brand_id"] = brand.uuid
        response = await _async_client_as_staff.patch(
            f"{self.base_url}/{collection.uuid}", params={**payload}
        )

        assert response.status_code == 200

        got = response.json()
        want = _test_data["cases"]["patch"]["want"]

        assert_dict_response(got=got, want=want)
