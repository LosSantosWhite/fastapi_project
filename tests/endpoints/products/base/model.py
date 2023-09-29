from io import BufferedReader
from typing import List, Type
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from typing import Generic
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgresql.crud import Table
from app.external.s3.service import S3_Service
from tests.utils.assertions import assert_dict_response, assert_list_response
from app.config import config


async def return_image_path(*args, **kwargs):
    return (
        f"{config.s3.endpoint_url}/{config.s3.bucket_name}/{kwargs['file_uuid']}.webp"
    )


class Base(Generic[Table]):
    """Tests for brand endpoints."""

    base_url = f"v1/products"
    json_key = ""
    model: Type[Table] = None

    # |Tests|
    @pytest.mark.asyncio
    @patch.object(S3_Service, "upload_file", return_image_path)
    async def test_create(
        self,
        # _mocked_download_file: Mock,
        _async_session: "AsyncSession",
        _test_data: dict,
        _test_image_entity: BufferedReader,
        _async_client_as_staff: "AsyncClient",
    ):
        payload = _test_data["cases"]["create"]["payload"]
        # _mocked_download_file.return_value = payload["file"]

        response = await _async_client_as_staff.post(
            f"{self.base_url}",
            params=dict(name=payload["name"]),
            files={"file": _test_image_entity},
        )
        assert response.status_code == 201
        got = response.json()

        want = _test_data["cases"]["create"]["want"]
        want["file"] = await return_image_path(file_uuid=got["uuid"])
        assert_dict_response(got=got, want=want)
        stmt = select(self.model).where(self.model.uuid == got["uuid"])

        result = await _async_session.execute(stmt)
        entity: Table = result.scalar_one()

        assert entity

    @pytest.mark.asyncio
    async def test_get(
        self,
        _async_client_as_staff: "AsyncClient",
        _test_data: "dict",
        _async_session: "AsyncSession",
        _data: Table,
    ):
        entity = await _data(model=self.model)
        response = await _async_client_as_staff.get(f"{self.base_url}/{entity.uuid}")
        assert response.status_code == 200
        got = response.json()
        want = _test_data["cases"]["get"]["want"]
        assert_dict_response(got=got, want=want)
        stmt = select(self.model).where(self.model.uuid == got["uuid"])
        result = await _async_session.execute(stmt)
        entity: Table = result.scalar_one()
        assert entity

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        _async_client_as_staff: "AsyncClient",
        _test_data: "dict",
        _datas: List[Table],
    ):
        entities = await _datas(model=self.model)
        response = await _async_client_as_staff.get(f"{self.base_url}/all")

        assert response.status_code == 200
        got = response.json()

        want = _test_data["init_data"][self.json_key]
        assert_list_response(got=got, want=want)

        assert len(entities) == len(got)

    @pytest.mark.asyncio
    @patch("app.modules.products.base.service.download_file")
    async def test_patch(
        self,
        _mocked_download_file: "Mock",
        _async_client_as_staff: "AsyncClient",
        _data: "Table",
        _test_data: "dict",
        _async_session: "AsyncSession",
    ):
        payload = _test_data["cases"]["patch"]["payload"]
        _mocked_download_file.return_value = _test_data["init_data"][self.json_key][0][
            "file"
        ]

        entity: Table = await _data(model=self.model)

        response = await _async_client_as_staff.patch(
            f"{self.base_url}/{entity.uuid}?name={payload['name']}"
        )
        assert response.status_code == 200

        got = response.json()
        want = _test_data["cases"]["patch"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = select(self.model).where(self.model.uuid == entity.uuid)

        result = await _async_session.execute(stmt)
        entity: Table = result.scalar_one()

        assert entity.name == got["name"]
        assert entity.file == want["file"]

    @pytest.mark.asyncio
    async def test_delete(
        self,
        _async_client_as_staff: "AsyncClient",
        _data: "Table",
        _test_data: dict,
        _async_session: "AsyncSession",
    ):
        entity = await _data(model=self.model)

        response = await _async_client_as_staff.delete(f"{self.base_url}/{entity.uuid}")
        assert response.status_code == 200

        got = response.json()

        want = _test_data["cases"]["delete"]["want"]

        assert_dict_response(got=got, want=want)

        stmt = select(self.model).where(self.model.uuid == entity.uuid)
        result = await _async_session.execute(stmt)
        assert result.scalar() == None
