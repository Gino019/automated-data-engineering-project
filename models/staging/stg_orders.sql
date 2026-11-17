select
    cast(order_id as integer) as order_id,
    cast(order_ts as timestamp) as order_ts,
    cast(customer_id as integer) as customer_id,
    cast(product_id as integer) as product_id,
    cast(quantity as integer) as quantity,
    cast(unit_price as decimal(12, 2)) as unit_price,
    lower(trim(status)) as order_status
from {{ source('raw', 'orders') }}
