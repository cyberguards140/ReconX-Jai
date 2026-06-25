from reconx.api_gateway.filtering import get_filter_params
from fastapi import Request

class MockRequest:
    def __init__(self, query_params):
        class MockQueryParams:
            def __init__(self, params):
                self.params = params
            def multi_items(self):
                for k, v in self.params.items():
                    if isinstance(v, list):
                        for item in v:
                            yield k, item
                    else:
                        yield k, v
        self.query_params = MockQueryParams(query_params)

def test_get_filter_params():
    req = MockRequest({"type": "domain", "risk_score__gte": "80", "page": "1", "tags": ["a", "b"]})
    params = get_filter_params(req) # type: ignore
    filters = params.to_dict()
    assert "page" not in filters
    assert filters["type"] == "domain"
    assert filters["risk_score__gte"] == "80"
    assert filters["tags"] == ["a", "b"]
