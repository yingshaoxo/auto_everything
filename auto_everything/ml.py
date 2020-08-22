class DataProcessor():
    """
    To implement some functionality related to data
    """

    def __init__(self):
        pass

    def get_time_series_data_from_a_list(self, the_list, sequence_length):
        """
        Get sub sequences for LSTM network.

        Parameters
        ----------
        the_list: 
        sequence_length: int
            how long you want the subsequence to be.

        Returns
        -------
        tuple
            return ([features], [labels])
        """
        assert len(the_list)>=sequence_length+1, "len(the_list) should >= sequence_length + 1"
        array_1d = []
        array_2d = []
        array_target = []
        for element in the_list:
            array_1d.append(element)
            if len(array_1d) == sequence_length+1:
                target = array_1d.pop()
                array_target.append(target)
                array_2d.append(array_1d.copy())
                array_1d.clear()
        return array_2d, array_target


if __name__ == "__main__":
    from pprint import pprint
    data_processor = DataProcessor()
    the_list = list(range(1000))
    features, labels = data_processor.get_time_series_data_from_a_list(the_list, 10)
