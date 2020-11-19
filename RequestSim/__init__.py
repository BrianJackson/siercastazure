import logging
import azure.functions as func


def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # replace with body parsing.
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        hash = req_body.get('hash')

    if hash:
        msg.set(req.get_body())
        return func.HttpResponse(
            f"Simulation request for {hash} was successfully received and queued.",
            status_code=202    
        )
    else:
        return func.HttpResponse(
             "The simulation request must include a hash",
             status_code=400
        )
