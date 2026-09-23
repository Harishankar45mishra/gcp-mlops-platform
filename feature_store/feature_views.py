from feast import Field
from feast import FeatureView
from feast.types import Float32

from entities import iris
from data_sources import iris_source

iris_features = FeatureView(
    name="iris_features",

    entities=[iris],

    ttl=None,

    schema=[
        Field(name="sepal_length", dtype=Float32),
        Field(name="sepal_width", dtype=Float32),
        Field(name="petal_length", dtype=Float32),
        Field(name="petal_width", dtype=Float32),
    ],

    source=iris_source,
)
