from locust import HttpUser, task, between
import random


class ExpenseUser(HttpUser):

    # Jeda antar request user
    wait_time = between(1, 3)

    # =========================
    # HALAMAN UTAMA
    # =========================
    @task(3)
    def homepage(self):
        self.client.get("/")

    # =========================
    # DAFTAR PENGELUARAN
    # =========================
    @task(3)
    def expenses(self):
        self.client.get("/expenses")

    # =========================
    # TAMBAH PENGELUARAN
    # =========================
    @task(2)
    def add_expense(self):

        random_amount = random.randint(10000, 500000)

        categories = [
            "Kebutuhan",
            "Keinginan",
            "Tabungan/Investasi",
            "Cicilan"
        ]

        payload = {
            "title": f"Test Expense {random.randint(1,1000)}",
            "amount": random_amount,
            "category": random.choice(categories),
            "created_at": "2026-05-10"
        }

        self.client.post(
            "/expenses/add",
            data=payload
        )

    # =========================
    # DETAIL PENGELUARAN
    # =========================
    @task(1)
    def detail_expense(self):

        expense_id = random.randint(1, 10)

        self.client.get(
            f"/expenses/{expense_id}"
        )

    # =========================
    # EDIT PENGELUARAN
    # =========================
    @task(1)
    def edit_expense(self):

        expense_id = random.randint(1, 10)

        categories = [
            "Kebutuhan",
            "Keinginan",
            "Tabungan/Investasi",
            "Cicilan"
        ]

        payload = {
            "title": f"Edit Expense {random.randint(1,1000)}",
            "amount": random.randint(10000, 300000),
            "category": random.choice(categories),
            "created_at": "2026-05-10"
        }

        self.client.post(
            f"/expenses/edit/{expense_id}",
            data=payload
        )

    # =========================
    # HAPUS PENGELUARAN
    # =========================
    @task(1)
    def delete_expense(self):

        expense_id = random.randint(1, 10)

        self.client.post(
            f"/expenses/delete/{expense_id}"
        )