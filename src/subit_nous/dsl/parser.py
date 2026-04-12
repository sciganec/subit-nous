"""Parser for SUBIT Query Language."""

import re
from typing import Optional
from .ast import (
    Axis, AxisValue, QueryType, Condition,
    Eq, And, Or, Not, Distance, Query
)


class Parser:
    """Parser for SUBIT Query Language."""
    
    # Mapping for axis values (including aliases)
    VALUE_MAP = {
        # WHO
        "ME": AxisValue.ME, "WE": AxisValue.WE,
        "YOU": AxisValue.YOU, "THEY": AxisValue.THEY,
        # WHERE
        "EAST": AxisValue.EAST, "SOUTH": AxisValue.SOUTH,
        "WEST": AxisValue.WEST, "NORTH": AxisValue.NORTH,
        # WHEN
        "SPRING": AxisValue.SPRING, "SUMMER": AxisValue.SUMMER,
        "AUTUMN": AxisValue.AUTUMN, "WINTER": AxisValue.WINTER,
        # MODE (primary)
        "STATE": AxisValue.STATE, "VALUE": AxisValue.VALUE,
        "FORM": AxisValue.FORM, "FORCE": AxisValue.FORCE,
        # MODE (Greek aliases)
        "LOGOS": AxisValue.STATE, "ETHOS": AxisValue.VALUE,
        "PATHOS": AxisValue.FORM, "THYMOS": AxisValue.FORCE,
    }
    
    AXIS_MAP = {
        "WHO": Axis.WHO, "WHERE": Axis.WHERE,
        "WHEN": Axis.WHEN, "MODE": Axis.MODE
    }
    
    def __init__(self):
        self.tokens = []
        self.pos = 0
    
    def parse(self, query_str: str) -> Query:
        """Parse query string into Query AST."""
        # Clean up the query string
        query_str = query_str.strip()
        
        # Parse query type
        query_type = self._parse_query_type(query_str)
        
        # Extract WHERE clause
        where_match = re.search(r'WHERE\s+(.+)', query_str, re.IGNORECASE)
        if where_match:
            condition_str = where_match.group(1).strip()
            condition = self._parse_condition(condition_str)
        else:
            condition = None
        
        # Extract source (FROM)
        from_match = re.search(r'FROM\s+(\S+)', query_str, re.IGNORECASE)
        source = from_match.group(1) if from_match else ""
        
        return Query(
            query_type=query_type,
            condition=condition,
            source=source
        )
    
    def _parse_query_type(self, query_str: str) -> QueryType:
        """Parse query type from string."""
        lower = query_str.lower()
        if lower.startswith("text"):
            return QueryType.TEXT
        elif lower.startswith("graph"):
            return QueryType.GRAPH
        elif lower.startswith("files"):
            return QueryType.FILES
        else:
            return QueryType.TEXT
    
    def _parse_condition(self, cond_str: str) -> Condition:
        """Parse condition string into AST."""
        cond_str = cond_str.strip()
        
        # Handle parentheses
        if cond_str.startswith('(') and cond_str.endswith(')'):
            return self._parse_condition(cond_str[1:-1])
        
        # Handle OR (lowest precedence)
        or_parts = self._split_by_operator(cond_str, 'OR')
        if len(or_parts) > 1:
            left = self._parse_condition(or_parts[0])
            right = self._parse_condition(or_parts[1])
            return Or(left, right)
        
        # Handle AND
        and_parts = self._split_by_operator(cond_str, 'AND')
        if len(and_parts) > 1:
            left = self._parse_condition(and_parts[0])
            right = self._parse_condition(and_parts[1])
            return And(left, right)
        
        # Handle NOT
        if cond_str.startswith('NOT '):
            inner = self._parse_condition(cond_str[4:])
            return Not(inner)
        
        # Handle DISTANCE
        dist_match = re.match(r'DISTANCE\s*([<>]=?|=)\s*(\d+)', cond_str, re.IGNORECASE)
        if dist_match:
            op = dist_match.group(1)
            value = int(dist_match.group(2))
            return Distance(op, value)
        
        # Handle equality: AXIS = VALUE
        eq_match = re.match(r'(\w+)\s*=\s*(\w+)', cond_str)
        if eq_match:
            axis_str = eq_match.group(1).upper()
            value_str = eq_match.group(2).upper()
            
            axis = self.AXIS_MAP.get(axis_str)
            value = self.VALUE_MAP.get(value_str)
            
            if axis and value:
                return Eq(axis, value)
        
        raise ValueError(f"Could not parse condition: {cond_str}")
    
    def _split_by_operator(self, s: str, op: str) -> list:
        """Split string by operator, respecting parentheses."""
        parts = []
        current = []
        depth = 0
        i = 0
        
        while i < len(s):
            if s[i] == '(':
                depth += 1
                current.append(s[i])
            elif s[i] == ')':
                depth -= 1
                current.append(s[i])
            elif depth == 0 and s[i:i+len(op)] == op:
                parts.append(''.join(current).strip())
                current = []
                i += len(op)
                continue
            else:
                current.append(s[i])
            i += 1
        
        if current:
            parts.append(''.join(current).strip())
        
        return parts


def parse(query_str: str) -> Query:
    """Convenience function to parse query."""
    return Parser().parse(query_str)


def _parse_condition(self, cond_str: str) -> Condition:
    """Parse condition string into AST."""
    cond_str = cond_str.strip()
    
    # DIAGNOSTIC
    print(f"[DEBUG] _parse_condition received: '{cond_str}'")
    
    # ... rest of the code