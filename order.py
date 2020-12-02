class Order:
    def __init__(self, customer, staff):
        self.customer = customer
        self.received_by = staff
        self.order_date = None
        self.payment_method = None
        self.billing_address = None
        self.shipping_cost = None
        self.tax_cost = None
        self.total_cost = None
