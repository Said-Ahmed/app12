from pydantic import BaseModel, EmailStr, ConfigDict, model_validator


class SUserRegister(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: EmailStr
    password: str
    password_repeat: str
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_repeat:
            raise ValueError('Пароли не совпадают')
        return self


class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class SUserDetail(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None


class SUserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    is_admin: bool = False