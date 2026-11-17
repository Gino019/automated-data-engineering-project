select
    o.order_id,
    o.order_ts,
    cast(o.order_ts as date) as order_date,
    o.customer_id,
    c.region,
    c.segment,
    p.category,
    p.product_name,
    o.quantity,
    round(o.quantity * o.unit_price, 2) as revenue,
    round(o.quantity * p.unit_cost, 2) as cost,
    round(o.quantity * (o.unit_price - p.unit_cost), 2) as profit
from {{ ref('stg_orders') }} o
inner join {{ ref('stg_customers') }} c on o.customer_id = c.customer_id
inner join {{ ref('stg_products') }} p on o.product_id = p.product_id
where o.order_status = 'completed'
