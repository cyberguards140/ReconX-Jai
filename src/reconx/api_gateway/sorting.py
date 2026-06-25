from fastapi import Query
from pydantic import BaseModel


class SortField(BaseModel):
    field: str
    descending: bool


class SortParams(BaseModel):
    sorts: list[SortField]


def get_sort_params(
    sort: str | None = Query(
        None, description="Comma-separated fields to sort by. Prefix with '-' for descending."
    ),
) -> SortParams:
    """
    Extracts sorting parameters.
    Example: ?sort=-risk_score,created_at
    """
    sorts = []
    if sort:
        for field in sort.split(","):
            field = field.strip()
            if not field:
                continue
            if field.startswith("-"):
                sorts.append(SortField(field=field[1:], descending=True))
            elif field.startswith("+"):
                sorts.append(SortField(field=field[1:], descending=False))
            else:
                sorts.append(SortField(field=field, descending=False))
    return SortParams(sorts=sorts)
