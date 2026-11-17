select
    cast(customer_id as integer) as customer_id,
    trim(region) as region,
    trim(segment) as segment
from {{ source('raw', 'customers') }}
