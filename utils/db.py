from sqlalchemy.dialects import postgresql


def statement_to_str(statement):
    return statement.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
