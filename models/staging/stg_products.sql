select
    cast(product_id as integer) as product_id,
    trim(product_name) as product_name,
    trim(category) as category,
    cast(unit_cost as decimal(12,2)) as unit_cost
from {{ source('raw', 'products') }}
