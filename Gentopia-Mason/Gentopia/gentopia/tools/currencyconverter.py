import requests
from gentopia.tools import BaseTool, Optional, Type, Any
from pydantic import BaseModel, Field

class CurrencyConverterArgs(BaseModel):
    amount: float = Field(..., description="The amount to convert")
    from_currency: str = Field(..., description="The currency to convert from (e.g., USD)")
    to_currency: str = Field(..., description="The currency to convert to (e.g., INR)")

class CurrencyConverter(BaseTool):
    """Tool that adds the capability to convert currencies using public exchange rates API."""
    
    name = "currency_converter"
    description = ("A currency converter that uses real-time exchange rates. "
                   "Input should be the amount, from_currency, and to_currency.")
    
    args_schema: Optional[Type[BaseModel]] = CurrencyConverterArgs
    
    def _run(self, amount: float, from_currency: str, to_currency: str) -> str:
        base_url = f"https://open.er-api.com/v6/latest/{from_currency}"
        
        try:
            response = requests.get(base_url)
            response.raise_for_status()
            
            data = response.json()
            # Check if the API call was successful
            if data.get('result') == 'success' and to_currency in data['rates']:
                rate = data['rates'][to_currency]
                converted_amount = amount * rate
                return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
            else:
                return "Error: Unable to retrieve exchange rates. Please check your currency codes."
        
        except requests.exceptions.RequestException as e:
            return f"Error: Unable to fetch exchange rates. Details: {str(e)}"
    
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    converter = CurrencyConverter()
    result = converter._run(100, "USD", "INR")
    print(result)
