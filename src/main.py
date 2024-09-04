from queries.orm import SyncOrm
from queries.core import SyncCore

# SyncCore.create_tables()
# SyncCore.insert_data()
# SyncCore.read_all()
# SyncCore.update_name()
# SyncCore.read_all()

SyncOrm.create_tables()
SyncOrm.insert_data()
SyncOrm.update(2, 'pidor')
SyncOrm.read_all()
SyncOrm.insert_resumes()
SyncOrm.select_resumes_avg_compensation_by_workload('python')
SyncOrm.join_cte_subquery_window_func()