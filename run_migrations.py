from alembic.config import CommandLine

if __name__ == "__main__":
    import subprocess

    subprocess.run(["alembic", "revision", "--autogenerate", "-m", "auto"])
    CommandLine().main(argv=["upgrade", "head"])
