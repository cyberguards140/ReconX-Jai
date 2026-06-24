from reconx.api_gateway.responses import SuccessResponse, ErrorResponse, PaginatedResponse

def test_success_response():
    resp = SuccessResponse(data={"key": "value"})
    assert resp.success is True
    assert resp.data == {"key": "value"}
    assert resp.version == "v1"
    assert "timestamp" in resp.model_dump()
    assert "request_id" in resp.model_dump()

def test_error_response():
    resp = ErrorResponse(error_code="TEST_ERROR", message="Test failed")
    assert resp.success is False
    assert resp.error_code == "TEST_ERROR"
    assert resp.message == "Test failed"
    assert resp.details == []

def test_paginated_response():
    resp = PaginatedResponse(
        data=[1, 2, 3],
        meta={"page": 1, "size": 10, "total": 3, "pages": 1}
    )
    assert resp.success is True
    assert len(resp.data) == 3
    assert resp.meta.page == 1
