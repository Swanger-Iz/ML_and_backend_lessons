import asyncio
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from queries.core import SyncCore
from queries.orm import AsyncOrm, SyncOrm


def sync_start():
    SyncOrm.create_tables()
    SyncOrm.insert_data_in_WorkersOrm()
    SyncOrm.insert_rows_in_ResumeOrm()
    # SyncOrm.select_workers_with_selectin_relashionship()
    SyncOrm.select_workers_with_condition_relationship()


async def start_script():
    SyncOrm.create_tables()
    await AsyncOrm.insert_data_workers_resumes()
    await AsyncOrm.join_cte_subquery_window_func()


if __name__ == "__main__":
    # asyncio.run(start_script())
    sync_start()
