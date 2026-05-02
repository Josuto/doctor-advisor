from mcp.server.fastmcp import FastMCP

import logging                                                                                                                                 
logging.getLogger("mcp").setLevel(logging.WARNING) 

mcp = FastMCP("insurance-network")

_doctors = [
    {"name": "Dr. John Smith",       "speciality": "neumology",            "email": "john.smith@city-hospital.com"},
    {"name": "Dr. Jane Doe",         "speciality": "neumology",            "email": "jane.doe@metro-clinic.com"},
    {"name": "Dr. Robert Johnson",   "speciality": "digestive",            "email": "robert.johnson@central-hospital.com"},
    {"name": "Dr. Alice Williams",   "speciality": "ophthalmology",        "email": "alice.williams@eye-care-center.com"},
    {"name": "Dr. Fatima Panisello", "speciality": "general_practitioner", "email": "fatima.panisello@new-hospital.com"},
]


@mcp.tool("fetch_doctors")
def fetch_doctors() -> list[dict]:
    """Return all doctors covered by the insurance network."""
    return _doctors


if __name__ == "__main__":
    mcp.run(transport="stdio")
