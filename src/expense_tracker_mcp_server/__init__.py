from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date: str, amount: float, category: str, subcategory: str = "", note: str = "") -> dict:
    '''Add a new expense entry to the database.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}
    
@mcp.tool()
def list_expenses(start_date: str, end_date: str) -> list[dict]:
    '''List expense entries within an inclusive date range (YYYY-MM-DD).'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date: str, end_date: str, category: str = None) -> list[dict]:
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def update_expense(expense_id: int, date: str = None, amount: float = None, category: str = None, subcategory: str = None, note: str = None) -> dict:
    '''Update an existing expense entry by its ID. Only provided fields will be updated.'''
    with sqlite3.connect(DB_PATH) as c:
        # Pehle check karein ki entry exist karti hai ya nahi
        cur = c.execute("SELECT id, date, amount, category, subcategory, note FROM expenses WHERE id = ?", (expense_id,))
        row = cur.fetchone()
        if not row:
            return {"status": "error", "message": f"Expense with ID {expense_id} not found."}
        
        # Current values se default bhar dein agar nayi value na di gayi ho
        curr_date, curr_amount, curr_category, curr_subcategory, curr_note = row[1], row[2], row[3], row[4], row[5]
        
        new_date = date if date is not None else curr_date
        new_amount = amount if amount is not None else curr_amount
        new_category = category if category is not None else curr_category
        new_subcategory = subcategory if subcategory is not None else curr_subcategory
        new_note = note if note is not None else curr_note

        c.execute(
            """
            UPDATE expenses
            SET date = ?, amount = ?, category = ?, subcategory = ?, note = ?
            WHERE id = ?
            """,
            (new_date, new_amount, new_category, new_subcategory, new_note, expense_id)
        )
        return {"status": "ok", "message": f"Expense ID {expense_id} updated successfully."}

@mcp.tool()
def delete_expense(expense_id: int) -> dict:
    '''Delete an expense entry by its ID.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        if cur.rowcount == 0:
            return {"status": "error", "message": f"Expense with ID {expense_id} not found."}
        return {"status": "ok", "message": f"Expense ID {expense_id} deleted successfully."}

@mcp.resource("expense://categories", mime_type="application/json")
def categories() -> str:
    '''Read categories dynamically from categories.json file.'''
    if not os.path.exists(CATEGORIES_PATH):
        return '["Food", "Travel", "Utilities", "Entertainment", "Shopping"]'
    
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()