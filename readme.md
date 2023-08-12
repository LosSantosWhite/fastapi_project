# API for creating product

## Stack

<ul>
<li> Python 3.10
<li> FastAPI
<li> PostgresSQL
<li> SQLAlchemy:
    <ul>
    <li> Alembic
    <li> asyncpg
    </ul>
<li> Redis
<li> Celery
<li> Poetry
</ul>

## Description

API based on 5 SQL-models:

<ul>
<li>Brand (exm. "Apple")
<li>Category (exm. "Phone")
<li>Collection (exm. "Red Product")
<li>Color (exm. "Green")
<li>Images
<li>Model (exm. "iPhone 12")

</ul>

You can find them in `app/modules/products/crud/models`

## Admin API routers

### Brand

To create:

    Method: POST;
    url: /admin/v1/products/brand

To get one/all

    Method: GET;
    URL: /admin/v1/products/brand/{brand_uuid};
    /admin/v1/products/brand/all

To update:

    Method: UPDATE;
    URL: /admin/v1/products/brand/{brand_uuid}

To delete:

    Method: DELETE;
    URL: /admin/v1/products/brand/{brand_uuid}

### Color

To create:

    Method: POST;
    url: /admin/v1/products/color

To get one/all

    Method: GET;
    URL: /admin/v1/products/color/{color_uuid};
    /admin/v1/products/color/all

To update:

    Method: UPDATE;
    URL: /admin/v1/products/color/{color_uuid}

To delete:

    Method: DELETE;
    URL: /admin/v1/products/color/{color_uuid}
