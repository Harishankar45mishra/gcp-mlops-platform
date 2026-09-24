from feast import Entity
from feast.value_type import ValueType

entity = Entity(
    name="entity_id",
    join_keys=["entity_id"],
    value_type=ValueType.INT64,
)
