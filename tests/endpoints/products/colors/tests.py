from io import BufferedReader
from typing import List
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.products.crud.models import Color
from app.modules.products.utils import download
from tests.utils.assertions import assert_dict_response, assert_list_response


class TestColor:
    """Tests for color endpoints."""

    base_url = f"v1/color"

    # |Tests|
    @pytest.mark.asyncio
    @patch("app.modules.products.colors.api.v1.endpoints.download_file")
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

        assert response.status_code == 201

        got = response.json()
        want = _test_data["cases"]["create"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = select(Color).where(Color.uuid == got["uuid"])
        result = await _async_session.execute(stmt)
        color: Color = result.scalar_one()

        assert color

    @pytest.mark.asyncio
    async def test_get(
        self,
        _async_client_as_staff: "AsyncClient",
        _test_data: "dict",
        _async_session: "AsyncSession",
        _data: "Color",
    ):
        color = await _data(model=Color)

        response = await _async_client_as_staff.get(f"{self.base_url}/{color.uuid}")

        assert response.status_code == 200
        got = response.json()

        want = _test_data["cases"]["get"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = select(Color).where(Color.uuid == got["uuid"])
        result = await _async_session.execute(stmt)

        color: Color = result.scalar_one()
        assert color

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        _async_client_as_staff: "AsyncClient",
        _test_data: "dict",
        _datas: List["Color"],
    ):
        colors = await _datas(model=Color)
        response = await _async_client_as_staff.get(f"{self.base_url}/all")
        assert response.status_code == 200
        got = response.json()

        want = _test_data["init_data"]["colors"]
        assert_list_response(got=got, want=want)

        assert len(colors) == len(got)

    @pytest.mark.asyncio
    @patch("app.modules.products.colors.api.v1.endpoints.download_file")
    async def test_patch_color(
        self,
        _mocked_download_file: "Mock",
        _async_client_as_staff: "AsyncClient",
        _data: "Color",
        _test_data: "dict",
        _async_session: "AsyncSession",
    ):
        payload = _test_data["cases"]["patch"]["payload"]
        _mocked_download_file.return_value = _test_data["init_data"]["colors"][0][
            "image_path"
        ]

        color: Color = await _data(model=Color)

        response = await _async_client_as_staff.patch(
            f"{self.base_url}/{color.uuid}?name={payload['name']}"
        )
        assert response.status_code == 200

        got = response.json()
        want = _test_data["cases"]["patch"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = select(Color).where(Color.uuid == color.uuid)

        result = await _async_session.execute(stmt)
        print(result)
        color: Color = result.scalar_one()

        assert color.name == got["name"]
        assert color.image_path == want["image_path"]
