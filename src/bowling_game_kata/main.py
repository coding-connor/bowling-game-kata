from abc import ABC, abstractmethod
from pydantic import BaseModel, field_validator
from pydantic.dataclasses import dataclass


def hello_world():
    return "hello world"


if __name__ == "__main__":
    test = hello_world()
