from fastapi import FastAPI, HTTPException
from kiteconnect import KiteConnect
import json

app = FastAPI()

API_KEY = "your_api_key"
ACCESS_TOKEN = "your_access_token"
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

@app.get("/option-chain/{symbol}")
def get_option_chain(symbol: str):
    try:
        instruments = kite.instruments("NFO")
        option_chain = [inst for inst in instruments 
                        if inst.get('name') == symbol and inst.get('segment') == 'NFO-OPT']
        
        if not option_chain:
            raise HTTPException(status_code=404, detail="Option chain not found")
        return json.loads(json.dumps(option_chain, default=str))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/open-interest/{symbol}")
def get_open_interest(symbol: str):
    try:
        oi_data = kite.ltp(f'NFO:{symbol}')
        
        if f'NFO:{symbol}' not in oi_data:
            raise HTTPException(status_code=404, detail="Symbol not found")
        
        return {"symbol": symbol, "open_interest": oi_data[f'NFO:{symbol}']['last_price']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
