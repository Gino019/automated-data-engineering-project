-- An empty result set means the test passes.
select order_id
from {{ ref('fct_completed_orders') }}
where revenue < 0 or cost < 0
