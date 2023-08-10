from io import BufferedReader
from typing import List
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.crud.models import Brand
from app.modules.products.utils import download
from tests.utils.assertions import assert_dict_response, assert_list_response


class TestBrand:
    """Tests for brand endpoints."""

    base_url = f"v1/brand"

    # |Tests|
    @pytest.mark.asyncio
    @patch("app.modules.products.brands.api.v1.endpoints.download_file")
    async def test_create(
        self,
        _mocked_download_file: Mock,
        _async_session: "AsyncSession",
        _test_data: dict,
        _test_image_entity: BufferedReader,
        _async_client_as_staff: "AsyncClient",
    ):
        payload = _test_data["cases"]["create"]["payload"]
        _mocked_download_file.return_value = payload["image_path"]

        response = await _async_client_as_staff.post(
            f"{self.base_url}?name={payload['name']}",
            files={"file": _test_image_entity},
        )
        print(response.json())
        assert response.status_code == 201

        got = response.json()
        want = _test_data["cases"]["create"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = select(Brand).where(Brand.uuid == got["uuid"])
        result = await _async_session.execute(stmt)
        brand: Brand = result.scalar_one()

        assert brand

    @pytest.mark.asyncio
    async def test_get(
        self,
        _async_client_as_staff: "AsyncClient",
        _test_data: "dict",
        _async_session: "AsyncSession",
        _data: "Brand",
    ):
        brand = await _data(model=Brand)

        response = await _async_client_as_staff.get(f"{self.base_url}/{brand.uuid}")

        assert response.status_code == 200
        got = response.json()

        want = _test_data["cases"]["get"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = select(Brand).where(Brand.uuid == got["uuid"])
        result = await _async_session.execute(stmt)

        brand: Brand = result.scalar_one()
        assert brand

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        _async_client_as_staff: "AsyncClient",
        _test_data: "dict",
        _datas: List["Brand"],
    ):
        brands = await _datas(model=Brand)
        response = await _async_client_as_staff.get(f"{self.base_url}/all")
        assert response.status_code == 200
        got = response.json()

        want = _test_data["init_data"]["brands"]
        assert_list_response(got=got, want=want)

        assert len(brands) == len(got)

    @pytest.mark.asyncio
    @patch("app.modules.products.brands.api.v1.endpoints.download_file")
    async def test_patch(
        self,
        _mocked_download_file: "Mock",
        _async_client_as_staff: "AsyncClient",
        _data: "Brand",
        _test_data: "dict",
        _async_session: "AsyncSession",
    ):
        payload = _test_data["cases"]["patch"]["payload"]
        _mocked_download_file.return_value = _test_data["init_data"]["brands"][0][
            "image_path"
        ]

        brand: Brand = await _data(model=Brand)

        response = await _async_client_as_staff.patch(
            f"{self.base_url}/{brand.uuid}?name={payload['name']}"
        )
        assert response.status_code == 200

        got = response.json()
        want = _test_data["cases"]["patch"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = select(Brand).where(Brand.uuid == Brand.uuid)

        result = await _async_session.execute(stmt)
        print(result)
        brand: Brand = result.scalar_one()

        assert brand.name == got["name"]
        assert brand.image_path == want["image_path"]
