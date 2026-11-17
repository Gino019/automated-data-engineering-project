-- Curated aggregate consumed by the publicly hosted analytics dashboard.
select
    cast(date_trunc('month', order_ts) as date) as month_start,
    cast(extract(year from order_ts) as integer) as year,
    region,
    category,
    count(*) as order_count,
    sum(quantity) as units_sold,
    round(sum(revenue), 2) as revenue,
    round(sum(profit), 2) as profit
from {{ ref('fct_completed_orders') }}
group by 1, 2, 3, 4
