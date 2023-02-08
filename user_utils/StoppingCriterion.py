class StoppingCriterion:
    def __init__(self):
        self.__best_result = 1.5 # smaller than 1.5 for 10 times, then converges
        self.__count = 0
        self.__total_count = 0
        self.__count_limit = 10

    def check(self, optcontent):
        """
        :param optcontent: an instance of the class RacosCommon.
                           Several functions can be invoked to get the contexts of the optimization,
                           which are listed as follows,
        optcontent.get_best_solution(): get the current optimal solution
        optcontent.get_data(): get all the solutions contained in the current solution pool
        optcontent.get_positive_data(): get positive solutions contained in the current solution pool
        optcontent.get_negative_data(): get negative solutions contained in the current solution pool

        :return: bool object.

        """
        self.__total_count += 1
        
        content_best_value = optcontent.get_best_solution().get_value()
        if content_best_value <= self.__best_result:            
            print("content_best_value",content_best_value)
            self.__count += 1
        else:
            #self.__best_result = content_best_value
            self.__count = 0
            
        if self.__count >= self.__count_limit:
            print("stopping criterion holds, total_count: %d" % self.__total_count)
            return True
        else:
            return False