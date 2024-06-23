import crcmod.predefined

modbus_crc = crcmod.predefined.mkCrcFun('modbus')


def str_to_bool(value: str) -> bool:
    """
    Convert a string to a boolean value.
    """
    return value.lower() in {'true', '1', 't', 'y', 'yes'}
