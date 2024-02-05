# WebSocket URL
import websockets
import asyncio
import json
import pandas as pd
import uuid
from .messages import create_subscription_message, create_unsubscription_message
from .utils import extract_values
from io import StringIO

from .constantes import get_file_paths

longest_json_data = None
longest_json_length = 0

# WebSocket message callback
async def on_message():
    global longest_json_data, longest_json_length
    WEBSOCKET_URL, OUTPUT_EXCEL_PATH, ORDERS_PATH = get_file_paths("20240129")
    df_nemos = pd.read_csv(ORDERS_PATH, sep=";", on_bad_lines='warn')
    symbols_to_process = df_nemos['Nemotécnico'].unique().tolist()
    message_count = 0  # Count the number of messages received
    df = pd.DataFrame(columns=["Symbol", "Last", "AskPx", "BidPx" ])  # Create an empty DataFrame
    async with websockets.connect(WEBSOCKET_URL) as ws:
        print("WebSocket connection established")  # Print verification message
        async for message in ws:
            data = json.loads(message)
            if isinstance(data, dict) and data["topic"] == "securityList":
                # Convert the payload from a JSON string to a dictionary
                data["payload"] = json.loads(data["payload"])
                # Calcula la longitud del JSON
                json_length = len(json.dumps(data))
                # Si este JSON es más largo que el actual más largo, actualiza los datos más largos
                if json_length > longest_json_length:
                    longest_json_data = data
                    longest_json_length = json_length
                print("Longest JSON length: " + str(longest_json_length))
            message_count += 1
            # Close the connection after receiving 3 messages
            if message_count == 3:
                break
        if isinstance(longest_json_data, dict):
            for security in longest_json_data["payload"]["listSecurities"]:
                symbol = security["symbol"]
                if symbol in symbols_to_process:
                    print(f"Processing symbol: {symbol}")
                    df = await process_symbol(ws, symbol, df)
        await ws.close()  # Close WebSocket connection
        print("WebSocket connection closed")  # Print verification message
    # Write the DataFrame to the Excel file
    with pd.ExcelWriter(OUTPUT_EXCEL_PATH, mode="w", engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return

async def process_symbol(ws, symbol, df): 
    uid = str(uuid.uuid4())
    subscription_message = create_subscription_message(symbol, uid)
    await ws.send(json.dumps(subscription_message))
    # Wait for 2 messages for this symbol
    for _ in range(2):
        try:
            message = await asyncio.wait_for(ws.recv(), timeout=1)
        except asyncio.TimeoutError:
            last, askPx, bidPx = None, None, None
            df = df._append({"Symbol": symbol, "Last": last, "AskPx": askPx, "BidPx": bidPx}, ignore_index=True)  # Add the data to the DataFrame
            print(f"Symbol written to Excel: {symbol}, Last: {last}, AskPx: {askPx}, BidPx: {bidPx}")
            break
        data = json.loads(message)
        if isinstance(data, dict) and data["topic"] == "snapshot":
            last, askPx, bidPx = extract_values(data)
            if last is not None and askPx is not None and bidPx is not None:
                df = df._append({"Symbol": symbol, "Last": last, "AskPx": askPx, "BidPx": bidPx}, ignore_index=True)  # Add the data to the DataFrame
                print(f"Symbol written to Excel: {symbol}, Last: {last}, AskPx: {askPx}, BidPx: {bidPx}")
                break
    # Send unsubscription message
    unsubscribe_message = create_unsubscription_message(uid)
    await ws.send(json.dumps(unsubscribe_message))
    return df