
"""
 Copyright (C) 2005 Eric Ehlers
 Copyright (C) 2005 Plamen Neykov
 Copyright (C) 2005 Aurelien Chanudet

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it under the
 terms of the QuantLib license.  You should have received a copy of the
 license along with this program; if not, please email quantlib-dev@lists.sf.net
 The license is also available online at http://quantlib.org/html/license.html

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
"""

"""encapsulate state necessary to generate source code 
relating to a function parameter."""

import common
import serializable

class Value(serializable.Serializable):
    """Represent any value which may be passed to or received from a Function.

    This base class is presently empty and is included to clarify the class 
    hierarchy."""
    pass

class Parameter(Value):
    """encapsulate state necessary to generate source code 
    relating to a function parameter."""

    groupName = 'Parameters'

    def serialize(self, serializer):
        """load/unload class state to/from serializer object."""
        serializer.serializeAttribute(self.__dict__, common.NAME)
        serializer.serializeProperty(self.__dict__, common.TYPE)
        serializer.serializeProperty(self.__dict__, common.TENSOR_RANK)
        serializer.serializeProperty(self.__dict__, common.DESCRIPTION)
        serializer.serializeAttributeBoolean(self.__dict__, common.IGNORE)
        serializer.serializeAttribute(self.__dict__, common.DEFAULT)
        serializer.serializeAttribute(self.__dict__, common.LIBRARY_CLASS)
        serializer.serializeAttribute(self.__dict__, common.QL_TYPE)

    def postSerialize(self):
        """determine whether the datatype of this parameter requires a conversion."""
        if self.ignore or (self.tensorRank == common.SCALAR
        and self.type != common.ANY and not self.default):
            self.needsConversion = False
        else:
            self.needsConversion = True

class ReturnValue(Value):
    """encapsulate state necessary to generate source code 
    relating to a function return value."""

    # sometimes a ReturnValue will be treated like a Parameter
    # in which case the properties below require default values
    name = ''
    default = False

    def key(self):
        """return unique identifier for this object."""
        return 'returnValue'

    def serialize(self, serializer):
        """load/unload class state to/from serializer object."""
        serializer.serializeProperty(self.__dict__, common.TYPE)
        serializer.serializeProperty(self.__dict__, common.TENSOR_RANK)
        serializer.serializeProperty(self.__dict__, common.DESCRIPTION)

class ConstructorReturnValue(Value):
    """class to represent state shared by the return values
    of all constructors in QuantLibAddin"""

    name = ''
    type = 'string'
    tensorRank = 'scalar'
    description = 'handle of newly created object'
    default = False

