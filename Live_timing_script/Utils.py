def time_str_to_seconds(time_str):
        """
        Convert a time string in the format 'hh:mm:ss.ss', 'mm:ss.ss', or 'ss.ss'
        into a float representing the total number of seconds.

        :param time_str: A string representing the time (e.g., '1:16.861', '0:01:16.861', or '76.861')
        :return: A float representing the time in seconds.
        """
        time_parts = time_str.split(':')
        
        # Check the number of parts and convert accordingly
        if len(time_parts) == 3:  # Format hh:mm:ss.ss
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = float(time_parts[2])
            total_seconds = hours * 3600 + minutes * 60 + seconds
        
        elif len(time_parts) == 2:  # Format mm:ss.ss
            minutes = int(time_parts[0])
            seconds = float(time_parts[1])
            total_seconds = minutes * 60 + seconds
        
        else:  # Format ss.ss
            total_seconds = float(time_parts[0])
        
        return total_seconds