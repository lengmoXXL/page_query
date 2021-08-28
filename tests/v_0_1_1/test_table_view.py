from rich.console import COLOR_SYSTEMS, Console
from rich.table import Table, Column


def test_table_view():
    table = Table(
        Column("Title", style='green'),
        Column("Tags"),
        Column("Summary"),
        Column("Urls"),
    )

    table.add_row("grep process 混入了一个中文 with pid in linux"*5, "linux,process", 'ps aux | grep <pid>'*10, '- https://some-url')

    console = Console(width=150)
    console.print(table)

    assert False, 'assert false to view table'