from domain.model import RestockBatch, OrderLine
from datetime import date


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return (
        RestockBatch("test-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )


def test_allocating_reduces_available_quantity():
    batch = RestockBatch("test-001", "book", qty=20, eta=date.today())
    line = OrderLine("order-123", "book", qty=2)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_cannot_allocate_if_sku_do_not_match():
    batch = RestockBatch("test-001", "book", 20, eta=date.today())
    diffrent_sku_line = OrderLine("order-123", "notebook", 20)
    assert batch.can_allocate(diffrent_sku_line) is False


def test_can_allocate_if_available_greter_than_required():
    large_batch, small_line = make_batch_and_line("book", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_can_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("book", 2, 20)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_than_required():
    equal_batch, equal_line = make_batch_and_line("book", 20, 20)
    assert equal_batch.can_allocate(equal_line)


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("book", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20
