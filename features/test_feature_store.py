from feast import FeatureStore

store = FeatureStore(repo_path=".")

features = store.get_online_features(
    features=[
        "default_features:feature_1",
        "default_features:feature_2",
        "default_features:feature_3",
        "default_features:feature_4",
    ],
    entity_rows=[
        {"entity_id": 1},
    ],
).to_dict()

print(features)
