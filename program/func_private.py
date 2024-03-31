from datetime import datetime, timedelta
import time
from pprint import pprint
from func_utils import format_number

# Place market order
# we need to place a "reduce only" order in order to close or open positions

# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
  # Get Position Id
  account_response = client.private.get_account()
  position_id = account_response.data["account"]["positionId"]

  # Get expiration time
  server_time = client.public.get_time()
  expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z", "")) + timedelta(seconds=70)

  # Place an order
  placed_order = client.private.create_order(
    position_id=position_id, # required for creating the order signature
    market=market,
    side=side,
    order_type="MARKET",
    post_only=False,
    size=size,
    #if I buy(go long), I want the price to be above today's market price
    #when you are trading, you are buying from the asks, from the price that is higher than the current price
    #if I was shorting, I would want the price that is lower or the same as current
    price=price,
    limit_fee='0.015',
    expiration_epoch_seconds=expiration.timestamp(),
    time_in_force="FOK", 
    reduce_only=reduce_only
  )
  # Return results
  return placed_order.data


def abort_all_positions(client):
    if client is None:
        raise Exception("Client object is None")

    try:
        # Cancel all orders
        client.private.cancel_all_orders()

        # Protect API
        time.sleep(0.5)

        # Get markets for reference of tick size
        markets = client.public.get_markets().data

        # Protect API
        time.sleep(0.5)

        # Get all open positions
        positions = client.private.get_positions(status="OPEN")
        all_positions = positions.data["positions"]

        # Handle open positions
        close_orders = []
        if len(all_positions) > 0:
            # Loop through each position
            for position in all_positions:
                try:
                    # Determine Market
                    market = position["market"]

                    # Determine Side
                    side = position["side"]

                    # Get the position size
                    position_size = abs(float(position["size"]))

                    # Determine the order size and direction based on the side
                    if side == "LONG":
                        # For LONG positions, we sell to close
                        order_size = position_size
                        order_side = "SELL"
                    else:  # side == "SHORT"
                        # For SHORT positions, we buy to close
                        order_size = position_size
                        order_side = "BUY"

                    # Format the order_size to a string with a maximum of 8 decimal places
                    order_size_str = "{:.8f}".format(order_size).rstrip("0").rstrip(".")

                    # Check if the order size is greater than zero
                    if order_size > 0:
                        # Get Price
                        price = float(position["entryPrice"])

                        # Determining the worst acceptable price (I will accept the price that is worse by 70% from initial position price)
                        accept_price = price * 0.7 if side == "LONG" else price * 1.3
                        tick_size = markets["markets"][market]["tickSize"]
                        accept_price = format_number(accept_price, tick_size)

                        # Place order to close
                        order = place_market_order(
                            client,
                            market,
                            order_side,
                            order_size_str,
                            accept_price,
                            True
                        )

                        # Append the result
                        close_orders.append(order)

                        # Protect API
                        time.sleep(0.2)
                    else:
                        print(f"Skipping order for market {market} due to zero order size.")

                except Exception as e:
                    print(f"Error closing position for market {market}:")
                    print(str(e))
                    continue

        # Return closed orders
        return close_orders

    except Exception as e:
        print("Error in abort_all_positions:")
        print(str(e))
        raise e
"""
# Abort all open positions
def abort_all_positions(client):
  
  # Cancel all orders
  client.private.cancel_all_orders()

  # Protect API
  time.sleep(0.5)

  # Get markets for reference of tick size
  markets = client.public.get_markets().data

  # Protect API
  time.sleep(0.5)

  # Get all open positions
  positions = client.private.get_positions(status="OPEN")
  all_positions = positions.data["positions"]

  # Handle open positions
  close_orders = []
  if len(all_positions) > 0:

    # Loop through each position
    for position in all_positions:

      # Determine Market
      market = position["market"]

      # Determine Side
      side = "BUY"
      if position["side"] == "LONG":
        side = "SELL"

      # Get Price
      price = float(position["entryPrice"])
      #determining the worst acceptible price (I will accept the price that is worse by 70% from initial position price)
      accept_price = price * 1.7 if side == "BUY" else price * 0.3
      tick_size = markets["markets"][market]["tickSize"]
      accept_price = format_number(accept_price, tick_size)

      # Place order to close
      order = place_market_order(
        client,
        market,
        side,
        position["sumOpen"],
        accept_price,
        True
      )

      # Append the result
      close_orders.append(order)

      # Protect API
      time.sleep(0.2)


    # Override json file with empty list
    bot_agents = []
    with open("bot_agents.json", "w") as f:
      json.dump(bot_agents, f)


    # Return closed orders
return close_orders

"""

