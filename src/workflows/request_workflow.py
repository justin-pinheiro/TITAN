import os
from typing import Optional, Iterator
from phi.agent import Agent
from phi.workflow import Workflow, RunResponse, RunEvent
from phi.utils.pprint import pprint_run_response
from phi.model.ollama import Ollama
from phi.utils.log import logger

ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

class RequestResponse(Workflow):
    router: Agent = Agent(
        model=Ollama(id="mistral:latest", host=ollama_host),
        description=
            f"""
                You are a router agent deciding if the request needs other agents or a simple LLM response. 
            """,
        instructions=[
            f"""
                Given a user request:
                - respond 'SIMPLE' if the request can be answered by a simple LLM.
                - respond 'COMPLEX' if the request needs specialized agents to provide accurate results.
            """],
        guidelines=[
            f"""
                Only answer with one word: 'SIMPLE' or 'COMPLEX'.
                Do not add comments.
            """],
        prevent_prompt_leakage=True,
        prevent_hallucinations=True,
        debug_mode=True
    )

    def run(self, request: str, use_cache: bool = True) -> Iterator[RunResponse]:
        logger.info(f"Generating a response for request: {request}")

        # Step 1: router agent
        num_tries = 0
        request_type:str = ""
        # Run until we get a valid request_type (SIMPLE or COMPLEX)
        while request_type != "SIMPLE" and request_type != "COMPLEX" and num_tries < 3:
            try:
                num_tries += 1
                request_type: str = self.router.run(request).content
                request_type = request_type.strip()
                logger.info(f"Router replied: [{request_type}]")
                if (
                    isinstance(request_type, str)
                    and (request_type == "SIMPLE" or request_type == "COMPLEX")
                ):
                    logger.info(f"Router decided that request is of type {request_type}.")
                else:
                    logger.warning("Router response invalid, trying again...")
            except Exception as e:
                logger.warning(f"Error running router: {e}")




request = "What events are in my calendar ?"

responder = RequestResponse()
responder.run(request)