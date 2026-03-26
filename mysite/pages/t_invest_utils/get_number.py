from decimal import Decimal

def quotation_to_decimal(quotation) -> Decimal:

    units = Decimal(quotation.units)
    fractional_part = Decimal(quotation.nano) / Decimal('1000000000')

    return units + fractional_part