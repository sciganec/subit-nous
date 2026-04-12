"""Abstract Syntax Tree for SUBIT Query Language."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Union
from enum import Enum


class Axis(Enum):
    WHO = "WHO"
    WHERE = "WHERE"
    WHEN = "WHEN"
    MODE = "MODE"


class AxisValue(Enum):
    # WHO
    ME = "ME"
    WE = "WE"
    YOU = "YOU"
    THEY = "THEY"
    # WHERE
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"
    NORTH = "NORTH"
    # WHEN
    SPRING = "SPRING"
    SUMMER = "SUMMER"
    AUTUMN = "AUTUMN"
    WINTER = "WINTER"
    # MODE
    STATE = "STATE"
    VALUE = "VALUE"
    FORM = "FORM"
    FORCE = "FORCE"


class QueryType(Enum):
    TEXT = "text"
    GRAPH = "graph"
    FILES = "files"


class Condition(ABC):
    """Base class for all conditions."""
    
    @abstractmethod
    def evaluate(self, subit: int) -> bool:
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        pass


@dataclass
class Eq(Condition):
    """Equality condition: axis = value"""
    axis: Axis
    value: AxisValue
    
    def evaluate(self, subit: int) -> bool:
        shift = {"WHO": 6, "WHERE": 4, "WHEN": 2, "MODE": 0}[self.axis.value]
        axis_bits = (subit >> shift) & 0b11
        
        value_map = {
            # WHO
            AxisValue.ME: 0b10, AxisValue.WE: 0b11,
            AxisValue.YOU: 0b01, AxisValue.THEY: 0b00,
            # WHERE
            AxisValue.EAST: 0b10, AxisValue.SOUTH: 0b11,
            AxisValue.WEST: 0b01, AxisValue.NORTH: 0b00,
            # WHEN
            AxisValue.SPRING: 0b10, AxisValue.SUMMER: 0b11,
            AxisValue.AUTUMN: 0b01, AxisValue.WINTER: 0b00,
            # MODE
            AxisValue.STATE: 0b10, AxisValue.VALUE: 0b11,
            AxisValue.FORM: 0b01, AxisValue.FORCE: 0b00,
        }
        return axis_bits == value_map[self.value]
    
    def __repr__(self) -> str:
        return f"Eq({self.axis.value}={self.value.value})"


@dataclass
class And(Condition):
    left: Condition
    right: Condition
    
    def evaluate(self, subit: int) -> bool:
        return self.left.evaluate(subit) and self.right.evaluate(subit)
    
    def __repr__(self) -> str:
        return f"And({self.left}, {self.right})"


@dataclass
class Or(Condition):
    left: Condition
    right: Condition
    
    def evaluate(self, subit: int) -> bool:
        return self.left.evaluate(subit) or self.right.evaluate(subit)
    
    def __repr__(self) -> str:
        return f"Or({self.left}, {self.right})"


@dataclass
class Not(Condition):
    condition: Condition
    
    def evaluate(self, subit: int) -> bool:
        return not self.condition.evaluate(subit)
    
    def __repr__(self) -> str:
        return f"Not({self.condition})"


@dataclass
class Distance(Condition):
    """Distance condition: DISTANCE > 2, DISTANCE < 4, etc."""
    op: str  # '<', '>', '<=', '>=', '='
    value: int
    
    def evaluate(self, subit: int) -> bool:
        # This requires a reference subit - will be set during evaluation
        raise NotImplementedError("Distance requires reference subit")
    
    def evaluate_with_ref(self, subit: int, ref_subit: int) -> bool:
        dist = bin(subit ^ ref_subit).count('1')
        if self.op == '<':
            return dist < self.value
        elif self.op == '<=':
            return dist <= self.value
        elif self.op == '>':
            return dist > self.value
        elif self.op == '>=':
            return dist >= self.value
        elif self.op == '=':
            return dist == self.value
        return False
    
    def __repr__(self) -> str:
        return f"Distance({self.op} {self.value})"


@dataclass
class Query:
    """Complete query with type and condition."""
    query_type: QueryType
    condition: Optional[Condition]
    source: str  # file path, graph path, or text
    
    def __repr__(self) -> str:
        return f"Query(type={self.query_type.value}, condition={self.condition}, source={self.source})"