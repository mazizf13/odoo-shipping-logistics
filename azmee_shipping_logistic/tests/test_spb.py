from odoo.tests.common import TransactionCase


class TestSPB(TransactionCase):

    def setUp(self):
        super().setUp()

        warehouse = self.env['stock.warehouse'].search([], limit=1)
        self.spb = self.env['khoer.spb'].create([{
            'warehouse_from_id': warehouse.id,
            'warehouse_to_id': warehouse.id,
        }])

    def test_confirm_spb(self):

        self.spb.action_confirm()

        self.assertEqual(
            self.spb.state,
            'confirmed'
        )