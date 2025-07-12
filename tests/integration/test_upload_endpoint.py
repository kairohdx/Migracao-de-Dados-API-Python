import pytest


@pytest.mark.asyncio
async def test_upload_txt_file(client):
    content = (
        b"0000000081                                 Tad O'Conner00000008780000000003      231.9720211211\n"
        b"0000000041                           Dr. Dexter Rolfson00000004470000000003     1563.4720210630"
    )
    response = client.post(
        "/api/v1/migration/upload",
        files={"file": ("dados.txt", content, "text/plain")}
    )
    assert response.status_code == 200
    assert response.json()
    