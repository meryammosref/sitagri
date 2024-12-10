from datetime import datetime
import requests
import json
import asyncio
import websockets
import pyodbc



data_array = []



def connect_to_sql_server():
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=IXIA-DSI-GHASSE\SQLEXPRESS;"
            "Database=sitagri;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        print("Successfully connected to SQL Server")
        return conn, cursor
    except Exception as e:
        print(f"Failed to connect to SQL Server: {e}")
        return None, None

conn, cursor = connect_to_sql_server()


async def get_websocket_messages():
    global data_array

    try:
        # Fetch the list of available DevTools sessions
        response = requests.get('http://localhost:9222/json')
        tabs = response.json()

        search_keyword = 'sitagrimobile'
        target_tab = None
        for tab in tabs:
            if search_keyword in tab['url']:
                target_tab = tab['id']
                break

        if not target_tab:
            raise Exception("Target tab not found")

        print(target_tab)

        # Connect to the WebSocket endpoint for the target tab
        ws_url = f"ws://localhost:9222/devtools/page/{target_tab}"
        async with websockets.connect(ws_url) as websocket:
            # Enable network domain to capture WebSocket messages
            await websocket.send(json.dumps({"id": 1, "method": "Network.enable"}))
            # Capture WebSocket frames
            await websocket.send(json.dumps({"id": 2, "method": "Network.webSocketFrameReceived"}))

            # Get Data
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    print(data)
                    if 'method' in data and data['method'] == "Network.webSocketFrameReceived" and 'quote' in data['params']['response']['payloadData'] and 'last' in data['params']['response']['payloadData']:
                        payload_data_str = data['params']['response']['payloadData']
                        payload_data = json.loads(payload_data_str)

                        quote = payload_data['data']['quote']
                        last_slash_index = quote.rfind('/')
                        quote = quote[last_slash_index + 1:]
                        
                        last_date = payload_data['data']['last']['date']
                        last_date = datetime.fromtimestamp(last_date).isoformat()  # Convert timestamp to ISO format
                        
                        last_price = payload_data['data']['last']['value']
                        settlement = payload_data['data']['settlement']['value']
                        
                        now = datetime.now()
                        Last_update=now.strftime("%d/%m/%Y %H:%M:%S")

                        # Append data to array if not duplicate or update the existing entry
                        exists = False
                        for entry in data_array:
                            if entry["quote"] == quote :
                                exists = True
                                entry.update({"Date": last_date, "Last": last_price, "Last_update": Last_update, "settlement": settlement})
                                break

                        if not exists:
                            data_array.append({
                                "quote": quote,
                                "Date": last_date,
                                "Last": last_price,
                                "Last_update": Last_update,
                                "settlement": settlement
                            })
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    break
    except Exception as e:
        print(f"Error with WebSocket connection: {e}")

def insert_into_mysql(data):
       
    # Insert data into the MySQL database
    for entry in data:
        # Use a MERGE statement to insert or update
        merge_query = """
        MERGE INTO [sitagri].[dbo].[test_rt] AS target
        USING (VALUES (?, ?, ?, ?, ?)) AS source (quote, Date, Last,Last_update,settlement)
        ON target.quote = source.quote 
        WHEN MATCHED AND target.Last <> source.Last THEN
            UPDATE SET Date = source.Date, Last = source.Last, Last_update = source.Last_update , settlement = source.settlement
        WHEN NOT MATCHED THEN
            INSERT (quote, Date, Last,Last_update,settlement) VALUES (source.quote, source.Date, source.Last, source.Last_update, source.settlement);
        """

        cursor.execute(merge_query, (entry["quote"], entry["Date"], entry["Last"], entry["Last_update"], entry["settlement"]))
        conn.commit()
       
# RealTime Data Push database
async def push_data_periodically():
    global data_array
    
    while True:
        if data_array:           
            payload = data_array.copy()  # Copy current data
            print(len(data_array))
            insert_into_mysql(payload)
            data_array = []
            
        await asyncio.sleep(1)  # Wait for 1 second before next push

async def main():
    await asyncio.gather(
        get_websocket_messages(),
        push_data_periodically()
    )

asyncio.run(main())
