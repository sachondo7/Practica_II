def extract_values(data): 
    # Check if "statistic" exists in the message
    if "statistic" in data["payload"]:
        # Check if "last" exists in "statistic"
        if "last" in data["payload"]["statistic"]:
            last = data["payload"]["statistic"]["last"]
        else:
            last = None
        # Check if "askPx" exists in "statistic"
        if "askPx" in data["payload"]["statistic"]:
            askPx = data["payload"]["statistic"]["askPx"]
        else:
            askPx = None
        # Check if "bidPx" exists in "statistic"
        if "bidPx" in data["payload"]["statistic"]:
            bidPx = data["payload"]["statistic"]["bidPx"]
        else:
            bidPx = None
    else:
        last, askPx, bidPx = None, None, None
    return last, askPx, bidPx