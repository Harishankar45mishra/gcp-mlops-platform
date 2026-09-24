from feast import FileSource

default_source = FileSource(
    path="data/default.parquet",
    timestamp_field="event_timestamp",
)
