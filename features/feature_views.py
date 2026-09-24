from feast import Field
from feast import FeatureView
from feast.types import Float32

from entities import entity
from data_sources import default_source

default_features = FeatureView(
    name="default_features",

    entities=[entity],

    ttl=None,

    schema=[
        Field(name="feature_1", dtype=Float32),
        Field(name="feature_2", dtype=Float32),
        Field(name="feature_3", dtype=Float32),
        Field(name="feature_4", dtype=Float32),
    ],

    source=default_source,
)
