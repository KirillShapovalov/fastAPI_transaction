import pydantic as pd


class QuerySchema(pd.BaseModel):
    user_id: int
    balance_dif: float
