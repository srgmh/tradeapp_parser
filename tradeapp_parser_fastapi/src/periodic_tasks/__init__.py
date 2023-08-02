from src.services.binance_service import BinanceService

binance_websocket = BinanceService()


async def get_binance_websocket() -> BinanceService:
    return binance_websocket
