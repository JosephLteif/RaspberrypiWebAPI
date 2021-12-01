from pydantic import BaseModel
class Sensor(BaseModel):
	name: str
	category: str
	value: float
	status: str