from app.services.scipy_wrapper import (
    execute_afc,
    execute_acm,
    execute_cah,
    execute_kmeans,
)


def test_execute_afc_returns_expected_keys():
    # Simple 2x2 contingency table
    table = [[10, 20], [30, 40]]
    result = execute_afc(table)
    assert isinstance(result, dict)
    for key in ["row_coordinates", "col_coordinates", "explained_inertia"]:
        assert key in result
    # Verify types
    assert isinstance(result["row_coordinates"], list)
    assert isinstance(result["col_coordinates"], list)
    assert isinstance(result["explained_inertia"], list)


def test_execute_acm_returns_expected_keys():
    # Indicator matrix for 3 categorical variables (one-hot encoded)
    matrix = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]
    result = execute_acm(matrix)
    assert isinstance(result, dict)
    for key in ["coordinates", "explained_inertia"]:
        assert key in result
    assert isinstance(result["coordinates"], list)
    assert isinstance(result["explained_inertia"], list)


def test_execute_cah_returns_labels_and_linkage():
    data = [[0, 0], [1, 1], [5, 5], [6, 5]]
    result = execute_cah(data, n_clusters=2, linkage_method="ward")
    assert isinstance(result, dict)
    assert "labels" in result and "linkage_matrix" in result
    assert isinstance(result["labels"], list)
    assert isinstance(result["linkage_matrix"], list)
    # Expect exactly 2 clusters
    assert len(set(result["labels"])) == 2


def test_execute_kmeans_returns_centers_labels_inertia():
    data = [[0, 0], [1, 1], [5, 5], [6, 5]]
    result = execute_kmeans(data, n_clusters=2, max_iter=100, init="k-means++")
    assert isinstance(result, dict)
    for key in ["centers", "labels", "inertia"]:
        assert key in result
    assert isinstance(result["centers"], list)
    assert isinstance(result["labels"], list)
    assert isinstance(result["inertia"], float)
    # Should produce exactly 2 cluster centers
    assert len(result["centers"]) == 2
