import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services import MigrationDataService

@pytest.fixture
def mocked_repositories():
    return {
        "user_repo": AsyncMock(),
        "item_repo": AsyncMock(),
        "order_repo": AsyncMock(),
    }

@pytest.mark.asyncio
async def test_process_and_save_lines(mocked_repositories):
    service = MigrationDataService(
        user_repository=mocked_repositories["user_repo"],
        order_item_repository=mocked_repositories["item_repo"],
        order_repository=mocked_repositories["order_repo"]
    )

    file_mock = AsyncMock()
    file_mock.read.return_value = b"0000000074                            Mallory Murray IV00000007930000000002      283.2920210316\n"

    await service.process_and_save_lines(file_mock)

    assert mocked_repositories["user_repo"].bulk_insert_users.call_count >= 1
    assert mocked_repositories["order_repo"].bulk_insert_orders.call_count >= 1
    assert mocked_repositories["item_repo"].bulk_insert_order_items.call_count >= 1
