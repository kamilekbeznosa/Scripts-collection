import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement import models
from datetime import datetime, timedelta, timezone

def get_azure_costs(subscription_id: str, is_dry_run: bool = False) -> str:
    """
    Pobiera koszty Azure. Jeśli is_dry_run jest True lub ustawiono zmienną środowiskową,
    zwraca symulowane dane (mock).
    """

    if is_dry_run or os.getenv("USE_MOCK_DATA") == "true":
        return ("Koszty za ostatnie 30 dni (SYMULACJA):\n"
                "- Virtual Machines: 120.50 USD\n"
                "- Storage: 45.20 USD\n"
                "- Networking: 12.00 USD\n"
                "Suma: 177.70 USD")

    credential = DefaultAzureCredential()
    client = CostManagementClient(credential=credential)
    
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=30)
    
    query = models.QueryDefinition(
        type="Usage",
        timeframe="Custom",
        time_period=models.QueryTimePeriod(from_property=start_date, to=end_date),
        dataset={
            "granularity": "Daily",
            "grouping": [{"type": "Dimension", "name": "ResourceGroup"}] 
        }
    )
    
    scope = f"/subscriptions/{subscription_id}"
    response = client.query.usage(scope=scope, parameters=query)
    
    return "Raport wygenerowany pomyślnie z Azure API."