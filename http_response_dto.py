from pydantic import BaseModel
from typing import Optional, Union

class HttpResponseDto(BaseModel):
  status: str = 'Ok'
  data: Optional[Union[str,dict,list]]
  metadata: Optional[dict]
