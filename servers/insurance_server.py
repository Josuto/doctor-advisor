import sqlite3

from mcp.server.fastmcp import FastMCP
from servers.insurance_directory import DB_PATH

import logging                                                                                                                                 
logging.getLogger("mcp").setLevel(logging.WARNING)    

mcp = FastMCP("insurance-network")


@mcp.tool("fetch_doctors")
def fetch_doctors() -> list[dict]:
    """Return all doctors covered by the insurance network."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT name, speciality, email FROM doctors").fetchall()
    return [dict(row) for row in rows]


if __name__ == "__main__":
    mcp.run(transport='stdio')
