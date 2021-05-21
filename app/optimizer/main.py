from orders.models import Orders
from optimizer.models import Route
from optimizer.opt.optimizer import Optimizer

fetch_all_orders = Orders.objects.all()



def _optimize_orders():
    pass
