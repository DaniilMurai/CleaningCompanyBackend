import asyncio

import typer
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from db.crud import UserCRUD
from db.session import async_session

app = typer.Typer()


@app.command()
def createsuperadmin(
        nickname: str = typer.Option(..., prompt=True),
        password: str = typer.Option(..., prompt=True, hide_input=True),
):
    async def run():
        db: AsyncSession
        async with async_session() as db:
            crud = UserCRUD(db)
            user = await crud.create(
                nickname=nickname,
                password=password,
                role=schemas.UserRole.superadmin,
                status=schemas.UserStatus.active,
            )
            typer.echo(f"Superadmin {user.nickname} #{user.id} created!")

    asyncio.run(run())


@app.command()
def test():
    typer.echo("test")


if __name__ == '__main__':
    app()
