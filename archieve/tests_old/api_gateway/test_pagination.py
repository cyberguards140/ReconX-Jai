from reconx.api_gateway.pagination import calculate_pagination_meta, PaginationParams

def test_calculate_pagination_meta():
    meta = calculate_pagination_meta(page=2, size=50, total=150)
    assert meta["page"] == 2
    assert meta["size"] == 50
    assert meta["total"] == 150
    assert meta["pages"] == 3
    
def test_calculate_pagination_meta_zero_total():
    meta = calculate_pagination_meta(page=1, size=50, total=0)
    assert meta["pages"] == 1

def test_pagination_params():
    params = PaginationParams(page=2, size=20)
    assert params.offset == 20
    assert params.limit == 20
