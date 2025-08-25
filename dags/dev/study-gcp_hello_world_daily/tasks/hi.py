# ---
# python_callable: run
# ---

from loguru import logger

def run(**kwargs):
  greeeting = kwargs["params"]["mensagem"]
  logger.info(f"{greeeting}")
  return greeeting