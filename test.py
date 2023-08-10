import httpx


async def make_my_response():
    async with httpx.AsyncClient() as client:
        name = {"name": "new name"}
        with open(
            "./tests/endpoints/products/colors/data/test_image.png", "rb"
        ) as file_obj:
            response = await client.post(
                f"http://localhost:8080/admin/v1/color",
                json=name,
                files={"image": file_obj},
            )
            print(response.json())


import asyncio

asyncio.run(make_my_response())
