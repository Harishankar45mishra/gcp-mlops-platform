from feast import Entity
from feast.value_type import ValueType

iris = Entity(
    name="iris_id",
    join_keys=["iris_id"],
    value_type=ValueType.INT64,
)
