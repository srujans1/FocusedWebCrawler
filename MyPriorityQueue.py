from Queue import PriorityQueue

# Queue implementation for Priority Queue that keeps track of insertion and 
# checks queue before new insertion to avoid duplicate insertions

class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        #self.all_items = set()
        self.counter = 0

    def put(self, item, priority):
        #if item not in self.all_items:      # Check if item already exists or ever existed in the queue to prevent duplicate effort
            PriorityQueue.put(self, (priority, self.counter, item))
            #self.all_items.add(item)
            self.counter += 1

    def get(self, *args, **kwargs):
        priority, _, item = PriorityQueue.get(self, *args, **kwargs)
        return (priority,item) 
    
    #def inQueue(self, item):            # Method to check if item is enqueued or not
    #    if item in self.all_items:
    #        return True
    #    else:
    #       return False
    
    #def getPriority(self, item):
        
    
