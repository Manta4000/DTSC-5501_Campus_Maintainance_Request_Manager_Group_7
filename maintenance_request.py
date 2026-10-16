class MaintenanceRequest: 
    def __init__(self, request_id, building, category, priority, reported_time, status):
        self.request_id = request_id
        self.building = building
        self.category = category
        self.priority = priority 
        self.reported_time = reported_time
        self.status = status 

        if self.priority == 1:
            print("Urgent")
        elif self.priority == 2:
            print("High")
        elif self.priority == 3:
            print("Normal")
        elif self.priority == 4:
            print("Low")
