from sqlalchemy import Select


class Paginator:

    @staticmethod
    def add_pagination_rules(stmt: Select, skip: int, limit: int | None = None):
        stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)
        return stmt
