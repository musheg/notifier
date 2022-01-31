from copy import deepcopy

from notifier import Notifier
from entities import Company

company_before_update = Company(employees_max=50, employees_min=10, link='test', name='test', crawling_status=0, is_deleted=False, is_blacklisted=False)
company = deepcopy(company_before_update)
company.is_deleted = True
company.crawling_status = 13
n = Notifier(company, company_before_update, "Company")
n.notify()
