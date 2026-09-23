from feast import FileSource

iris_source = FileSource(
    path="data/iris.parquet",
    timestamp_field="event_timestamp",
)
