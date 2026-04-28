def num_in_kilo ( num:int|float ) -> str:
    """ Round number to kilos (nearest 1K)

    :param num: The number to format as number of kilos
    :type num: int|float
    :return: Returns number in kilos or the number passed if under 1K 
    :rtype: str
    """
    return str(num) if (num < 1000) else f"{round(num/1000)}K"
