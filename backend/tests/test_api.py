def test_create_then_list_newest_first(client):
    older = {
        "amount": "10.00",
        "description": "Older lunch",
        "category": "Food",
        "date": "2026-01-01",
    }
    same_day_first = {
        "amount": "3.00",
        "description": "Morning coffee",
        "category": "Food",
        "date": "2026-02-01",
    }
    same_day_second = {
        "amount": "20.50",
        "description": "Train home",
        "category": "Transport",
        "date": "2026-02-01",
    }

    assert client.post("/api/expenses", json=older).status_code == 201
    assert client.post("/api/expenses", json=same_day_first).status_code == 201
    created = client.post("/api/expenses", json=same_day_second)
    assert created.status_code == 201
    assert created.json()["amount"] == "20.50"
    assert created.json()["category"] == "Transport"

    descriptions = [item["description"] for item in client.get("/api/expenses").json()]
    assert descriptions == ["Train home", "Morning coffee", "Older lunch"]


def test_invalid_category_is_rejected(client):
    response = client.post(
        "/api/expenses",
        json={
            "amount": "5.00",
            "description": "Mystery",
            "category": "Nope",
            "date": "2026-10-02",
        },
    )
    assert response.status_code == 422


def test_monthly_total_includes_only_that_month(client):
    for expense in (
        {"amount": "10.00", "description": "Lunch", "category": "Food", "date": "2026-10-02"},
        {"amount": "5.50", "description": "Bus", "category": "Transport", "date": "2026-10-15"},
        {"amount": "100.00", "description": "Rent share", "category": "Housing", "date": "2026-09-30"},
    ):
        assert client.post("/api/expenses", json=expense).status_code == 201

    summary = client.get("/api/summary/monthly", params={"month": "2026-10"})
    assert summary.status_code == 200
    assert summary.json() == {"month": "2026-10", "total": "15.50", "count": 2}


def test_categories_endpoint(client):
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert "Food" in response.json()["categories"]
    assert "Other" in response.json()["categories"]
