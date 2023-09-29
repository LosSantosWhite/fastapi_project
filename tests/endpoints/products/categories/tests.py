import pytest

from httpx import AsyncClient
from app.modules.products.categories.crud.models import Category
from tests.utils.assertions import assert_list_response


class TestCategory:
    base_url = "/category"

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        _async_client_as_staff: AsyncClient,
        _datas: Category,
        _test_data: dict,
    ):
        await _datas(model=Category)

        response = await _async_client_as_staff.get(f"{self.base_url}/all")

        assert response.status_code == 200
        want = _test_data["cases"]["get"]["all"]["want"]
        got = response.json()

        assert_list_response(got=got, want=want)

    @pytest.mark.asyncio
    async def test_get(self, _data: Category, _async_client_as_staff: AsyncClient):
        category = await _data(model=Category)

        response = await _async_client_as_staff.get(f"{self.base_url}/{category.id}")

        assert response.status_code == 200
