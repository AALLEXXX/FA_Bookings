import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,booked_rooms, status_code",
    *[
        [(4, "2024-04-08", "2024-04-15", i, 201) for i in range(3, 11)]
        + [(4, "2024-04-08", "2024-04-15", 10, 409)] * 2
    ]
)

async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "v1/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code

    response = await authenticated_ac.get("v1/bookings")

    assert len(response.json()) == booked_rooms


@pytest.mark.parametrize("status_code", [200])
async def test_get_delete_get_bookings(
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.get("v1/bookings")
    assert response.status_code == 200
    for booking in response.json():
        book_id = booking["id"]
        delete_response = await authenticated_ac.delete(
            f"v1/bookings/{book_id}"
        )
        assert delete_response.status_code == 204

    response = await authenticated_ac.get("v1/bookings")
    assert len(response.json()) == 0
